import streamlit as st
from classifier import classify_ticket
from logger import log_request
import json
import os

# Page configuration
st.set_page_config(page_title="Ticket Classifier", page_icon="🎫", layout="centered")

# App title and description
st.title("🎫 Customer Support Ticket Classifier")
st.markdown("""
Classify customer support tickets into categories: **delivery, return, product_question, spam**.
The system will also provide a reply template.
""")

# Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("DeepSeek API Key", type="password", help="Enter your DeepSeek API key here.")
    if not api_key:
        st.warning("Please enter your DeepSeek API key in the sidebar to use the classifier.")

# Main Input
st.subheader("Enter Ticket Message")
user_input = st.text_area("Paste the customer message below:", height=150, placeholder="e.g., Where is my order #12345?")

if st.button("Classify Ticket"):
    if not api_key:
        st.error("API Key is missing. Please provide it in the sidebar.")
    elif not user_input.strip():
        st.warning("Please enter some text to classify.")
    else:
        with st.spinner("Classifying..."):
            try:
                result = classify_ticket(user_input, api_key)
                category = result["category"]
                confidence = result["confidence"]
                template = result["template"]
                tokens = result["tokens"]
                
                # Log the request
                log_request(user_input, result)
                
                # Display results
                st.success("Classification Complete!")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Category", category.capitalize())
                with col2:
                    st.metric("Confidence", f"{confidence:.2f}")
                with col3:
                    st.metric("Total Tokens", tokens["total"])
                
                # Warning for low confidence
                if confidence < 0.6:
                    st.warning("⚠️ **Low Confidence:** The AI is not very sure about this classification. Please review manually.")

                st.subheader("Proposed Reply Template")
                st.code(template, language="text")
                
                with st.expander("Token Details"):
                    st.write(f"**Input Tokens:** {tokens['input']}")
                    st.write(f"**Output Tokens:** {tokens['output']}")
                    st.write(f"**Total Tokens:** {tokens['total']}")
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Display Logs
st.divider()
st.subheader("Recent Activity (Logs)")
if os.path.exists("logs.json"):
    try:
        with open("logs.json", "r") as f:
            logs = json.load(f)
            if logs:
                st.json(logs[-5:]) # Show last 5 logs
            else:
                st.write("No logs yet.")
    except Exception:
        st.write("Error reading logs.")
else:
    st.write("No activity recorded yet.")
