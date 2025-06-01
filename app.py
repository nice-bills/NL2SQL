import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')

# Configure the page
st.set_page_config(
    page_title="Natural Language to SQL Converter",
    page_icon="🤖",
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
    </style>
    """, unsafe_allow_html=True)

API_URL = "https://router.huggingface.co/novita/v3/openai/chat/completions"
headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
}

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {str(e)}")
        return None

def generate_sql(question):
    prompt = f"""You are a SQL expert. Convert the following natural language question to a SQL query. Provide only the SQL query, no other text or comments.
    Question: {question}
    SQL Query:"""
    
    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "model": "meta-llama/llama-3.1-8b-instruct"
    }
    
    response = query(payload)
    if response and 'choices' in response and len(response['choices']) > 0:
        return response['choices'][0]['message']['content']
    else:
        st.error("Failed to generate SQL query. Please try again.")
        return None

# Main content area
st.title("🤖 Natural Language to SQL Converter")

# Setup instructions
with st.expander("Setup Instructions"):
    st.markdown("""
    1. Create an account on [Hugging Face](https://huggingface.co)
    2. Get your API key from Hugging Face's settings
    3. Create a `.env` file in the project directory
    4. Add your API key: `HUGGINGFACE_API_TOKEN=your_api_key_here`
    5. Restart the application
    """)

# Input section
user_input = st.text_area(
    "Enter your question in natural language:",
    height=100,
    placeholder="Example: Show me all employees who earn more than $50,000"
)

if st.button("Convert to SQL", type="primary"):
    if not HUGGINGFACE_API_TOKEN:
        st.error("Please set your HUGGINGFACE_API_TOKEN in the .env file")
    elif user_input:
        with st.spinner("Converting to SQL..."):
            sql_query = generate_sql(user_input)
            if sql_query:
                st.markdown("### Generated SQL Query:")
                # st.markdown(f'<div class="sql-output">{sql_query}</div>', unsafe_allow_html=True)
                st.code(sql_query, language="sql")
    else:
        st.warning("Please enter a question!")

# Add example questions
with st.expander("Example Questions"):
    st.markdown("""
    Try these example questions:
    - Find all employees who earn more than $50,000
    - Show the total sales by product category for the year 2023
    - List the top 10 customers by order value
    - Get all orders placed in the last 30 days
    - Calculate the average order value by month
    """) 