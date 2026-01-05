"""Data Agent CLI."""

import asyncio
import logging
import os
from pathlib import Path
from typing import Annotated, Any
from uuid import uuid4

import typer
from dotenv import load_dotenv
from rich.prompt import Prompt

from data_agent import DataAgentFlow
from data_agent.cli.console import console, print_error
from data_agent.cli.output import (
    print_dashboard,
    print_error_panel,
    print_query_info,
    print_response,
)
from data_agent.config import CONFIG_DIR, AgentConfig
from data_agent.config_loader import ConfigLoader
from data_agent.core.logging import setup_logging
from data_agent.models.state import OutputState

load_dotenv()

logger = logging.getLogger(__name__)

LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
}


app = typer.Typer(
    name="data-agent",
    help="Natural Language to SQL Query Agent",
    no_args_is_help=True,
    rich_markup_mode="rich",
)


def get_config_choices() -> list[str]:
    """Get available configuration file names.

    Returns:
        List of config names (without .yaml extension).
    """
    return [f.stem for f in CONFIG_DIR.glob("*.yaml")]


def validate_config(config: str) -> Path:
    """Validate configuration exists and return its path.

    Args:
        config: Name of the configuration file (without extension).

    Returns:
        Path to the configuration file.

    Raises:
        typer.Exit: If the configuration file does not exist.
    """
    config_path = CONFIG_DIR / f"{config}.yaml"
    if not config_path.exists():
        available = ", ".join(get_config_choices())
        print_error(f"Config '{config}' not found. Available: {available}")
        raise typer.Exit(1)
    return config_path


def load_config(config: str | None) -> tuple[AgentConfig, str]:
    """Load configuration, either by name or all configs merged.

    Args:
        config: Name of the configuration file, or None to load all.

    Returns:
        Tuple of (AgentConfig, display_name).
    """
    if config:
        validate_config(config)
        return ConfigLoader.load_by_name(config), config
    return ConfigLoader.load_all(), "all"


def get_azure_credentials() -> tuple[str | None, str | None, str | None]:
    """Get Azure OpenAI credentials from environment variables.

    These are optional as each agent can have its own LLM configuration.

    Returns:
        Tuple of (endpoint, api_key, deployment_name). Values may be None.
    """
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

    return endpoint, api_key, deployment


async def handle_clarification_request(
    payload: dict[str, Any],
) -> str | None:
    """Handle clarification request when intent detection needs more context.

    Prompts the user to clarify or rephrase their question so intent
    detection can better route to the appropriate agent.

    Args:
        payload: Interrupt payload with 'message', 'original_question',
            and optional 'hint' keys.

    Returns:
        The clarified question, or None if the user cancelled.
    """
    message = payload.get("message", "Could you please clarify your question?")
    hint = payload.get("hint", "")

    console.print()
    console.print(f"[warning]⚠️ {message}[/warning]")
    if hint:
        console.print(f"[muted]Hint: {hint}[/muted]")

    try:
        clarification = Prompt.ask(
            "[cyan]Your clarified question[/cyan]",
        )
        return clarification.strip() if clarification.strip() else None
    except KeyboardInterrupt:
        return None


async def execute_query(
    flow: DataAgentFlow,
    question: str,
    thread_id: str,
) -> tuple[OutputState | dict[str, Any], str]:
    """Execute a query against the data agent flow.

    Handles the query execution and any interrupts that require user
    input, such as clarifying ambiguous questions.

    Args:
        flow: The DataAgentFlow instance to query.
        question: The natural language question to execute.
        thread_id: Unique identifier for the conversation thread.

    Returns:
        Tuple of (query result, final question used).
    """
    with console.status("[cyan]Thinking...[/cyan]", spinner="dots"):
        result = await flow.run(question, thread_id=thread_id)

    if not isinstance(result, dict):
        result = dict(result)

    if isinstance(result, dict) and "__interrupt__" in result:
        interrupt_data = result["__interrupt__"]
        if interrupt_data and len(interrupt_data) > 0:
            interrupt_obj = interrupt_data[0]
            payload = (
                interrupt_obj.value
                if hasattr(interrupt_obj, "value")
                else interrupt_obj
            )

            if payload.get("type") == "clarification_needed":
                clarified = await handle_clarification_request(payload)
                if clarified is None:
                    return {"error": "User cancelled"}, question

                with console.status("[cyan]Thinking...[/cyan]", spinner="dots"):
                    resume_result = await flow.run(
                        resume_value={"question": clarified},
                        thread_id=thread_id,
                    )
                if not isinstance(resume_result, dict):
                    resume_result = dict(resume_result)
                return resume_result, clarified

    return result, question


