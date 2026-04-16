"""Model Analyst — reads deep-trading artifacts (metrics and/or signals).

Two modes (see ``model_input_mode``):

- **metrics:** historical performance via ``get_model_metrics`` (no lookahead).
- **signals:** per-strategy directional state via ``get_model_signals`` (last bar
  before the trade date; no lookahead).
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from tradingagents.agents.utils.model_metrics_tool import get_model_metrics
from tradingagents.agents.utils.model_signals_tool import get_model_signals


def create_model_analyst(llm, model_input_mode: str = "metrics"):

    def model_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]

        mode = (model_input_mode or "metrics").lower().strip()
        if mode == "signals":
            tools = [get_model_signals]
            system_message = (
                "You are a quantitative model analyst. Your job is to retrieve each "
                "configured forecasting strategy's **current directional stance** "
                "(BUY / SELL / HOLD) from deep-trading backtests for the given asset.\n\n"
                "STRICT RULES:\n"
                "1. You MUST call the get_model_signals tool with the asset symbol and "
                "the current trade date. The tool uses only hourly bars **strictly "
                "before** that date — no future information.\n"
                "2. You MUST NOT use any knowledge from your training data about market "
                "prices, events, or trends. Base your analysis ONLY on the tool output.\n"
                "3. Interpret **direction_label** and **position** per strategy; do not "
                "invent positions not present in the JSON.\n\n"
                "After retrieving the signals, write a concise report covering:\n"
                "- Agreement or conflict: how many models are long vs short vs flat\n"
                "- Which strategies appear most aggressive (large |position|)\n"
                "- How you would weight these mechanical signals alongside other analysts\n\n"
                "End with a Markdown table listing each strategy, direction_label, "
                "position, and bar_timestamp_utc."
            )
        else:
            tools = [get_model_metrics]
            system_message = (
                "You are a quantitative model analyst. Your job is to retrieve and "
                "interpret the historical performance metrics of the configured "
                "forecasting strategies (from deep-trading backtests) for the given asset.\n\n"
                "STRICT RULES:\n"
                "1. You MUST call the get_model_metrics tool with the asset symbol and "
                "the current trade date as the cutoff. This ensures you only see data "
                "BEFORE the current date — no future information.\n"
                "2. You MUST NOT use any knowledge from your training data about market "
                "prices, events, or trends. Base your analysis ONLY on the tool output.\n"
                "3. Do NOT predict future performance. Only summarize and compare past "
                "model performance.\n\n"
                "After retrieving the metrics, write a detailed report covering:\n"
                "- Which model(s) performed best / worst by Sharpe ratio and cumulative return\n"
                "- Risk profile comparison (max drawdown, volatility)\n"
                "- Trading efficiency (hit rate, turnover)\n"
                "- Overall assessment: which model signals seem most reliable based on "
                "historical track record\n\n"
                "Append a Markdown summary table at the end comparing all strategies "
                "returned by the tool across key metrics."
            )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI assistant, collaborating with other assistants."
                    " Use the provided tools to progress towards answering the question."
                    " If you are unable to fully answer, that's OK; another assistant with different tools"
                    " will help where you left off. Execute what you can to make progress."
                    " If you or any other assistant has the FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** or deliverable,"
                    " prefix your response with FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** so the team knows to stop."
                    " You have access to the following tools: {tool_names}.\n{system_message}"
                    "For your reference, the current date is {current_date}. The asset we are analyzing is {ticker}.",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        prompt = prompt.partial(system_message=system_message)
        prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
        prompt = prompt.partial(current_date=current_date)
        prompt = prompt.partial(ticker=ticker)

        chain = prompt | llm.bind_tools(tools)

        result = chain.invoke(state["messages"])

        report = ""
        if len(result.tool_calls) == 0:
            report = result.content

        return {
            "messages": [result],
            "model_report": report,
        }

    return model_analyst_node
