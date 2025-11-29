import os
import json
import google.generativeai as genai
from googleapiclient.discovery import build
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv(dotenv_path='.env.search_agent')

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CUSTOM_SEARCH_API_KEY = os.getenv("CUSTOM_SEARCH_API_KEY") 
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

# --- Verification ---
if not all([GOOGLE_API_KEY, CUSTOM_SEARCH_API_KEY, SEARCH_ENGINE_ID]):
    raise ValueError("One or more required API keys or IDs not found! Check .env.search_agent.")

# --- Local Python Function (The Tool's Code) ---
# This is just the Python code. The AI does not see this directly.
def web_search(query: str) -> str:
  """The actual implementation of the web search tool."""
  print(f"⚡ [MANUAL] Performing web search for: '{query}'")
  try:
    service = build("customsearch", "v1", developerKey=CUSTOM_SEARCH_API_KEY)
    res = service.cse().list(q=query, cx=SEARCH_ENGINE_ID, num=3).execute()
    snippets = [f"{item['title']}: {item['snippet']}" for item in res.get('items', [])]
    if not snippets:
      return "No relevant search results found."
    # We return a dictionary as a string for clarity in the API call
    return json.dumps([item for item in res.get('items', [])])
  except Exception as e:
    return f"Error during search: {e}"

# --- Manual Tool Schema Definition ---
# This is the complex part that @genai.tool automates.
# You are describing your Python function in a way the LLM understands.
web_search_tool_declaration = genai.protos.Tool(
    function_declarations=[
        genai.protos.FunctionDeclaration(
            name="web_search",
            description="Performs a web search to find up-to-date information, answer questions about recent events, or research topics.",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "query": genai.protos.Schema(type=genai.protos.Type.STRING, description="The search query.")
                },
                required=["query"]
            )
        )
    ]
)

# --- Agent Orchestration (The Manual Way) ---
def run_research_bot():
  print("🚀 AI Web Explorer Bot Initialized (Manual Mode). Ask me anything!")
  
  genai.configure(api_key=GOOGLE_API_KEY)
  
  model = genai.GenerativeModel(
      model_name='gemini-1.5-flash',
      tools=[web_search_tool_declaration] # Pass the manually defined tool
  )
  
  # Start chat WITHOUT automatic function calling
  chat = model.start_chat()
  
  while True:
    question = input("\nYour question: ")
    if question.lower() in ['exit', 'quit']:
      print("Bot shutting down. Goodbye! 👋")
      break
      
    print("🧠 Thinking...")
    # 1. Send the user's question to the model
    response = chat.send_message(question)
    
    # 2. Check if the model wants to call a function
    try:
        function_call = response.candidates[0].content.parts[0].function_call
    except (IndexError, AttributeError):
        function_call = None
        
    if function_call:
        print(f"▶️ Model requested function call: {function_call.name}")
        
        # 3. If so, call the appropriate local function
        if function_call.name == "web_search":
            # Extract arguments provided by the model
            args = {key: value for key, value in function_call.args.items()}
            # Execute the function
            tool_result = web_search(**args)
            
            # 4. Send the function's result back to the model
            print("✔️ Function executed. Sending result back to model...")
            response = chat.send_message(
                genai.protos.Part(
                    function_response=genai.protos.FunctionResponse(
                        name="web_search",
                        response={"result": tool_result}
                    )
                )
            )
    
    # 5. Print the final text response from the model
    print("\n✅ Final Answer:")
    print(response.text)

if __name__ == "__main__":
  run_research_bot()