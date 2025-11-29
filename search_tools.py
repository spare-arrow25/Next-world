# search_tool.py

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv(dotenv_path='.env.search_tools')

# --- Configuration ---
# Get your credentials from the .env file
# IMPORTANT: DO NOT hardcode these values in the script!
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CUSTOM_SEARCH_ENGINE_ID = os.getenv("CUSTOM_SEARCH_ENGINE_ID")

def google_search(query: str, num_results: int = 5):
    """
    Performs a Google search using the Custom Search JSON API.
    
    Args:
        query (str): The search query.
        num_results (int): The number of search results to return.
        
    Returns:
        list: A list of dictionaries, where each dictionary represents a search result.
              Returns an empty list if an error occurs.
    """
    if not GOOGLE_API_KEY or not CUSTOM_SEARCH_ENGINE_ID:
        print("🔴 ERROR: Missing GOOGLE_API_KEY or CUSTOM_SEARCH_ENGINE_ID in .env file.")
        return []

    # API endpoint
    url = "https://www.googleapis.com/customsearch/v1"
    
    # Parameters for the API request
    params = {
        'key': GOOGLE_API_KEY,
        'cx': CUSTOM_SEARCH_ENGINE_ID,
        'q': query,
        'num': num_results
    }
    
    try:
        # Make the GET request
        print(f"🔍 Searching the web for: '{query}'...")
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        # Parse the JSON response
        search_results = response.json()
        
        # Extract the relevant items
        items = search_results.get('items', [])
        
        # Format the results
        formatted_results = []
        for item in items:
            formatted_results.append({
                'title': item.get('title'),
                'link': item.get('link'),
                'snippet': item.get('snippet')
            })
        
        return formatted_results

    except requests.exceptions.RequestException as e:
        print(f"🔴 ERROR: An error occurred during the API request: {e}")
        return []
    except Exception as e:
        print(f"🔴 ERROR: An unexpected error occurred: {e}")
        return []

# --- Main Execution ---
if __name__ == "__main__":
    # Example usage of the search function
    search_query = "What are the benefits of using AI in social impact projects?"
    results = google_search(search_query)
    
    if results:
        print("\n✅ Search complete! Here are the top results:\n")
        # Print the results in a readable format
        for i, result in enumerate(results, 1):
            print(f"--- Result {i} ---")
            print(f"Title: {result['title']}")
            print(f"Link: {result['link']}")
            print(f"Snippet: {result['snippet']}\n")
    else:
        print("No search results found or an error occurred.")
