
import streamlit as st
import pandas as pd
import psycopg
import sqlglot

from sqlglot import exp
from google import genai

# ---------------- CONFIGURATION ----------------

st.set_page_config(
    page_title="Talk with Database",
    page_icon="💬",
    layout="wide"
)

st.title("💬 Talk with Database")
st.caption("Ask questions about your database in plain English.")

MODEL_NAME = "gemini-3.8-flash"

@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

client = get_gemini_client()

DATABASE_URL = st.secrets["DATABASE_URL"]

DB_SCHEMA = """
customers(customer_id, customer_name, email, city, created_at)
products(product_id, product_name, category, price, stock_quantity)
orders(order_id, customer_id, order_date, status)
order_items(item_id, order_id, product_id, quantity, unit_price)
payments(payment_id, order_id, payment_date, amount,
         payment_method, payment_status)
"""

ALLOWED_TABLES = {
    "customers", "products", "orders",
    "order_items", "payments"
}

# ---------------- SQL GENERATION ----------------

def generate_sql(question):

    prompt = f"""
You are an expert PostgreSQL SQL query generator.

Database schema:
{DB_SCHEMA}

User question:
{question}

Rules:
1. Generate only PostgreSQL SELECT queries.
2. Use only the five tables listed in the schema.
3. Use correct JOIN conditions.
4. Calculate customer spending using
   SUM(quantity * unit_price).
5. Exclude cancelled orders from revenue calculations
   unless the user explicitly asks otherwise.
6. Never generate INSERT, UPDATE, DELETE, DROP,
   ALTER or other modification statements.
7. Never invent tables or columns.
8. Return only SQL, without Markdown.
9. Add LIMIT 100 to large list queries when appropriate.

SQL:
"""

    response = client.models.generate_content(
    model=MODEL_NAME,
    contents=prompt,
    config={
        "http_options": {
            "timeout": 60000
         }
    }
    )

    return response.text.strip().replace("```sql", "").replace("```", "").strip()


# ---------------- SQL VALIDATION ----------------

def validate_sql(query):

    try:
        statements = sqlglot.parse(query, read="postgres")

        if len(statements) != 1 or statements[0] is None:
            return False, "Only one SQL statement is allowed."

        tree = statements[0]

        if not isinstance(tree, (
            exp.Select, exp.Union, exp.Intersect, exp.Except
        )):
            return False, "Only SELECT queries are allowed."

        cte_names = {
            cte.alias_or_name.lower()
            for cte in tree.find_all(exp.CTE)
        }

        referenced_tables = {
            table.name.lower()
            for table in tree.find_all(exp.Table)
        }

        if not referenced_tables:
            return False, "Query must use an approved database table."

        if referenced_tables - ALLOWED_TABLES - cte_names:
            return False, "Query references an unapproved table."

        blocked_functions = {
            "PG_SLEEP", "PG_READ_FILE", "PG_LS_DIR",
            "SET_CONFIG", "DBLINK"
        }

        for function in tree.find_all(exp.Func):
            if function.sql_name().upper() in blocked_functions:
                return False, "Query contains a restricted function."

        return True, "SQL query passed validation."

    except Exception:
        return False, "Invalid SQL syntax."


# ---------------- QUERY EXECUTION ----------------

def execute_query(query):

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(query)

            if cur.description is None:
                raise ValueError("No result returned.")

            rows = cur.fetchmany(100)
            columns = [desc[0] for desc in cur.description]

    return pd.DataFrame(rows, columns=columns)


# ---------------- CHAT INTERFACE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message.get("sql"):
            with st.expander("View generated SQL"):
                st.code(message["sql"], language="sql")

        if message.get("data") is not None:
            st.dataframe(message["data"], use_container_width=True)

question = st.chat_input("Ask something about your database...")

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):

        try:
            with st.spinner("AI is thinking..."):

                generated_sql = generate_sql(question)

            is_safe, validation_message = validate_sql(generated_sql)

            if not is_safe:
                st.error(validation_message)

            else:
                st.success("SQL validation successful!")

                with st.expander("View generated SQL"):
                    st.code(generated_sql, language="sql")

                with st.spinner("Fetching database results..."):

                    result = execute_query(generated_sql)

                st.write("### Query Results")
                st.dataframe(result, use_container_width=True)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Here are your database results.",
                    "sql": generated_sql,
                    "data": result
                })

        except Exception as e:
            st.error(f"Error: {type(e).__name__}: {e}")