def display_result(
    result: OutputState | dict[str, Any],
    question: str,
    verbose: bool = False,
) -> None:
    """Display the query result to the console.

    Shows query info (if verbose), the response, and any errors.
    When verbose is True, also prints the message history with pretty_print().

    Args:
        result: The query result from execute_query.
        question: The original question (for verbose display).
        verbose: Whether to show detailed query state info and message history.
    """
    result_dict = result if isinstance(result, dict) else dict(result)

    # Print message history when verbose
    if verbose:
        messages = result_dict.get("messages", [])
        if messages:
            console.print("\n[dim]─── Message History ───[/dim]")
            turn = 0
            for i, msg in enumerate(messages):
                # Track turns: each HumanMessage starts a new turn
                msg_type = getattr(msg, "type", "")
                if msg_type == "human":
                    turn += 1
                    console.print(f"[dim]── Turn {turn} ──[/dim]")
                if hasattr(msg, "pretty_print"):
                    msg.pretty_print()
                else:
                    console.print(f"[dim]{msg}[/dim]")
            console.print("[dim]───────────────────────[/dim]\n")

    if verbose:
        print_query_info(
            question=question,
            agent=result_dict.get("datasource_name"),
            sql=result_dict.get("generated_sql"),
            rewritten_question=result_dict.get("rewritten_question"),
        )

    if result_dict.get("final_response"):
        print_response(result_dict["final_response"])

    # Always show the generated SQL if available
    generated_sql = result_dict.get("generated_sql")
    if generated_sql:
        from data_agent.cli.output import print_sql
        print_sql(generated_sql)

    error = result_dict.get("error")
    if error and error != "out_of_scope" and not str(error).startswith("Interrupt"):
        print_error_panel(str(error))


@app.command()
def query(
    question: Annotated[str, typer.Argument(help="The question to ask")],
    config: Annotated[
        str | None,
        typer.Option(
            "--config",
            "-c",
            help="Configuration to use (default: load all configs)",
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose/--quiet", "-v/-q", help="Show query state (agent, SQL)"
        ),
    ] = False,
    log_level: Annotated[
        str | None,
        typer.Option(
            "--log-level",
            "-l",
            help="Logging level (debug, info, warning, error)",
        ),
    ] = None,
) -> None:
    """Run a single query and exit.

    Executes the given question against the configured data agents
    and displays the result.
    """
    if log_level:
        setup_logging(LOG_LEVELS.get(log_level.lower(), logging.INFO))
    agent_config, config_name = load_config(config)
    endpoint, api_key, deployment = get_azure_credentials()

    async def _run() -> None:
        async with DataAgentFlow(
            config=agent_config,
            azure_endpoint=endpoint,
            api_key=api_key,
            deployment_name=deployment,
        ) as flow:
            agents = [
                {"name": agent.name, "description": agent.description}
                for agent in flow.config.data_agents
            ]
            print_dashboard(config_name, agents)

            thread_id = uuid4().hex
            result, final_question = await execute_query(flow, question, thread_id)
            display_result(result, final_question, verbose)

    asyncio.run(_run())


