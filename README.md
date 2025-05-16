# Natural Language to SQL Converter

This application converts natural language questions into SQL queries using Hugging Face's free API. It provides a user-friendly interface built with Streamlit where users can input their database schema and questions in plain English to get corresponding SQL queries.

## Features

- Convert natural language questions to SQL queries using FLAN-T5-XL model
- Database schema management:
  - Add tables and columns through the UI
  - Upload schema as JSON
  - Download current schema
  - View and manage schema in real-time
- Clean and intuitive user interface
- Example questions for reference
- Copy-to-clipboard functionality for generated queries
- Responsive design
- Free to use with Hugging Face's API

## Prerequisites

- Python 3.7+
- Hugging Face API key (free)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd natural-language-to-sql
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root directory and add your Hugging Face API key:
```
HUGGINGFACE_API_KEY=your_api_key_here
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. Set up your database schema:
   - Use the sidebar to add tables and columns
   - Or upload a JSON schema file
   - You can also download your current schema for later use

4. Enter your question in natural language in the text area

5. Click "Convert to SQL" to generate the SQL query

## Example Schema
```json
{
    "customers": ["customer_id", "name", "email", "join_date"],
    "orders": ["order_id", "customer_id", "order_date", "total_amount"],
    "products": ["product_id", "name", "category", "price"],
    "order_items": ["order_id", "product_id", "quantity", "unit_price"]
}
```

## Example Questions

- Find all employees who earn more than $50,000
- Show the total sales by product category for the year 2023
- List the top 10 customers by order value
- Get all orders placed in the last 30 days
- Calculate the average order value by month

## Getting Started with Hugging Face

1. Create a free account on [Hugging Face](https://huggingface.co/join)
2. Get your API key from [Hugging Face's settings](https://huggingface.co/settings/tokens)
3. The free tier includes:
   - Access to thousands of open-source models
   - Rate limits apply (but generous for personal use)
   - No credit card required

## Security Note

Never commit your `.env` file or expose your API key. The `.env` file is included in `.gitignore` by default.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 