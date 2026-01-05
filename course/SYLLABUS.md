# LIS 4230: Relational Database Management Systems
## Graduate-Level Course - 10 Weeks

**Course Description:** This course provides a comprehensive introduction to relational database management systems. Students learn database fundamentals, SQL programming, schema design, and query optimization through hands-on exercises. A Natural Language to SQL (NL2SQL) AI agent is woven throughout the course as a learning tool, allowing students to explore SQL generation, validate their queries, and understand how modern AI interacts with databases.

---

## 📊 Grading Structure

| Component | Weight | Description |
|-----------|--------|-------------|
| **Assignment 1** | 15% | Foundations & Data Modeling (Due: Week 2) |
| **Assignment 2** | 15% | Schema Design & Setup (Due: Week 4) |
| **Assignment 3** | 15% | Data Manipulation & Querying (Due: Week 6) |
| **Assignment 4** | 15% | Advanced Design & Optimization (Due: Week 8) |
| **Mid-Course Project** | 20% | Small Complete Database - Library System (Due: Week 5) |
| **Final Project** | 20% | Full-Featured Database with Presentation (Due: Week 10) |

---

## 🗄️ Course Databases

| Database | Platform | Domain | Purpose |
|----------|----------|--------|---------|
| **University** | SQLite | Academic | Quick demos, zero-setup learning |
| **ContosoHR** | Azure SQL | HR Management | Enterprise database patterns |
| **Chinook** | MySQL | Music Store | Cross-platform comparison |
| **Pagila** | PostgreSQL | DVD Rental | Advanced queries & optimization |

---

## 📅 Weekly Schedule

### Week 1: Introduction to Databases
*"Understanding the landscape"*

**Topics:**
- Course overview & NL2SQL agent demonstration
- What is a database? Why do we need them?
- Types of databases (Relational, NoSQL, Graph, Time-series)
- RDBMS terminology (tables, rows, columns, records, fields)
- Database management systems overview

**Tools:**
- 🛠️ **DB Browser for SQLite** - Visual database exploration
- 🛠️ **Command Line** - Quick intro to sqlite3 CLI
- 🤖 **NL2SQL Agent** - First demo with University database

**Lab Exercises:**
```bash
# Demo: Ask questions in natural language
uv run data-agent query "How many students are enrolled?" -c university
uv run data-agent query "List all departments" -c university
```

