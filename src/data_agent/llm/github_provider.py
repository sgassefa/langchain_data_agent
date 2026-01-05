"""GitHub Models LLM provider.

This module provides GitHub Models integration using OpenAI-compatible API.
GitHub Models offers free access to models like GPT-4o, GPT-4o-mini, etc.
"""

import os
from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from data_agent.llm.base import BaseProvider


class GitHubModelsProvider(BaseProvider):
    """GitHub Models LLM provider.

    GitHub Models provides free access to AI models through an OpenAI-compatible API.
    Get your token at: https://github.com/settings/tokens

    Attributes:
        name: Provider identifier ('github').
    """

    name = "github"

    def create_llm(self, **kwargs: Any) -> BaseChatModel:
        """Create a GitHub Models chat model.

        Args:
            api_key: GitHub token (or uses GITHUB_TOKEN env var).
            deployment_name: Model name (alias for model parameter).
            model: Model name (default: 'gpt-4o-mini').
                   Available: gpt-4o, gpt-4o-mini, etc.
            temperature: Sampling temperature (default: 0).
            **kwargs: Additional ChatOpenAI parameters.

        Returns:
            Configured ChatOpenAI instance pointing to GitHub Models.
        """
        # Get API key from param or environment
        api_key = kwargs.get("api_key") or os.getenv("GITHUB_TOKEN")
        # Support both 'model' and 'deployment_name' (for compatibility with Azure config)
        model = kwargs.get("deployment_name") or kwargs.get("model", "gpt-4o-mini")
        
        return ChatOpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=api_key,
            model=model,
            temperature=kwargs.get("temperature", 0),
            max_tokens=kwargs.get("max_tokens", 2000),
        )