@app.command()
def teach(
    topic: Annotated[
        str | None,
        typer.Argument(
            help="Optional topic or question to start with",
        ),
    ] = None,
    log_level: Annotated[
        str | None,
        typer.Option(
            "--log-level",
            "-l",
            help="Logging level (debug, info, warning, error)",
        ),
    ] = None,
) -> None:
    """Start teaching mode - learn database concepts interactively.

    A conversational AI tutor for learning relational database concepts.
    No database connection required - perfect for learning fundamentals
    like ERD, normalization, SQL syntax, and schema design.

    Examples:
        # Start interactive teaching session
        data-agent teach

        # Ask a specific question
        data-agent teach "What is a primary key?"

        # Learn about normalization
        data-agent teach "Explain 1NF, 2NF, and 3NF with examples"
    """
    import os
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
    from rich.markdown import Markdown
    from rich.panel import Panel

    if log_level:
        setup_logging(LOG_LEVELS.get(log_level.lower(), logging.INFO))

    # Get GitHub token
    api_key = os.getenv("GITHUB_TOKEN") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print_error("No API key found. Set GITHUB_TOKEN or OPENAI_API_KEY in .env")
        raise typer.Exit(1)

    # Determine provider based on available key
    if os.getenv("GITHUB_TOKEN"):
        llm = ChatOpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.getenv("GITHUB_TOKEN"),
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=2000,
        )
    else:
        llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=2000,
        )

    # Teaching system prompt
    system_prompt = """You are a friendly and patient database instructor teaching a graduate-level course on Relational Database Management Systems. Your students have ZERO background in databases.

## Your Teaching Style
- Use simple, clear explanations with real-world analogies
- Always provide concrete examples (use a library, university, or music store as examples)
- When explaining SQL, show the syntax AND what it means in plain English
- Break complex topics into digestible pieces
- Encourage questions and validate student understanding
- Use tables and diagrams (in ASCII/text) when helpful

## Topics You Can Teach
- Database fundamentals (what is a database, why use one, types)
- Relational model (tables, rows, columns, records, fields)
- Entities, attributes, and relationships
- Entity-Relationship Diagrams (ERD) - draw them in ASCII
- Keys (primary, foreign, candidate, composite)
- Cardinality (1:1, 1:N, M:N relationships)
- SQL basics (SELECT, INSERT, UPDATE, DELETE)
- DDL (CREATE TABLE, ALTER, DROP, data types, constraints)
- JOINs (INNER, LEFT, RIGHT, FULL) with visual examples
- Normalization (1NF, 2NF, 3NF) with before/after examples
- Indexes and performance
- Transactions and ACID properties
- Schema design best practices

## Response Format
- Keep responses focused and not too long
- Use markdown formatting for code blocks and tables
- If showing SQL, always explain what each part does
- End complex explanations with a quick comprehension check question

Remember: You're helping students who are completely new to databases. Be encouraging!"""

    # Print welcome banner
    console.print()
    console.print(Panel(
        "[bold cyan]📚 Database Teaching Mode[/bold cyan]\n\n"
        "I'm your AI tutor for learning relational databases!\n"
        "Ask me anything about:\n"
        "• Database concepts & terminology\n"
        "• ERD and schema design\n"
        "• SQL syntax (DDL, DML, queries)\n"
        "• Normalization (1NF, 2NF, 3NF)\n"
        "• JOINs, indexes, transactions\n\n"
        "[dim]Type 'quit' or 'exit' to end the session.[/dim]",
        title="🎓 Teaching Mode",
        border_style="cyan",
    ))
    console.print()

    # Initialize conversation history
    messages = [SystemMessage(content=system_prompt)]

    # If topic provided, ask about it
    if topic:
        console.print(f"[bold cyan]You:[/bold cyan] {topic}")
        messages.append(HumanMessage(content=topic))
        with console.status("[cyan]Thinking...[/cyan]", spinner="dots"):
            response = llm.invoke(messages)
        messages.append(AIMessage(content=response.content))
        console.print()
        console.print(Panel(
            Markdown(response.content),
            title="[bold green]Tutor[/bold green]",
            border_style="green",
            padding=(1, 2),
        ))
        console.print()

    # Interactive loop
    while True:
        try:
            user_input = Prompt.ask("[bold cyan]You[/bold cyan]")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[muted]Happy learning! 📚[/muted]")
            break

        if not user_input.strip():
            continue

        if user_input.strip().lower() in {"quit", "exit", "q"}:
            console.print("[muted]Happy learning! 📚[/muted]")
            break

        # Add to conversation and get response
        messages.append(HumanMessage(content=user_input))
        
        with console.status("[cyan]Thinking...[/cyan]", spinner="dots"):
            response = llm.invoke(messages)
        
        messages.append(AIMessage(content=response.content))
        
        console.print()
        console.print(Panel(
            Markdown(response.content),
            title="[bold green]Tutor[/bold green]",
            border_style="green",
            padding=(1, 2),
        ))
        console.print()