**Readings:**
- Course textbook Chapter 1: Introduction to Databases
- [SQLite Tutorial](https://www.sqlitetutorial.net/)

---

### Week 2: The Relational Model
*"Designing data relationships"*

**Topics:**
- Entities, attributes, and relationships
- Entity-Relationship Diagrams (ERD)
- Keys: Primary, Foreign, Candidate, Composite
- Cardinality (1:1, 1:N, M:N)
- Translating business requirements to data models

**Tools:**
- 🛠️ **MySQL Workbench** - ER diagram creation
- 🛠️ **draw.io** - Free diagramming tool
- 🛠️ **dbdiagram.io** - Code-based ERD design

**Lab Exercises:**
- Draw ERD for a simple library system
- Identify entities and relationships in Chinook database
- Reverse-engineer University database schema

**📝 Assignment 1 Due: Foundations & Data Modeling (15%)**
> Design an ERD for a given business scenario. Identify entities, attributes, relationships, and keys. Submit diagram + written explanation.

---

### Week 3: Setting Up Databases
*"From installation to first data"*

**Topics:**
- Installing database systems (SQLite, MySQL, PostgreSQL)
- Creating databases and schemas
- Importing existing data (CSV, SQL dumps)
- Database connection strings
- GUI tools vs command line

**Tools:**
- 🛠️ **SQLite** - File-based, zero-config
- 🛠️ **MySQL Workbench** - Full IDE experience
- 🛠️ **pgAdmin / DBeaver** - PostgreSQL management

**Lab Exercises:**
```sql
-- Create a new database
CREATE DATABASE library_db;

-- Import the University sample data
-- Use DB Browser for SQLite to explore data/university.db
```

**Hands-on:**
- Set up local MySQL instance
- Import Chinook database from SQL dump
- Connect NL2SQL agent to your local database

---

### Week 4: SQL Basics - Data Definition Language (DDL)
*"Building the structure"*

**Topics:**
- CREATE TABLE syntax
- Data types across platforms (INT, VARCHAR, DATE, DECIMAL, BOOLEAN)
- ALTER TABLE (ADD, MODIFY, DROP columns)
- DROP TABLE, TRUNCATE
- Constraints: NOT NULL, UNIQUE, DEFAULT, CHECK
- Primary and Foreign Key constraints

**Lab Exercises:**
```sql
-- Create tables with proper constraints
CREATE TABLE books (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    isbn VARCHAR(13) UNIQUE,
    published_date DATE,
    price DECIMAL(10,2) CHECK (price >= 0)
);

CREATE TABLE authors (
    author_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    birth_year INT CHECK (birth_year > 1800)
);
```

**📝 Assignment 2 Due: Schema Design & Setup (15%)**
> Create a complete database schema for your mid-course project (Library System). Include at least 5 tables with proper constraints, keys, and relationships. Submit DDL scripts + ERD.

---

### Week 5: SQL - Data Manipulation Language (DML)
*"Working with data"*

**Topics:**
- INSERT statements (single row, multiple rows, from SELECT)
- UPDATE with WHERE clause
- DELETE vs TRUNCATE
- Transaction basics (BEGIN, COMMIT, ROLLBACK)
- Data integrity and referential actions

**Lab Exercises:**
```sql
-- Insert sample data
INSERT INTO books (title, isbn, price) VALUES
    ('Database Systems', '978-0132943', 89.99),
    ('SQL Fundamentals', '978-0134685', 49.99);

-- Update with conditions
UPDATE books SET price = price * 0.9 WHERE published_date < '2020-01-01';

-- Safe delete with transaction
BEGIN TRANSACTION;
DELETE FROM books WHERE book_id = 5;
-- Check results before committing
ROLLBACK; -- or COMMIT;
```

**🏆 Mid-Course Project Due: Library Database (20%)**
> Submit a complete Library Management database with:
> - Minimum 5 tables (books, members, loans, authors, categories)
> - Sample data (at least 10 records per table)
> - DDL + DML scripts
> - ERD diagram
> - 5 sample queries demonstrating your schema

---

### Week 6: Queries and Aggregations
*"Extracting insights from data"*

**Topics:**
- SELECT statement deep dive
- WHERE clause operators (=, <>, LIKE, IN, BETWEEN, IS NULL)
- Sorting with ORDER BY (ASC, DESC, multiple columns)
- Aggregate functions: COUNT, SUM, AVG, MIN, MAX
- GROUP BY for categorization
- HAVING for filtering groups
- DISTINCT and LIMIT/TOP

**Lab Exercises:**
```sql
-- NL2SQL comparison exercises
"What is the average salary by department?"
"How many courses are offered in each department?"
"Which departments have a budget over $100,000?"

-- Hand-write SQL, then compare with agent output
SELECT dept_name, AVG(salary) as avg_salary
FROM instructor
GROUP BY dept_name
HAVING AVG(salary) > 70000
ORDER BY avg_salary DESC;
```

**📝 Assignment 3 Due: Data Manipulation & Querying (15%)**
> Write 15 queries of increasing complexity against the Chinook database:
> - 5 basic SELECT with filtering/sorting
> - 5 aggregate queries with GROUP BY/HAVING
> - 5 queries combining multiple concepts
> Include NL2SQL agent output comparison for each query.

---

### Week 7: JOINs and Subqueries
*"Connecting related data"*

**Topics:**
- Understanding table relationships in queries
- INNER JOIN - matching rows only
- LEFT/RIGHT OUTER JOIN - including unmatched rows
- FULL OUTER JOIN - all rows from both tables
- Self-joins (employee-manager, prerequisite chains)
- Subqueries: scalar, column, table
- Correlated subqueries
- EXISTS and NOT EXISTS

**Lab Exercises:**
```sql
-- JOINs with University database
"List all students with their advisor names"
"Show courses with their prerequisites"
"Find instructors who teach in multiple departments"

-- Subqueries
"Find students who have taken more courses than average"
"List departments where the average salary exceeds the university average"
```

**NL2SQL Deep Dive:**
- Observe how the agent handles JOIN queries
- Compare agent-generated JOINs with hand-written versions
- Test edge cases (missing relationships, ambiguous joins)

---

### Week 8: Normalization and Database Design
*"Organizing data properly"*

**Topics:**
- Why normalize? (Reduce redundancy, prevent anomalies)
- First Normal Form (1NF) - Atomic values, no repeating groups
- Second Normal Form (2NF) - Full functional dependency
- Third Normal Form (3NF) - No transitive dependencies
- When to denormalize (read performance, reporting)
- Refactoring existing schemas

**Tools:**
- 🛠️ **dbdiagram.io** - Visual schema design
- 🛠️ **NL2SQL Agent** - Test queries against normalized vs denormalized schemas

**Lab Exercises:**
- Identify normalization violations in sample data
- Normalize a denormalized "flat file" into 3NF
- Compare query complexity before/after normalization

**📝 Assignment 4 Due: Advanced Design & Optimization (15%)**
> Part A: Take a denormalized dataset and normalize it to 3NF. Document each step.
> Part B: Write 5 complex queries using JOINs and subqueries.
> Part C: Analyze and optimize 3 slow queries (include EXPLAIN output).

---

### Week 9: Indexes, Views, and Transactions
*"Performance and reliability"*

**Topics:**
- **Indexes:**
  - How indexes work (B-tree structure)
  - Creating indexes (single column, composite)
  - When to use indexes (and when not to)
  - EXPLAIN / Query execution plans
  
- **Views:**
  - Creating and using views
  - Simplifying complex queries
  - Security through views
  
- **Transactions & ACID:**
  - Atomicity, Consistency, Isolation, Durability
  - Transaction isolation levels
  - Basic concurrency concepts (locks, deadlocks)

**Lab Exercises:**
```sql
-- Index creation and analysis
CREATE INDEX idx_instructor_dept ON instructor(dept_name);
EXPLAIN ANALYZE SELECT * FROM instructor WHERE dept_name = 'Comp. Sci.';

-- View creation
CREATE VIEW cs_courses AS
SELECT c.course_id, c.title, s.semester, s.year
FROM course c JOIN section s ON c.course_id = s.course_id
WHERE c.dept_name = 'Comp. Sci.';

-- Transaction example
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

---

### Week 10: Advanced Topics & Final Presentations
*"Beyond the basics"*

**Topics (Brief Overview):**
- **Stored Procedures:** Reusable SQL code blocks
- **Triggers:** Automatic actions on data changes
- **Security:** Users, roles, permissions, SQL injection prevention
- **Database Integration:** APIs, ORMs, connection pooling
- **Emerging Trends:** 
  - AI-powered databases
  - Vector databases for embeddings
  - Real-time analytics
  - Cloud-native databases

**Class Schedule:**
- First half: Brief lecture on advanced topics
- Second half: **Final Project Presentations**

**🏆 Final Project Due & Presentations (20%)**
> Build a full-featured database application:
> - **Domain:** Choose your own (e-commerce, healthcare, sports, etc.)
> - **Requirements:**
>   - Minimum 8 tables with proper normalization
>   - Complete ERD with documentation
>   - DDL scripts with all constraints
>   - Sample data (20+ records per main table)
>   - 10 complex queries demonstrating JOINs, subqueries, aggregations
>   - At least 2 indexes with performance analysis
>   - At least 2 views
>   - NL2SQL agent configuration (YAML file) for your database
> - **Presentation:** 10-minute demo + Q&A

---

## 📋 Assignment Details

### Assignment 1: Foundations & Data Modeling (15%)
**Due:** End of Week 2

**Requirements:**
1. Given a business scenario (provided), create a complete ERD
2. Identify all entities, attributes, and relationships
3. Specify primary keys, foreign keys, and cardinality
4. Write a 1-page explanation of your design decisions
5. Use draw.io, dbdiagram.io, or MySQL Workbench

**Deliverables:** ERD diagram (PDF) + Written explanation (1-2 pages)

---

### Assignment 2: Schema Design & Setup (15%)
**Due:** End of Week 4

**Requirements:**
1. Design the schema for your Library System (mid-course project)
2. Write complete DDL scripts (CREATE TABLE statements)
3. Include all constraints (PK, FK, NOT NULL, CHECK, UNIQUE)
4. Create an ERD matching your DDL
5. Test scripts execute without errors

**Deliverables:** DDL scripts (.sql) + ERD diagram + Test execution screenshots

---

### Assignment 3: Data Manipulation & Querying (15%)
**Due:** End of Week 6

**Requirements:**
1. Write 15 queries against the Chinook music database:
   - 5 basic SELECT (filtering, sorting, DISTINCT)
   - 5 aggregate queries (GROUP BY, HAVING, COUNT, SUM, AVG)
   - 5 combined queries (multiple tables, nested conditions)
2. For each query, also run the equivalent natural language through NL2SQL agent
3. Compare and document differences between hand-written and AI-generated SQL

**Deliverables:** SQL file with queries + NL2SQL comparison report

---

### Assignment 4: Advanced Design & Optimization (15%)
**Due:** End of Week 8

**Requirements:**
1. **Normalization Exercise:** Take provided denormalized data, normalize to 3NF
2. **Complex Queries:** Write 5 queries using JOINs and subqueries
3. **Optimization:** Analyze 3 slow queries with EXPLAIN, propose and implement improvements

**Deliverables:** 
- Normalization documentation (before/after schemas, step-by-step)
- SQL queries with explanations
- EXPLAIN output analysis with optimization recommendations

---

### Mid-Course Project: Library Database (20%)
**Due:** End of Week 5

**Scenario:** Design a Library Management System

**Required Tables (minimum):**
- `books` - Book catalog
- `authors` - Author information
- `book_authors` - Many-to-many relationship
- `members` - Library members
- `loans` - Book checkout/return records
- `categories` - Book categories/genres

**Deliverables:**
1. ERD diagram
2. DDL scripts (all CREATE TABLE statements)
3. DML scripts (INSERT statements for sample data)
4. 10 sample queries demonstrating your schema
5. Brief documentation (2-3 pages)

---

### Final Project: Full-Featured Database (20%)
**Due:** Week 10 (Presentation Day)

**Choose Your Domain:** E-commerce, Healthcare, Sports League, Restaurant, Hotel, Inventory, etc.

**Requirements:**
1. Minimum 8 tables in 3NF
2. Complete ERD with cardinality notation
3. DDL scripts with all constraints
4. Sample data (20+ records per main table)
5. 10 complex queries (JOINs, subqueries, aggregations)
6. 2+ indexes with EXPLAIN analysis
7. 2+ views
8. NL2SQL agent YAML configuration for your database
9. 10-minute presentation demonstrating your database

**Deliverables:**
- All SQL scripts (DDL, DML, queries)
- ERD diagram
- YAML configuration file
- Documentation (5-7 pages)
- Presentation slides

---

## 🛠️ Technical Setup

### Required Software
| Tool | Purpose | Install |
|------|---------|---------|
| VS Code | Code editor | [code.visualstudio.com](https://code.visualstudio.com) |
| DB Browser for SQLite | SQLite GUI | [sqlitebrowser.org](https://sqlitebrowser.org) |
| MySQL Workbench | MySQL GUI + ERD | [mysql.com/products/workbench](https://mysql.com/products/workbench) |
| DBeaver or pgAdmin | PostgreSQL GUI | [dbeaver.io](https://dbeaver.io) |
| Python 3.12+ | NL2SQL agent | [python.org](https://python.org) |
| GitHub Account | Codespaces access | [github.com](https://github.com) |

### NL2SQL Agent Access
**Easiest:** Use GitHub Codespaces (zero local setup)
1. Go to course repository
2. Click "Open in Codespaces"
3. Add your GitHub token to `.env`
4. Start querying!

### Database Connections
| Database | Connection |
|----------|------------|
| University | `data/university.db` (SQLite - included) |
| ContosoHR | `lis-4230.database.windows.net` (Azure SQL) |
| Chinook | `lis4230mysql.mysql.database.azure.com` (MySQL) |
| Pagila | `lis4230postgres.postgres.database.azure.com` (PostgreSQL) |

---

## 📚 Recommended Resources

### Textbooks
- *"Database System Concepts"* by Silberschatz, Korth, Sudarshan
- *"Learning SQL"* by Alan Beaulieu
- *"SQL Performance Explained"* by Markus Winand

### Online Resources
- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [W3Schools SQL](https://www.w3schools.com/sql/)
- [Use The Index, Luke](https://use-the-index-luke.com/) - Query optimization
- [dbdiagram.io](https://dbdiagram.io/) - ERD design
- [pgexercises.com](https://pgexercises.com/) - PostgreSQL practice

### NL2SQL Agent Documentation
- [Student Quick Start Guide](STUDENT_QUICKSTART.md)
- [Lab Exercises](LAB_EXERCISES.md)
- [Database Setup](DATABASE_SETUP.md)

---

## 🎯 Learning Outcomes

Upon successful completion of this course, students will be able to:

1. **Design and implement relational database schemas** using Entity-Relationship diagrams, normalization principles (1NF-3NF), and proper constraints (primary keys, foreign keys, NOT NULL, CHECK)

2. **Write SQL queries across multiple platforms** including basic retrieval (SELECT, WHERE, ORDER BY), aggregations (GROUP BY, HAVING), multi-table joins (INNER, LEFT, RIGHT), and subqueries

3. **Create and manage database structures** using Data Definition Language (CREATE, ALTER, DROP) and Data Manipulation Language (INSERT, UPDATE, DELETE) with transaction control

4. **Optimize database performance** by analyzing query execution plans, creating appropriate indexes, and applying best practices for efficient data retrieval

5. **Leverage AI-powered tools for database interaction** using Natural Language to SQL (NL2SQL) agents to generate, validate, and learn from SQL queries

---

## 📅 Important Dates Summary

| Week | Deliverable | Weight |
|------|-------------|--------|
| 2 | Assignment 1: Foundations & Data Modeling | 15% |
| 4 | Assignment 2: Schema Design & Setup | 15% |
| 5 | Mid-Course Project: Library Database | 20% |
| 6 | Assignment 3: Data Manipulation & Querying | 15% |
| 8 | Assignment 4: Advanced Design & Optimization | 15% |
| 10 | Final Project + Presentation | 20% |

**Total: 100%**
