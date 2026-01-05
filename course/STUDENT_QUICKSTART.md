# 🎓 Student Quick Start Guide

Welcome to the NL2SQL Data Agent course! This guide will get you up and running in under 5 minutes.

## 🚀 Option 1: GitHub Codespaces (Recommended - Zero Install)

### Step 1: Open in Codespaces
1. Go to the course repository on GitHub
2. Click the green **"Code"** button
3. Select **"Codespaces"** tab
4. Click **"Create codespace on main"**
5. Wait ~2 minutes for the environment to build

### Step 2: Add Your API Key
1. Open the `.env` file in the file explorer
2. Add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   ```
3. Save the file (Ctrl+S / Cmd+S)

> 💡 **Don't have an OpenAI API key?** 
> - Sign up at [platform.openai.com](https://platform.openai.com)
> - Go to API Keys → Create new secret key
> - Add $5-10 credit (queries cost ~$0.01 each)

### Step 3: Test Your Setup
Open the terminal (Ctrl+` or View → Terminal) and run:

```bash
uv run data-agent query "What courses does Srinivasan teach?" -c university
```

You should see a response with courses and the generated SQL! 🎉

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
4. Edit `.env` with your API key
5. Run test queries

---

## 📚 Available Databases

| Config | Database | Description |
|--------|----------|-------------|
| `university` | SQLite | Academic database with courses, students, instructors |
| `chinook` | MySQL | Digital media store (requires MySQL setup) |
| `pagila` | PostgreSQL | DVD rental store (requires PostgreSQL setup) |

For this course, we'll primarily use the **University** database (SQLite) as it requires no additional setup.

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

### "Invalid API key" Error
- Verify your API key is correct in `.env`
- Make sure there are no extra spaces or quotes
- Ensure you have credits in your OpenAI account

### "Module not found" Error
Run: `uv sync` to reinstall dependencies

### Query Returns Wrong Results
- Try rephrasing your question
- Be specific with names (e.g., "Srinivasan" not "the CS instructor")
- Check the generated SQL to understand what was queried

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