@app.command()
def chat(
    config: Annotated[
        str | None,
        typer.Option(
            "--config",
            "-c",
            help="Configuration to use (default: load all configs)",
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose/--quiet", "-v/-q", help="Show query state (agent, SQL)"
        ),
    ] = False,
    log_level: Annotated[
        str | None,
        typer.Option(
            "--log-level",
            "-l",
            help="Logging level (debug, info, warning, error)",
        ),
    ] = None,
) -> None:
    """Start interactive chat mode.

    Opens a REPL-style interface for asking multiple questions
    in a continuous session. Type 'quit' or 'exit' to end.
    """
    if log_level:
        setup_logging(LOG_LEVELS.get(log_level.lower(), logging.INFO))
    agent_config, config_name = load_config(config)
    endpoint, api_key, deployment = get_azure_credentials()

    async def _run() -> None:
        async with DataAgentFlow(
            config=agent_config,
            azure_endpoint=endpoint,
            api_key=api_key,
            deployment_name=deployment,
        ) as flow:
            agents = [
                {"name": agent.name, "description": agent.description}
                for agent in flow.config.data_agents
            ]
            print_dashboard(config_name, agents)

            console.print("[muted]Type 'quit' or 'exit' to end the session.[/muted]")
            console.print()

            thread_id = uuid4().hex

            while True:
                try:
                    user_input = Prompt.ask("[bold cyan]You[/bold cyan]")
                except (KeyboardInterrupt, EOFError):
                    console.print("\n[muted]Goodbye![/muted]")
                    break

                if not user_input.strip():
                    continue

                if user_input.strip().lower() in {"quit", "exit", "q"}:
                    console.print("[muted]Goodbye![/muted]")
                    break

                result, final_question = await execute_query(
                    flow, user_input, thread_id
                )
                display_result(result, final_question, verbose)
                console.print()

    asyncio.run(_run())


@app.command()
def configs() -> None:
    """List available configurations.

    Displays a table of all .yaml configuration files found
    in the config directory.
    """
    from rich.table import Table

    table = Table(title="Available Configurations", show_header=True)
    table.add_column("Name", style="cyan")
    table.add_column("Path", style="dim")

    for config_file in sorted(CONFIG_DIR.glob("*.yaml")):
        table.add_row(config_file.stem, str(config_file))

    console.print(table)


@app.command()
def validate(
    config: Annotated[
        str | None,
        typer.Option(
            "--config",
            "-c",
            help="Configuration name to validate (validates all if not specified)",
        ),
    ] = None,
) -> None:
    """Validate configuration files against the JSON schema.

    Checks that the YAML configuration follows the expected structure
    and reports any validation errors.
    """
    import yaml

    from data_agent.config_loader import ConfigLoader

    configs_to_validate = []
    if config:
        config_path = validate_config(config)
        configs_to_validate = [(config, config_path)]
    else:
        configs_to_validate = [(f.stem, f) for f in sorted(CONFIG_DIR.glob("*.yaml"))]

    has_errors = False
    for name, path in configs_to_validate:
        with path.open(encoding="utf-8") as f:
            raw = yaml.safe_load(f)

        errors = ConfigLoader.validate(raw)

        if errors:
            has_errors = True
            console.print(f"[red]✗[/red] {name}")
            for err in errors:
                console.print(f"  [red]•[/red] {err}")
        else:
            console.print(f"[green]✓[/green] {name}")

    if has_errors:
        raise typer.Exit(1)


@app.command()
def a2a(
    config: Annotated[
        str | None,
        typer.Option(
            "--config",
            "-c",
            help="Configuration name to use (from src/data_agent/config/). Loads all if not specified.",
        ),
    ] = None,
    host: Annotated[
        str,
        typer.Option(
            "--host",
            help="Server bind host.",
        ),
    ] = "localhost",
    port: Annotated[
        int,
        typer.Option(
            "--port",
            "-p",
            help="Server bind port.",
        ),
    ] = 8001,
    log_level: Annotated[
        str,
        typer.Option(
            "--log-level",
            help="Logging level.",
        ),
    ] = "info",
) -> None:
    """Start the A2A (Agent-to-Agent) protocol server.

    This exposes the NL2SQL Data Agent via the Google A2A protocol,
    enabling interoperability with other A2A-compliant agents.

    The agent card describing capabilities is available at:
    http://<host>:<port>/.well-known/agent-card.json

    Examples:
        # Start with all configs (default)
        data-agent a2a

        # Start with a specific config
        data-agent a2a --config contoso

        # Start on a custom port with debug logging
        data-agent a2a --port 9000 --log-level debug
    """
    from data_agent.a2a import run_server

    if config:
        validate_config(config)

    console.print("[cyan]Starting A2A server...[/cyan]")
    console.print(f"  Host: [green]{host}[/green]")
    console.print(f"  Port: [green]{port}[/green]")
    console.print(f"  Config: [green]{config or 'all'}[/green]")
    console.print(
        f"  Agent Card: [link=http://{host}:{port}/.well-known/agent-card.json]http://{host}:{port}/.well-known/agent-card.json[/link]"
    )
    console.print()

    run_server(
        config_name=config,
        host=host,
        port=port,
        log_level=log_level,
    )


if __name__ == "__main__":
    app()
