# Week-by-Week Lab Exercises
## LIS 4230: Relational Database Management Systems

---

## Week 1: Introduction to RDBMS & Basic SELECT
**Database:** ContosoHR (Azure SQL)

### Learning Objectives
- Understand the relational model
- Write basic SELECT statements
- Use WHERE clauses for filtering
- Sort results with ORDER BY

### Lab Exercises

#### Exercise 1.1: Basic SELECT
Write SQL queries to answer these questions. Then test them with the NL2SQL agent.

1. List all columns from the Employees table
2. Show only the FirstName and LastName of all employees
3. Display employee names and their salaries

**NL2SQL Test:**
```
"Show me all employees"
"List employee names and salaries"
```

#### Exercise 1.2: WHERE Clause Filtering
1. Find all employees in the Engineering department (DepartmentID = 1)
2. List employees with salary greater than $100,000
3. Show employees hired after January 1, 2024
4. Find all active employees (IsActive = 1)

**NL2SQL Test:**
```
"Who works in Engineering?"
"Show employees earning over 100000"
"List employees hired in 2024"
```

#### Exercise 1.3: ORDER BY
1. List all employees sorted by last name alphabetically
2. Show employees ordered by salary (highest first)
3. Display employees sorted by hire date (most recent first)

**NL2SQL Test:**
```
"List employees alphabetically by last name"
"Who are the highest paid employees?"
"Show recently hired employees"
```

### Assignment 1
Compare your hand-written SQL with the AI-generated SQL for 10 different questions.
Document any differences and discuss which version is better and why.

---

## Week 2: Data Types, Functions & Aggregations
**Database:** ContosoHR (Azure SQL)

### Learning Objectives
- Understand SQL data types
- Use built-in string, date, and numeric functions
- Apply aggregate functions (COUNT, SUM, AVG, MIN, MAX)
- Group data with GROUP BY and filter groups with HAVING

### Lab Exercises

#### Exercise 2.1: Built-in Functions
1. Display employee full names (FirstName + ' ' + LastName)
2. Show the year each employee was hired (using YEAR function)
3. Calculate how long each employee has been with the company in years
4. Display salaries formatted with two decimal places

```sql
-- Example: Full name
SELECT FirstName + ' ' + LastName AS FullName FROM dbo.Employees;

-- Example: Years employed
SELECT FirstName, LastName, 
       DATEDIFF(YEAR, HireDate, GETDATE()) AS YearsEmployed
FROM dbo.Employees;
```

#### Exercise 2.2: Aggregate Functions
1. Count the total number of employees
2. Find the total payroll (sum of all salaries)
3. Calculate the average salary
4. Find the minimum and maximum salaries

**NL2SQL Test:**
```
"How many employees do we have?"
"What is the total payroll?"
"What is the average salary?"
```

#### Exercise 2.3: GROUP BY and HAVING
1. Count employees in each department
2. Calculate average salary by department
3. Find total budget by department
4. Show only departments with more than 4 employees

**NL2SQL Test:**
```
"How many employees are in each department?"
"What is the average salary by department?"
"Which departments have more than 4 employees?"
```

### Assignment 2
Create a comprehensive salary analysis report including:
- Total headcount and payroll
- Average, min, max salary by department
- Departments with above-average salaries

---

## Week 3: JOINs and Table Relationships
**Database:** ContosoHR (Azure SQL)

### Learning Objectives
- Understand primary and foreign keys
- Write INNER JOIN, LEFT JOIN queries
- Use self-joins for hierarchical data
- Combine data from multiple tables

### Lab Exercises

#### Exercise 3.1: Understanding Relationships
Draw an ER diagram showing relationships between:
- Employees and Departments
- Employees and PerformanceReviews
- Employees and TimeOffRequests
- Employees and Employees (manager relationship)

#### Exercise 3.2: INNER JOIN
1. List employees with their department names
2. Show performance reviews with employee and reviewer names
3. Display time-off requests with employee names and department

```sql
-- Example: Employee with department
SELECT e.FirstName, e.LastName, d.Name AS Department
FROM dbo.Employees e
INNER JOIN dbo.Departments d ON e.DepartmentID = d.DepartmentID;
```

**NL2SQL Test:**
```
"List employees with their department names"
"Show performance reviews with employee names"
```

#### Exercise 3.3: LEFT JOIN
1. List all departments with employee count (include empty departments)
2. Show all employees with their manager names (include employees without managers)

