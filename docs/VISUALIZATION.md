# Data Visualization

This guide covers the code interpreter feature for generating charts and visualizations from query results.

## Overview

When enabled, the data agent can detect visualization intent in user queries (e.g., "show me a chart", "plot the data") and generate matplotlib code to create charts. The code runs in a secure, isolated environment using Azure Container Apps Dynamic Sessions.

**Key features:**
- Automatic detection of visualization requests
- LLM-generated matplotlib code
- Secure sandboxed execution with Hyper-V isolation
- Native image capture (no file storage)
- Support for bar charts, line charts, pie charts, scatter plots, and more

## Requirements

Visualization requires Azure Container Apps Dynamic Sessions. This provides:

| Feature | Benefit |
|---------|---------|
| **Hyper-V isolation** | Each execution runs in a dedicated VM |
| **Pre-installed packages** | NumPy, Pandas, Matplotlib ready to use |
| **Native image capture** | `plt.show()` output captured automatically |
| **Automatic cleanup** | Sessions terminate after idle timeout |
| **No host access** | Code cannot access host filesystem or network |

## Azure Setup

### 1. Create a Container Apps Environment

If you don't already have one:

```bash
az containerapp env create \
    --name aca-env \
    --resource-group rg-data-agent \
    --location eastus
```

### 2. Create the Session Pool

```bash
az containerapp sessionpool create \
    --name session-pool-viz \
    --resource-group rg-data-agent \
    --container-type PythonLTS \
    --max-sessions 100 \
    --cooldown-period 300 \
    --location eastus
```

**Parameters:**
- `--container-type PythonLTS`: Python runtime with common data science packages
- `--max-sessions`: Maximum concurrent sessions
- `--cooldown-period`: Seconds before idle session is terminated

### 3. Get the Pool Management Endpoint

```bash
az containerapp sessionpool show \
    --name session-pool-viz \
    --resource-group rg-data-agent \
    --query "properties.poolManagementEndpoint" -o tsv
```

This returns a URL like:
```
https://eastus.dynamicsessions.io/subscriptions/<sub>/resourceGroups/<rg>/sessionPools/<pool>
```

### 4. Assign the Executor Role

Grant your identity permission to execute code in the session pool:

```bash
# Get your user ID
USER_ID=$(az ad signed-in-user show --query id -o tsv)

# Get the session pool resource ID
POOL_ID=$(az containerapp sessionpool show \
    --name session-pool-viz \
    --resource-group rg-data-agent \
    --query id -o tsv)

# Assign the role
az role assignment create \
    --role "Azure ContainerApps Session Executor" \
    --assignee $USER_ID \
    --scope $POOL_ID
```

**Note:** For service principals or managed identities, replace `$USER_ID` with the appropriate object ID.

### 5. Install the SDK

```bash
pip install langchain-azure-dynamic-sessions
```

Or add to your `pyproject.toml`:
```toml
dependencies = [
    "langchain-azure-dynamic-sessions>=0.1.0",
]
```

## Configuration

### Environment Variable

Set the pool endpoint:

```bash
export AZURE_SESSIONS_POOL_ENDPOINT="https://eastus.dynamicsessions.io/subscriptions/.../sessionPools/..."
```

Or in `.env`:
```bash
AZURE_SESSIONS_POOL_ENDPOINT=https://eastus.dynamicsessions.io/subscriptions/.../sessionPools/...
```

### YAML Configuration

Enable visualization in your agent config:

```yaml
data_agents:
  - name: "sales_agent"
    # ... other config ...
    code_interpreter:
      enabled: true
      azure_sessions_endpoint: ${AZURE_SESSIONS_POOL_ENDPOINT}
```

| Setting | Description | Default |
|---------|-------------|---------|
| `enabled` | Enable/disable visualization | `false` |
| `azure_sessions_endpoint` | Session pool management endpoint URL | - |

### System Prompt

To enable visualization detection, include `visualization_requested` in your response format:

```yaml
system_prompt: |
  You are a SQL expert for the sales database.

  {schema_context}

  ## Response Format

  Provide your response as JSON with these fields:
  - "thinking": Step-by-step reasoning about the query
  - "sql_query": The generated SQL query
  - "explanation": Brief explanation of what the query does
  - "visualization_requested": Set to true if the user asks for a chart, graph, plot, or visualization
```

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Query                                │
│            "Show me a bar chart of sales by region"             │
└─────────────────────────────────────────┬───────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SQL Generation LLM                          │
│  Generates SQL + sets visualization_requested: true              │
└─────────────────────────────────────────┬───────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Database Query                               │
│              Execute SQL, return result rows                     │
└─────────────────────────────────────────┬───────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Visualization LLM                              │
│    Generates matplotlib code based on data + user question       │
└─────────────────────────────────────────┬───────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────┐
│              Azure Container Apps Dynamic Sessions               │
│   • Code executed in Hyper-V isolated container                 │
│   • plt.show() output captured automatically                    │
│   • Image returned as base64 PNG                                │
└─────────────────────────────────────────┬───────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Response                                    │
│         Text explanation + embedded chart image                  │
└─────────────────────────────────────────────────────────────────┘
```

### Execution Flow

1. **Intent Detection**: The SQL LLM sets `visualization_requested: true` when it detects chart/graph/plot intent
2. **SQL Execution**: Query runs against the database, returning structured data
3. **Code Generation**: A second LLM call generates matplotlib code tailored to the data and question
4. **Sandboxed Execution**: Code runs in Azure Sessions with automatic image capture
5. **Response Assembly**: Text response and chart image are combined for display

## Example Queries

These prompts trigger visualization:

| Query | Chart Type |
|-------|------------|
| "Show me a bar chart of sales by region" | Bar chart |
| "Visualize the top 10 customers by revenue" | Horizontal bar |
| "Plot monthly revenue trends for 2024" | Line chart |
| "Create a pie chart of transaction types" | Pie chart |
| "Graph the distribution of order values" | Histogram |
| "Compare Q1 vs Q2 performance" | Grouped bar |

## Further Reading

- [Azure Container Apps Dynamic Sessions](https://learn.microsoft.com/azure/container-apps/sessions)
- [Session Pool Management](https://learn.microsoft.com/azure/container-apps/sessions-code-interpreter)
- [LangChain Azure Dynamic Sessions](https://python.langchain.com/docs/integrations/tools/azure_dynamic_sessions)
