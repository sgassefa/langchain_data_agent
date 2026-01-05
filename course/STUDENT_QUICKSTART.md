# 🎓 Student Quick Start Guide

Welcome to the NL2SQL Data Agent course! This guide will get you up and running in under 5 minutes.

---

## 🔑 Understanding Credentials

This course uses **two types of credentials** for different purposes:

| Credential | Purpose | When Needed |
|------------|---------|-------------|
| **GitHub Token** | Powers the AI that generates SQL from your questions | Always (for NL2SQL agent) |
| **Database Credentials** | Connects to cloud databases where data lives | Only for MySQL, PostgreSQL, Azure SQL |

```
Your Question → [GitHub Token/AI] → Generates SQL → [Database Credentials] → Runs Query → Results
```

**Good news:** The **University database (SQLite)** requires NO database credentials - it's a local file!

---

## 🚀 Option 1: GitHub Codespaces (Recommended - Zero Install)

### Step 1: Open in Codespaces (Browser-Based)
1. Go to the course repository on GitHub
2. Click the green **"Code"** button
3. Select **"Codespaces"** tab
4. Click **"Create codespace on main"**
5. Wait ~2 minutes for the environment to build

> **💡 Tip: Open in Browser, Not VS Code**
> 
> By default, Codespaces may open in VS Code Desktop. To use the browser instead:
> 1. Go to [github.com/settings/codespaces](https://github.com/settings/codespaces)
> 2. Under **"Editor preference"**, select **"Visual Studio Code for the Web"**
> 3. Save changes
> 
> Or, when clicking on an existing Codespace, look for **"Open in Browser"** option.

### Step 2: Get Your GitHub Token (FREE!)
GitHub Models is **free** for all GitHub users! You just need a Personal Access Token:

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens?type=beta)
2. Click **"Generate new token"** → **"Fine-grained token"**
3. Give it a name like "NL2SQL Course"
4. Under **"Permissions"**, find **"Models"** and set to **"Read"**
5. Click **"Generate token"**
6. Copy the token (starts with `github_pat_...`)

### Step 3: Configure Your Environment
1. Open the `.env` file in the file explorer
2. Add your GitHub token:
   ```
   GITHUB_TOKEN=github_pat_your-token-here
   ```
3. Save the file (Ctrl+S / Cmd+S)

