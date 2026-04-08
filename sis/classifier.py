import os
import tiktoken
from openai import OpenAI

BASE_URL = "https://api.deepseek.com/v1"
MODEL = "deepseek-chat"

def count_tokens(text, model="gpt-3.5-turbo"):
    """
    Counts tokens in a text string using tiktoken.
    DeepSeek doesn't have a public tiktoken encoding, so we use gpt-3.5-turbo as an approximation.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception:
        # Fallback if encoding not found
        return len(text.split())

def classify_ticket(text, api_key):
    """
    Classifies a support ticket into one of four categories and generates a response template.
    Includes a confidence score and token counts.
    """
    if not api_key:
        raise ValueError("DeepSeek API key is required.")

    client = OpenAI(api_key=api_key, base_url=BASE_URL)

    system_prompt = (
        "You are a customer support ticket classifier. "
        "Classify the input message into exactly one of these categories: "
        "[delivery, return, product_question, spam]. "
        "Also provide a confidence score between 0.0 and 1.0. "
        "Then, provide a brief reply template for that category. "
        "Return the output in the following format:\n"
        "Category: <category>\n"
        "Confidence: <score>\n"
        "Template: <template>"
    )

    try:
        # Count input tokens
        input_tokens = count_tokens(text) + count_tokens(system_prompt)

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
            stream=False
        )
        content = response.choices[0].message.content
        
        # Count output tokens
        output_tokens = count_tokens(content)
        
        # Simple parsing
        lines = content.strip().split("\n")
        category = "unknown"
        confidence = 0.0
        template = ""
        
        for line in lines:
            line = line.strip()
            if line.lower().startswith("category:"):
                category = line.split(":", 1)[1].strip().lower()
            elif line.lower().startswith("confidence:"):
                try:
                    confidence = float(line.split(":", 1)[1].strip())
                except ValueError:
                    confidence = 0.0
            elif line.lower().startswith("template:"):
                template = line.split(":", 1)[1].strip()
        
        # Validate category
        valid_categories = ["delivery", "return", "product_question", "spam"]
        if category not in valid_categories:
            category = "other"
            
        return {
            "category": category,
            "template": template,
            "confidence": confidence,
            "tokens": {
                "input": input_tokens,
                "output": output_tokens,
                "total": input_tokens + output_tokens
            }
        }

    except Exception as e:
        raise Exception(f"API Error: {str(e)}")
