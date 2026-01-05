# LIS 4230: Relational Database Management Systems
## Graduate-Level Course - 10 Weeks

**Course Description:** This course teaches relational database concepts through the lens of Natural Language to SQL (NL2SQL) AI agents. Students will learn SQL fundamentals, schema design, query optimization, and ultimately build AI-powered database agents using LangGraph.

---

## 🗄️ Course Databases

| Database | Platform | Domain | Purpose |
|----------|----------|--------|---------|
| **ContosoHR** | Azure SQL | HR Management | Primary learning database (Weeks 1-6) |
| **Chinook** | MySQL | Music Store | Cross-platform comparison (Weeks 5-8) |
| **Pagila** | PostgreSQL | DVD Rental | Advanced queries & optimization (Weeks 6-10) |

---

## 📅 Weekly Schedule

### Module 1-2: SQL Fundamentals (Weeks 1-4)
*"What the AI agent generates"*

#### Week 1: Introduction to RDBMS & Basic SELECT
**Database:** ContosoHR (Azure SQL)

**Topics:**
- Course overview & NL2SQL demonstration
- Relational model concepts (tables, rows, columns)
- Basic SELECT statements
- WHERE clause filtering
- Sorting with ORDER BY

**Lab Exercises:**
```sql
-- Students write queries, then test with NL2SQL agent
"List all employees in the Engineering department"
"Show me employees hired after 2024"
"Who are the highest paid employees?"
```

**Assignment:** Query 10 natural language questions, compare AI-generated SQL with hand-written SQL

---

#### Week 2: Data Types, Functions & Aggregations
**Database:** ContosoHR (Azure SQL)

**Topics:**
- SQL data types (INT, VARCHAR, DATE, DECIMAL, BIT)
- Built-in functions (string, date, numeric)
- Aggregate functions (COUNT, SUM, AVG, MIN, MAX)
- GROUP BY and HAVING clauses

**Lab Exercises:**
```sql
"What is the average salary by department?"
"How many employees were hired each year?"
"Which departments have more than 5 employees?"
```

**Assignment:** Create a salary analysis report using aggregations

---

#### Week 3: JOINs and Table Relationships
**Database:** ContosoHR (Azure SQL)

**Topics:**
- Primary keys and foreign keys
- INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN
- Self-joins (employee-manager relationships)
- Multi-table queries

**Lab Exercises:**
```sql
"List employees with their department names"
"Show each employee with their manager's name"
"Find departments with no employees"
```

**Assignment:** ER diagram of ContosoHR + complex JOIN queries

---

#### Week 4: Subqueries and Set Operations
**Database:** ContosoHR (Azure SQL)

**Topics:**
- Scalar subqueries
- Correlated subqueries
- EXISTS and NOT EXISTS
- UNION, INTERSECT, EXCEPT
- Common Table Expressions (CTEs)

**Lab Exercises:**
```sql
"Find employees who earn more than their department average"
"List departments where all employees have performance ratings above 3"
"Show the top performer in each department"
```

**Assignment:** Rewrite subqueries as JOINs and compare execution plans

---

### Module 3-4: Schema Design (Weeks 5-6)
*"Table relationships the agent understands"*

#### Week 5: Database Design Principles
**Databases:** ContosoHR (Azure SQL) + Chinook (MySQL)

**Topics:**
- Entity-Relationship modeling
- Normalization (1NF, 2NF, 3NF, BCNF)
- Denormalization trade-offs
- Schema documentation for AI agents

**Lab Exercises:**
- Compare ContosoHR schema (HR domain) with Chinook schema (music store)
- Identify normalization levels in both databases
- Design schema metadata for NL2SQL prompts

**Assignment:** Design a new database schema and write its AI agent configuration

---

#### Week 6: Cross-Platform SQL & Constraints
**Databases:** ContosoHR (Azure SQL) + Chinook (MySQL) + Pagila (PostgreSQL)

**Topics:**
- SQL dialect differences (T-SQL, MySQL, PostgreSQL)
- Constraints (PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK)
- Indexes and their impact on queries
- Data integrity enforcement

**Lab Exercises:**
```sql
-- Same query, three platforms:
"Show top 10 customers by total purchases"
-- Compare: TOP vs LIMIT vs LIMIT/OFFSET
```