### Step 4: Test Your Setup
Open the terminal (Ctrl+` or View → Terminal) and run:

```bash
uv run data-agent query "What courses does Srinivasan teach?" -c university
```

You should see a response with courses and the generated SQL! 🎉

### 🔄 Updating an Existing Codespace

If you created your Codespace before updates were made to the repository, run these commands to get the latest code:

```bash
# Pull the latest code
git pull origin main

# Reinstall the package with new features
uv sync

# Verify the teach command is available
uv run data-agent --help
```

You should see `teach` in the list of available commands.

---

## 📖 Learning Mode: `teach` Command

Before diving into SQL queries, use the **teach** command to learn database fundamentals:

```bash
# Start an interactive tutoring session
uv run data-agent teach

# Or ask a specific question
uv run data-agent teach "What is a primary key?"
uv run data-agent teach "Explain 1NF, 2NF, and 3NF with examples"
```

The AI tutor will help you understand:
- Database fundamentals and terminology
- Entity-Relationship Diagrams (ERD)
- Primary keys, foreign keys, and relationships
- Normalization (1NF, 2NF, 3NF)
- SQL syntax and commands
- Schema design best practices

**No database connection required** - perfect for learning concepts first!

---

## 💻 Option 2: Local Setup (VS Code + Docker)

### Prerequisites
- [VS Code](https://code.visualstudio.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Steps
1. Clone the repository
2. Open in VS Code
3. Click **"Reopen in Container"** when prompted
4. Edit `.env` with your GitHub token
5. Run test queries

---

## 📚 Available Databases

| Config | Database | Credentials Needed | Description |
|--------|----------|-------------------|-------------|
| `university` | SQLite | ❌ None | Academic database - **Start here!** |
| `chinook` | MySQL | ✅ Student credentials | Digital media store |
| `pagila` | PostgreSQL | ✅ Student credentials | DVD rental store |
| `contoso_hr` | Azure SQL | ✅ Student credentials | HR management |

### 🎓 For Weeks 1-4: Use University Database Only
The **University** database (SQLite) requires no additional setup - perfect for learning SQL basics!

### 🔐 For Weeks 5+: Cloud Database Access
Your instructor will provide individual credentials for cloud databases:

| Database | Your Username | Your Password |
|----------|--------------|---------------|
| MySQL (Chinook) | `studentXX` | *(provided in class)* |
| PostgreSQL (Pagila) | `studentXX` | *(provided in class)* |
| Azure SQL (ContosoHR) | `studentXX` | *(provided in class)* |

Add these to your `.env` file when needed:
```bash
# MySQL (Chinook)
MYSQL_USER=studentXX
MYSQL_PASSWORD=your-password-here

# PostgreSQL (Pagila)  
POSTGRES_USER=studentXX
POSTGRES_PASSWORD=your-password-here

# Azure SQL (ContosoHR)
AZURE_SQL_USER=studentXX
AZURE_SQL_PASSWORD=your-password-here
```

---

## 🔍 Example Queries to Try

### University Database (`-c university`)

**Basic Queries:**
```bash
uv run data-agent query "List all departments" -c university
uv run data-agent query "How many students are enrolled?" -c university
uv run data-agent query "Show all instructors in the Computer Science department" -c university
```

**Joins & Relationships:**
```bash
uv run data-agent query "What courses does Srinivasan teach?" -c university
uv run data-agent query "List students with A grades in Computer Science" -c university
uv run data-agent query "Which instructors teach in Spring 2025?" -c university
```

**Prerequisites & Complex Queries:**
```bash
uv run data-agent query "What are the prerequisites for CS-315?" -c university
uv run data-agent query "Find students who have taken more than 3 courses" -c university
uv run data-agent query "What is the average salary by department?" -c university
```

---

## 🗄️ University Database Schema

The University database contains these tables:

| Table | Description |
|-------|-------------|
| `department` | Academic departments (name, building, budget) |
| `instructor` | Faculty members (name, department, salary) |
| `student` | Students (name, department, total credits) |
| `course` | Course catalog (title, department, credits) |
| `section` | Course sections (semester, year, room, time) |
| `teaches` | Instructor-section assignments |
| `takes` | Student enrollments with grades |
| `advisor` | Student-advisor relationships |
| `prereq` | Course prerequisites |
| `classroom` | Building rooms and capacity |
| `time_slot` | Class time schedules |

---

## 🛠️ Troubleshooting

### "Command 'teach' not recognized"
Your Codespace may have older code. Update it:
```bash
git pull origin main
uv sync
```

### "Invalid API key" or "Authentication failed" (GitHub Token)
- Verify your GitHub token is correct in `.env`
- Make sure there are no extra spaces or quotes
- Check that your token has **"Models: Read"** permission
- Try generating a new token

### Using OpenAI Instead of GitHub Models
If you see "OpenAI" in error messages when you expected GitHub Models:
1. Make sure `GITHUB_TOKEN` is set in your `.env` (not just `OPENAI_API_KEY`)
2. The `GITHUB_TOKEN` line should come **before** `OPENAI_API_KEY` in `.env`
3. Example correct `.env`:
   ```
   GITHUB_TOKEN=github_pat_your-token-here
   # OPENAI_API_KEY=sk-...  # Comment this out
   ```

### "Connection refused" or "Access denied" (Database)
- Verify your database credentials are correct
- Check you're using the right username/password for your student number
- Ensure the database server is accessible (ask instructor if unsure)

### "Module not found" Error
Run: `uv sync` to reinstall dependencies

### Query Returns Wrong Results
- Try rephrasing your question
- Be specific with names (e.g., "Srinivasan" not "the CS instructor")
- Check the generated SQL to understand what was queried

### Codespace Opens in VS Code Desktop Instead of Browser
1. Go to [github.com/settings/codespaces](https://github.com/settings/codespaces)
2. Under "Editor preference", select "Visual Studio Code for the Web"
3. Save changes

### Need Help?
- Check the course Slack/Discord channel
- Raise your hand in class
- Open an issue on GitHub

---

## 📖 Next Steps

1. Complete the lab exercises in [LAB_EXERCISES.md](LAB_EXERCISES.md)
2. Explore the database schema with SQLite viewer
3. Try writing your own natural language queries
4. Examine the generated SQL to learn SQL syntax

Happy querying! 🎉
