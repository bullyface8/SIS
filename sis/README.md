# Customer Support Ticket Classifier

A simple Streamlit application that uses the DeepSeek API to classify customer support tickets into four categories: `delivery`, `return`, `product_question`, and `spam`.

## Features
- **Ticket Classification**: Automatically categorizes customer messages.
- **Confidence Scoring**: Returns a confidence score (0.0 to 1.0) and warns users if the score is below 0.6.
- **Reply Templates**: Generates a brief response template based on the category.
- **Token Counting**: Tracks and displays token usage (input/output) using the `tiktoken` library.
- **Logging**: Saves every request, including metadata like confidence and tokens, to `logs.json`.
- **DeepSeek Integration**: Uses the `deepseek-chat` model for high-quality classification.

## Installation

1. **Clone or download** the project folder.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## Usage
1. Open the application in your browser (usually `http://localhost:8501`).
2. Enter your **DeepSeek API Key** in the sidebar.
3. Paste a customer message into the text area.
4. Click **Classify Ticket** to see the results.
5. Recent activity will be shown at the bottom and logged to `logs.json`.

## Technical Details
- **Engine**: DeepSeek API (OpenAI-compatible)
- **Model**: `deepseek-chat`
- **Frontend**: Streamlit
- **Logs**: JSON format