#### Exercise 3.4: Self-Join
1. Display each employee with their direct manager's name
2. Find employees who manage other employees

**NL2SQL Test:**
```
"Show each employee with their manager"
"Who are the managers?"
```

### Assignment 3
1. Create an ER diagram for ContosoHR database
2. Write 5 complex JOIN queries that combine 3 or more tables

---

## Week 4: Subqueries and CTEs
**Database:** ContosoHR (Azure SQL)

### Learning Objectives
- Write scalar and correlated subqueries
- Use EXISTS and NOT EXISTS
- Create Common Table Expressions (CTEs)
- Compare subquery vs JOIN approaches

### Lab Exercises

#### Exercise 4.1: Scalar Subqueries
1. Find employees earning more than the average salary
2. List employees in the department with the highest budget
3. Show the employee with the highest salary

```sql
-- Example: Above average salary
SELECT FirstName, LastName, Salary
FROM dbo.Employees
WHERE Salary > (SELECT AVG(Salary) FROM dbo.Employees);
```

**NL2SQL Test:**
```
"Who earns more than average?"
"Show the highest paid employee"
```

#### Exercise 4.2: Correlated Subqueries
1. Find employees earning more than their department average
2. List the top performer in each department
3. Show employees with no time-off requests

```sql
-- Example: Above department average
SELECT e.FirstName, e.LastName, e.Salary, e.DepartmentID
FROM dbo.Employees e
WHERE e.Salary > (
    SELECT AVG(e2.Salary) 
    FROM dbo.Employees e2 
    WHERE e2.DepartmentID = e.DepartmentID
);
```

#### Exercise 4.3: EXISTS / NOT EXISTS
1. Find departments that have at least one employee
2. List employees who have never had a performance review
3. Show departments with pending time-off requests

#### Exercise 4.4: Common Table Expressions
1. Rewrite a complex subquery as a CTE
2. Create a recursive CTE for the management hierarchy
3. Use multiple CTEs in a single query

```sql
-- Example: CTE for department stats
WITH DeptStats AS (
    SELECT DepartmentID, 
           COUNT(*) AS EmpCount, 
           AVG(Salary) AS AvgSalary
    FROM dbo.Employees
    GROUP BY DepartmentID
)
SELECT d.Name, ds.EmpCount, ds.AvgSalary
FROM dbo.Departments d
JOIN DeptStats ds ON d.DepartmentID = ds.DepartmentID;
```

### Assignment 4
Rewrite 5 subqueries as JOINs and compare execution plans.

---

## Week 5: Database Design Principles
**Databases:** ContosoHR (Azure SQL) + Chinook (MySQL)

### Learning Objectives
- Create Entity-Relationship diagrams
- Apply normalization rules (1NF through BCNF)
- Understand denormalization trade-offs
- Design schema metadata for AI agents

### Lab Exercises

#### Exercise 5.1: Schema Analysis
Compare the schemas of ContosoHR and Chinook:

| Aspect | ContosoHR | Chinook |
|--------|-----------|---------|
| Primary Domain | | |
| Number of Tables | | |
| Key Relationships | | |
| Normalization Level | | |

#### Exercise 5.2: Normalization Review
Identify the normal form of each table:
1. Is Employees in 3NF? Why or why not?
2. Is the Track table properly normalized?
3. Identify any transitive dependencies

#### Exercise 5.3: Design for AI
Write schema descriptions that would help an AI understand:
1. What business questions can this database answer?
2. What are the key relationships?
3. What columns are commonly queried together?

### Assignment 5
Design a new database schema for a domain of your choice.
Include AI agent configuration (system prompt, few-shot examples).

---

## Week 6: Cross-Platform SQL
**Databases:** ContosoHR + Chinook + Pagila

### Learning Objectives
- Understand SQL dialect differences
- Write portable SQL
- Apply constraints appropriately
- Work with indexes

### Lab Exercises

#### Exercise 6.1: Dialect Translation
Write the same query for all three platforms:

**Query 1:** "Get the top 10 items by count"
- T-SQL (Azure SQL): `SELECT TOP 10 ...`
- MySQL: `SELECT ... LIMIT 10`
- PostgreSQL: `SELECT ... LIMIT 10`

**Query 2:** "Concatenate first and last name"
- T-SQL: `FirstName + ' ' + LastName`
- MySQL: `CONCAT(FirstName, ' ', LastName)`
- PostgreSQL: `first_name || ' ' || last_name`

