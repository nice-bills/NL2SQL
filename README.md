# Natural Language to SQL Converter

A simple application that converts natural language questions into SQL queries using Hugging Face's API. Built with Streamlit, it provides a clean interface where users can input questions in plain English to get corresponding SQL queries.

## Features

- Convert natural language questions to SQL queries using Hugging Face's API
- Clean and intuitive user interface
- Example questions for reference
- Responsive design
- Fast and accurate SQL generation

## Prerequisites

- Python 3.7+
- Hugging Face API token

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

3. Create a `.env` file in the project root directory and add your Hugging Face API token:
```
HUGGINGFACE_API_TOKEN=your_token_here
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. Enter your question in natural language in the text area

4. Click "Convert to SQL" to generate the SQL query

## Example Questions

- Find all employees who earn more than $50,000
- Show the total sales by product category for the year 2023
- List the top 10 customers by order value
- Get all orders placed in the last 30 days
- Calculate the average order value by month

## Getting Started with Hugging Face

1. Create an account on [Hugging Face](https://huggingface.co)
2. Get your API token from your account settings
3. Hugging Face offers:
   - Access to state-of-the-art models
   - Easy-to-use API
   - Free tier available
   - High-quality results

## Security Note

Never commit your `.env` file or expose your API token. The `.env` file is included in `.gitignore` by default.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 