**Assignment:** Port 10 queries across all three database platforms

---

### Module 5-6: Query Optimization (Weeks 7-8)
*"How to write efficient SQL"*

#### Week 7: Query Execution Plans
**Database:** Pagila (PostgreSQL)

**Topics:**
- EXPLAIN and EXPLAIN ANALYZE
- Reading execution plans
- Table scans vs index scans
- Cost estimation

**Lab Exercises:**
- Analyze execution plans for various queries
- Identify bottlenecks in slow queries
- Compare costs of different query approaches

**Assignment:** Optimize 5 slow queries with documented improvements

---

#### Week 8: Indexing Strategies
**Databases:** All three platforms

**Topics:**
- B-tree indexes
- Composite indexes
- Covering indexes
- When NOT to use indexes
- Index maintenance

**Lab Exercises:**
- Create indexes and measure query improvements
- Analyze index usage statistics
- Balance read vs write performance

**Assignment:** Design indexing strategy for a high-traffic application

---

### Module 7-8: LLM + SQL Integration (Weeks 9)
*"Prompt engineering for databases"*

#### Week 9: Prompt Engineering for NL2SQL
**Databases:** All three platforms

**Topics:**
- How LLMs understand database schemas
- Few-shot prompting with SQL examples
- Schema representation strategies
- Handling ambiguous queries
- Error correction and retry logic

**Lab Exercises:**
- Modify agent prompts and observe output changes
- Add few-shot examples for complex queries
- Handle edge cases (typos, ambiguous column names)

**Assignment:** Write and test prompts for a new database domain

---

### Module 9-10: Building Agents with LangGraph (Week 10)
*"Orchestrating intelligent database assistants"*

#### Week 10: LangGraph Agent Architecture
**Databases:** All three platforms

**Topics:**
- LangGraph concepts (nodes, edges, state)
- Multi-agent architectures
- Intent detection and routing
- Error handling and retries
- Production considerations

**Lab Exercises:**
- Trace through the NL2SQL agent code
- Add a new data agent for Pagila
- Implement query validation node

**Final Project:** Build a multi-database NL2SQL agent that routes queries to the appropriate database based on the domain

---

## 📊 Grading Structure

| Component | Weight | Description |
|-----------|--------|-------------|
| Weekly Labs | 30% | Hands-on SQL exercises |
| Assignments | 30% | Take-home projects |
| Midterm Exam | 15% | Weeks 1-5 material (SQL fundamentals) |
| Final Project | 25% | Multi-database NL2SQL agent |

---

## 🛠️ Technical Setup

### Required Software
- VS Code with SQL extensions
- Python 3.11+ with uv package manager
- ODBC Driver 18 for SQL Server
- MySQL Workbench
- pgAdmin or DBeaver for PostgreSQL

### Database Access
| Database | Connection |
|----------|------------|
| ContosoHR | `lis-4230.database.windows.net` (Azure SQL) |
| Chinook | Local MySQL or Azure MySQL |
| Pagila | Local PostgreSQL or Azure PostgreSQL |

### Student Credentials
- Azure SQL: student01-student10 / Go4RDBMS#01! - Go4RDBMS#10!
- MySQL/PostgreSQL: Set up locally or provided cloud instances

---

## 📚 Recommended Resources

### Books
- "Learning SQL" by Alan Beaulieu
- "SQL Performance Explained" by Markus Winand
- "Designing Data-Intensive Applications" by Martin Kleppmann

### Online
- https://use-the-index-luke.com/ (Query optimization)
- https://pgexercises.com/ (PostgreSQL practice)
- https://langchain-ai.github.io/langgraph/ (LangGraph docs)

---

## 🎯 Learning Outcomes

By the end of this course, students will be able to:

1. **Write proficient SQL** across multiple database platforms
2. **Design normalized schemas** with proper constraints and relationships
3. **Optimize query performance** using indexes and execution plan analysis
4. **Engineer effective prompts** for LLM-based database assistants
5. **Build intelligent agents** using LangGraph for database interactions
6. **Compare and contrast** SQL dialects across Azure SQL, MySQL, and PostgreSQL
