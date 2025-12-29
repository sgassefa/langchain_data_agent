"""Code execution backends for sandboxed Python execution.

This module provides the executor for running LLM-generated Python code
in Azure Container Apps Dynamic Sessions with Hyper-V isolation.

Usage:
    from data_agent.executors import create_executor

    # Create from configuration
    executor = create_executor(config.code_interpreter)

    # Execute code
    result = await executor.execute("print('Hello')")
    if result.success:
        print(result.output)

Note:
    Visualization support requires deploying an Azure Container Apps
    session pool. See docs/CONFIGURATION.md for setup instructions.
"""

from typing import TYPE_CHECKING

from data_agent.executors.base import CodeExecutor, ExecutionResult, ExecutionStatus

if TYPE_CHECKING:
    from data_agent.config import CodeInterpreterConfig

__all__ = [
    "CodeExecutor",
    "ExecutionResult",
    "ExecutionStatus",
    "create_executor",
]


def create_executor(config: "CodeInterpreterConfig") -> CodeExecutor:
    """Create a code executor based on configuration.

    Args:
        config: CodeInterpreterConfig with endpoint settings.

    Returns:
        Configured AzureSessionsExecutor instance.

    Raises:
        ValueError: If azure_sessions_endpoint is not configured.
        TypeError: If config is not a CodeInterpreterConfig.
    """
    from data_agent.config import CodeInterpreterConfig

    if not isinstance(config, CodeInterpreterConfig):
        raise TypeError(f"Expected CodeInterpreterConfig, got {type(config)}")

    from data_agent.executors.azure_sessions import AzureSessionsExecutor

    return AzureSessionsExecutor(
        pool_management_endpoint=config.azure_sessions_endpoint,
    )