#### Exercise 6.2: Platform-Specific Features
Explore unique features:
- T-SQL: PIVOT, CROSS APPLY
- MySQL: GROUP_CONCAT, JSON functions
- PostgreSQL: Array types, Window functions, LATERAL

### Assignment 6
Port 10 ContosoHR queries to both MySQL (Chinook equivalent) and PostgreSQL (Pagila equivalent).

---

## Week 7: Query Execution Plans
**Database:** Pagila (PostgreSQL)

### Learning Objectives
- Read and interpret execution plans
- Identify performance bottlenecks
- Understand cost estimation
- Compare query approaches

### Lab Exercises

#### Exercise 7.1: EXPLAIN Basics
```sql
EXPLAIN SELECT * FROM public.film WHERE rating = 'PG';
EXPLAIN ANALYZE SELECT * FROM public.film WHERE rating = 'PG';
```

Questions:
1. What is the estimated cost?
2. What type of scan is being used?
3. How many rows are estimated vs actual?

#### Exercise 7.2: Join Analysis
```sql
EXPLAIN ANALYZE
SELECT f.title, COUNT(r.rental_id)
FROM public.film f
JOIN public.inventory i ON f.film_id = i.film_id
JOIN public.rental r ON i.inventory_id = r.inventory_id
GROUP BY f.film_id, f.title
ORDER BY COUNT(r.rental_id) DESC
LIMIT 10;
```

Analyze:
1. What join method is used?
2. Where is the most time spent?
3. How could this be optimized?

### Assignment 7
Optimize 5 slow queries with documented execution plan analysis.

---

## Week 8: Indexing Strategies
**Databases:** All platforms

### Learning Objectives
- Create effective indexes
- Understand index trade-offs
- Design composite indexes
- Analyze index usage

### Lab Exercises

#### Exercise 8.1: Index Impact
```sql
-- Before index
EXPLAIN ANALYZE SELECT * FROM public.rental WHERE customer_id = 100;

-- Create index
CREATE INDEX idx_rental_customer ON public.rental(customer_id);

-- After index
EXPLAIN ANALYZE SELECT * FROM public.rental WHERE customer_id = 100;
```

#### Exercise 8.2: Composite Indexes
When to use composite indexes:
```sql
-- Query filters on two columns
SELECT * FROM public.rental 
WHERE customer_id = 100 AND return_date IS NULL;

-- Consider index on (customer_id, return_date)
CREATE INDEX idx_rental_customer_return ON public.rental(customer_id, return_date);
```

### Assignment 8
Design an indexing strategy for a high-traffic rental application.

---

## Week 9: Prompt Engineering for NL2SQL
**Databases:** All platforms

### Learning Objectives
- Understand how LLMs interpret schemas
- Write effective system prompts
- Create few-shot examples
- Handle edge cases

### Lab Exercises

#### Exercise 9.1: Prompt Analysis
Examine the current prompts in the YAML config files:
1. What information is provided to the LLM?
2. How are tables described?
3. What makes a good few-shot example?

#### Exercise 9.2: Prompt Modification
Modify the system prompt to:
1. Handle ambiguous column names
2. Always include error handling
3. Prefer certain join types

#### Exercise 9.3: Few-Shot Engineering
Add few-shot examples for:
1. Complex aggregations
2. Date range queries
3. Percentage calculations

### Assignment 9
Write prompts for a new database domain (e-commerce, healthcare, etc.)

---

## Week 10: Building LangGraph Agents
**Databases:** All platforms

### Learning Objectives
- Understand LangGraph architecture
- Trace agent execution
- Add new capabilities
- Handle errors gracefully

### Lab Exercises

#### Exercise 10.1: Code Walkthrough
Trace through these files:
- `src/data_agent/graph/data_agent_graph.py`
- `src/data_agent/nodes/`
- `src/data_agent/tools/`

Questions:
1. How is state managed?
2. How are errors handled?
3. How is the database queried?

#### Exercise 10.2: Add a New Agent
Add the Pagila agent to the multi-database config and test routing.

#### Exercise 10.3: Custom Validation
Add a node that validates SQL before execution:
- Check for dangerous operations (DROP, DELETE without WHERE)
- Verify table names exist in schema
- Limit result set size

### Final Project
Build a multi-database NL2SQL agent that:
1. Routes queries to appropriate databases
2. Handles errors gracefully
3. Provides formatted responses
4. Includes at least 3 databases
