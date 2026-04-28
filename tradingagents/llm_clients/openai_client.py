import logging
import os
from typing import Any, Optional

from langchain_openai import ChatOpenAI

from .base_client import BaseLLMClient
from .validators import validate_model

logger = logging.getLogger(__name__)


class UnifiedChatOpenAI(ChatOpenAI):
    """ChatOpenAI subclass that strips incompatible params for certain models."""

    def __init__(self, **kwargs):
        model = kwargs.get("model", "")
        if self._is_reasoning_model(model):
            kwargs.pop("temperature", None)
            kwargs.pop("top_p", None)
        super().__init__(**kwargs)

    @staticmethod
    def _is_reasoning_model(model: str) -> bool:
        """Check if model is a reasoning model that doesn't support temperature."""
        model_lower = model.lower()
        return (
            model_lower.startswith("o1")
            or model_lower.startswith("o3")
            or "gpt-5" in model_lower
        )


class OpenAIClient(BaseLLMClient):
    """Client for OpenAI, Ollama, OpenRouter, and xAI providers."""

    def __init__(
        self,
        model: str,
        base_url: Optional[str] = None,
        provider: str = "openai",
        **kwargs,
    ):
        super().__init__(model, base_url, **kwargs)
        self.provider = provider.lower()

    def get_llm(self) -> Any:
        """Return configured ChatOpenAI instance."""
        llm_kwargs = {"model": self.model}

        if self.provider == "xai":
            llm_kwargs["base_url"] = "https://api.x.ai/v1"
            api_key = os.environ.get("XAI_API_KEY")
            if api_key:
                llm_kwargs["api_key"] = api_key
        elif self.provider == "openrouter":
            llm_kwargs["base_url"] = "https://openrouter.ai/api/v1"
            api_key = os.environ.get("OPENROUTER_API_KEY")
            if api_key:
                llm_kwargs["api_key"] = api_key
        elif self.provider == "ollama":
            # Use ExperimentConfig/YAML backend_url (e.g. per-job SLURM port); else default 11434.
            llm_kwargs["base_url"] = self.base_url or "http://localhost:11434/v1"
            llm_kwargs["api_key"] = "ollama"
            self._check_ollama(llm_kwargs["base_url"])
        elif self.base_url:
            llm_kwargs["base_url"] = self.base_url

        for key in ("timeout", "max_retries", "reasoning_effort", "api_key", "callbacks"):
            if key in self.kwargs:
                llm_kwargs[key] = self.kwargs[key]

        return UnifiedChatOpenAI(**llm_kwargs)

    def _check_ollama(self, base_url: str) -> None:
        """Log warnings if Ollama server or model is not available."""
        from .local_utils import check_ollama_health, check_ollama_model

        api_base = base_url.replace("/v1", "")
        healthy, msg = check_ollama_health(api_base)
        if not healthy:
            logger.warning("Ollama: %s", msg)
            return
        if not check_ollama_model(self.model, api_base):
            logger.warning(
                "Ollama: model '%s' not found locally. "
                "Pull it with: ollama pull %s",
                self.model,
                self.model,
            )

    def validate_model(self) -> bool:
        """Validate model for the provider."""
        return validate_model(self.provider, self.model)
