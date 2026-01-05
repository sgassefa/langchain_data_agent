"""OpenAI provider for direct OpenAI API access."""

import os
from typing import Any

from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel

from data_agent.llm.base import BaseProvider


class OpenAIProvider(BaseProvider):
    """Provider for OpenAI's API."""

    name = "openai"

    def create_llm(self, **kwargs: Any) -> BaseChatModel:
        api_key = kwargs.get("api_key") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable or api_key parameter is required")
        
        # Use deployment_name as model name
        model = kwargs.get("deployment_name", "gpt-4o-mini")
        temperature = kwargs.get("temperature", 0.0)
        
        return ChatOpenAI(
            api_key=api_key,
            model=model,
            temperature=temperature,
        )
