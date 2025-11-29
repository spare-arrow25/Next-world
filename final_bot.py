# main.py

import os
import google.generativeai as genai
from adk.api import GenAI
from adk.tools import Tool, tool
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env.search_agent')
# --- SECURITY BEST PRACTICE: Load API keys from environment variables ---


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("SEARCH_ENGINE_ID")
GOOGLE_SEARCH_API_KEY = os.getenv("CUSTOM_SEARCH_API_KEY")

# --- Tool Definition ---
@tool
def search(query: str) -> str:
    """
    Searches the web for the given query and returns the most relevant snippets.
    Args:
        query: The search query.
    """
    service = build("customsearch", "v1", developerKey=GOOGLE_SEARCH_API_KEY)
    try:
        res = service.cse().list(q=query, cx=GOOGLE_CSE_ID, num=3).execute()
        snippets = [f"Title: {item['title']}\nSnippet: {item['snippet']}" for item in res.get("items", [])]
        return "\n---\n".join(snippets) if snippets else "No relevant search results found."
    except Exception as e:
        return f"An error occurred during search: {e}"

# --- Main Application Logic ---
def main():
    """
    Main function to run the AI Web Explorer bot.
    """
    # 1. Verify API Keys are set
    if not all([GOOGLE_API_KEY, GOOGLE_CSE_ID, GOOGLE_SEARCH_API_KEY]):
        print("❌ ERROR: One or more environment variables are not set.")
        print("Please set GOOGLE_API_KEY, GOOGLE_CSE_ID, and GOOGLE_SEARCH_API_KEY.")
        return

    # 2. Configure the Generative AI model
    genai.configure(api_key=GOOGLE_API_KEY)
    GenAI.configure(api_key=GOOGLE_API_KEY)
    
    # 3. Create the agent with the search tool
    agent = GenAI(
        model_name="gemini-1.5-flash-latest",
        tools=[search],
        instruction="""
        You are a helpful research assistant.
        When given a question, you must use the search tool to find relevant information.
        After searching, you must synthesize the information from the search results
        and provide a concise, easy-to-understand summary as the final answer.
        Do not make up information. Base your answer only on the provided search results.
        """
    )
    
    # --- Improved User Interface ---
    print("=" * 50)
    print("🚀 Welcome to the AI Web Explorer Bot! 🚀")
    print("=" * 50)
    print("Type your question below or 'exit' to quit.")

    while True:
        # 4. Get user input
        user_question = input("\n❓ Your Question: ")

        if user_question.lower() == 'exit':
            print("\n👋 Goodbye!")
            break

        # 5. Process the question
        print("\n⏳ Searching the web and summarizing... Please wait.")
        try:
            # Send the message to the agent and stream the response
            response_generator = agent.send_message_streaming(user_question)
            
            final_answer = ""
            for chunk in response_generator:
                if chunk.text:
                    final_answer += chunk.text
            
            # 6. Present the final answer
            print("\n" + "="*20 + " Answer " + "="*20)
            print(f"✅ Summary:\n\n{final_answer}")
            print("=" * 48)

        except Exception as e:
            print(f"\n❌ An error occurred: {e}")


if __name__ == "__main__":
    main()
