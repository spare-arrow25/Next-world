# Filename: twin-brain.py

import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- Configuration ---
# This is the safest way to load your API key.
# It reads an "environment variable" named GOOGLE_API_KEY.

load_dotenv(dotenv_path='.env.search_tools')

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
except KeyError:
    print("🚨 Error: GOOGLE_API_KEY environment variable not set.")
    print("Please set the GOOGLE_API_KEY environment variable with your API key.")
    exit() # Exit the script if the key is not found

# --- AI Model Initialization ---
# This creates an instance of the Gemini Pro model.
model = genai.GenerativeModel('gemini-pro-latest')
print("✅ AI Brain is initialized. Ready for your questions!")
print("--------------------------------------------------")

# --- Main Interaction Loop ---
# This loop will run forever, allowing you to ask multiple questions.
while True:
    # 1. Take User Input
    user_question = input("Ask your question (or type 'exit' to quit): ")

    if user_question.lower() == 'exit':
        print("👋 Goodbye!")
        break

    # 2. Send the question to the Gemini LLM
    try:
        print("\n🧠 Thinking...")
        response = model.generate_content(user_question)

        # 3. Present the Answer
        print("\n💡 Here's the answer:")
        print(response.text)
        print("--------------------------------------------------")

    except Exception as e:
        print(f"🚨 An error occurred: {e}")
        print("--------------------------------------------------")