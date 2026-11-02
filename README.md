# 💬 Talk with Database

### Query Your Database Using Natural Language

Talk with Database is an AI-powered application that allows users to interact with a PostgreSQL database using plain English instead of writing SQL queries manually.

It uses Google's Gemini API to convert natural-language questions into SQL queries, validates the generated SQL for safety, executes approved queries against a read-only PostgreSQL database, and displays the results in an interactive table.

## 🚀 Features

- **Natural Language to SQL:** Convert everyday English questions into PostgreSQL queries using Gemini AI.
- **PostgreSQL Integration:** Retrieve information from a relational database containing interconnected tables.
- **SQL Query Validation:** Validate generated SQL queries and restrict execution to permitted read-only operations.
- **Read-Only Database Access:** Use a dedicated database user with read-only permissions to protect stored data.
- **Interactive Results:** Display query results in a structured table using Pandas and Streamlit.
- **Multiple Table Queries:** Support questions involving customers, products, orders, order items, and payments.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| PostgreSQL | Relational database |
| Neon | Cloud-hosted PostgreSQL |
| Google Gemini API | Natural-language-to-SQL generation |
| Streamlit | Interactive web interface |
| Psycopg | PostgreSQL connectivity |
| SQLGlot | SQL parsing and validation |
| Pandas | Data handling and tabular results |

## 🏗️ System Architecture

```text
           User
             |
             v
    Natural Language Question
             |
             v
       Streamlit Interface
             |
             v
        Gemini AI API
             |
             v
       Generated SQL Query
             |
             v
      SQL Validation Layer
             |
       +-----+------+
       |            |
     Valid        Invalid
       |            |
       v            v
 Read-Only DB     Reject Query
       |
       v
 PostgreSQL Database
       |
       v
   Query Results
       |
       v
 Interactive DataFrame
```

## 🗄️ Database Design

The project uses a PostgreSQL database with five interconnected tables:

| Table | Description |
|---|---|
| customers | Stores customer information |
| products | Stores product details and stock |
| orders | Stores customer orders |
| order_items | Stores products and quantities associated with orders |
| payments | Stores payment information and status |

Foreign keys establish relationships between customers, orders, products, order items, and payments.

## 💡 Example Questions

Users can ask questions such as:

- Show the top 5 customers by total spending.
- Which products have the lowest stock?
- What is the total revenue generated?
- Show all pending orders.
- Which customers have placed the most orders?
- Find the most popular product category.

The application converts these questions into SQL queries and displays the corresponding database results.

```

## 🔐 Security and Validation

The application incorporates safeguards to reduce the risk of unsafe SQL execution:

- Restricts execution to permitted read-only SQL queries.
- Uses a dedicated PostgreSQL read-only database account.
- Limits accessible database tables.
- Rejects disallowed SQL operations and potentially unsafe functions.
- Limits the number of returned records.

## ☁️ Deployment

The application is designed for deployment using:

- **GitHub:** Source code management.
- **Streamlit Community Cloud:** Application hosting.
- **Neon:** Cloud PostgreSQL database.

## 🎯 Learning Outcomes

Through this project, I explored:

- Relational database design and SQL queries.
- Primary keys, foreign keys, and table relationships.
- PostgreSQL database connectivity using Python.
- Natural-language-to-SQL generation using Generative AI.
- SQL parsing, validation, and secure query execution.
- Building and deploying interactive Python applications.

## 👩‍💻 Author

**Radhika Nerkar**

B.Tech – Information Technology

---

*Talk with Database – Making database interaction simpler through Generative AI.*
