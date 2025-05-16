import streamlit as st
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Initialize session state for schema
if 'schema' not in st.session_state:
    st.session_state.schema = {}

# Configure the page
st.set_page_config(
    page_title="Natural Language to SQL Converter",
    page_icon="🔍",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        font-size: 16px;
    }
    .sql-output {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 5px;
        font-family: monospace;
    }
    .schema-table {
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

def convert_to_sql(prompt, schema):
    """
    Convert natural language to SQL using Hugging Face's API
    """
    api_key = os.getenv('HUGGINGFACE_API_KEY')
    if not api_key:
        st.error("Please set your Hugging Face API key in the .env file")
        return None

    client = InferenceClient(token=api_key)

    # Create schema description
    schema_desc = "Database Schema:\n"
    for table, columns in schema.items():
        schema_desc += f"Table '{table}' with columns: {', '.join(columns)}\n"

    # Construct the prompt with schema
    full_prompt = f"""Given the following database schema:

{schema_desc}

Convert this question to a SQL query that works with the above schema.
Question: {prompt}

SQL Query:"""

    try:
        # Using FLAN-T5-XL model for SQL generation
        response = client.text_generation(
            prompt=full_prompt,
            model="google/flan-t5-xl",
            max_new_tokens=200,
            temperature=0.3,
            repetition_penalty=1.2
        )
        sql_query = response.strip()
        return sql_query
    except Exception as e:
        st.error(f"Error calling Hugging Face API: {str(e)}")
        return None

# Sidebar for schema management
with st.sidebar:
    st.title("Database Schema")
    
    # Table management
    st.subheader("Add New Table")
    new_table = st.text_input("Table Name")
    new_columns = st.text_input("Column Names (comma-separated)")
    
    if st.button("Add Table"):
        if new_table and new_columns:
            st.session_state.schema[new_table] = [col.strip() for col in new_columns.split(",")]
            st.success(f"Added table '{new_table}'")
        else:
            st.warning("Please enter both table name and columns")
    
    # Option to upload schema as JSON
    st.subheader("Upload Schema")
    schema_file = st.file_uploader("Upload schema (JSON)", type="json")
    if schema_file:
        try:
            st.session_state.schema = json.load(schema_file)
            st.success("Schema loaded successfully!")
        except Exception as e:
            st.error(f"Error loading schema: {str(e)}")
    
    # Option to download current schema
    if st.session_state.schema:
        st.download_button(
            "Download Schema",
            data=json.dumps(st.session_state.schema, indent=2),
            file_name="schema.json",
            mime="application/json"
        )
    
    # Clear schema button
    if st.button("Clear Schema"):
        st.session_state.schema = {}
        st.success("Schema cleared!")

    # Setup instructions
    st.markdown("---")
    st.title("Setup Instructions")
    st.markdown("""
    1. Create a free account on [Hugging Face](https://huggingface.co/join)
    2. Get your API key from [Hugging Face's settings](https://huggingface.co/settings/tokens)
    3. Create a `.env` file in the project directory
    4. Add your API key: `HUGGINGFACE_API_KEY=your_api_key_here`
    5. Restart the application
    
    **Note**: Hugging Face offers a free API tier with rate limits. No billing information required!
    """)

# Main content area
st.title("🔍 Natural Language to SQL Converter")

# Display current schema
if st.session_state.schema:
    st.subheader("Current Database Schema")
    for table, columns in st.session_state.schema.items():
        with st.expander(f"Table: {table}"):
            st.write(f"Columns: {', '.join(columns)}")
else:
    st.warning("Please add your database schema using the sidebar first!")

# Input section
with st.container():
    user_input = st.text_area(
        "Enter your question in natural language:",
        height=100,
        placeholder="Example: Show me all customers who made purchases over $1000 in the last month"
    )

    if st.button("Convert to SQL", type="primary"):
        if not st.session_state.schema:
            st.error("Please add your database schema first!")
        elif user_input:
            with st.spinner("Converting to SQL..."):
                sql_query = convert_to_sql(user_input, st.session_state.schema)
                if sql_query:
                    st.markdown("### Generated SQL Query:")
                    st.markdown(f'<div class="sql-output">{sql_query}</div>', unsafe_allow_html=True)
                    
                    # Add copy button
                    st.code(sql_query, language="sql")
        else:
            st.warning("Please enter a question first!")

# Add usage examples
with st.expander("See example questions"):
    st.markdown("""
    Try these example questions (after adding appropriate schema):
    - Find all employees who earn more than $50,000
    - Show the total sales by product category for the year 2023
    - List the top 10 customers by order value
    - Get all orders placed in the last 30 days
    - Calculate the average order value by month
    """)

# Add example schema
with st.expander("See example schema"):
    st.code("""
{
    "customers": ["customer_id", "name", "email", "join_date"],
    "orders": ["order_id", "customer_id", "order_date", "total_amount"],
    "products": ["product_id", "name", "category", "price"],
    "order_items": ["order_id", "product_id", "quantity", "unit_price"]
}
    """, language="json") 