# 🚀 AI Web Explorer: Your Smart Research Bot

## 📖 Description

The AI Web Explorer is an intelligent agent designed to be your ultimate research companion. When you ask a question, the bot automatically searches the web for relevant information, processes the results, and provides a clear, concise summary.

This project utilizes the power of "tool use" in AI, where a Large Language Model (LLM) is empowered to leverage external tools—in this case, a web search API—to solve complex problems beyond its inherent knowledge.

## ✨ Features

-   **Interactive Q&A:** Ask any question through a simple command-line interface.
-   **Automated Web Search:** The bot uses the Google Custom Search API to find relevant articles and data to expand its knowledge base.
-   **AI-Powered Summarization:** Google's Gemini model processes the search results to generate a concise and accurate summary.
-   **Tool-Using Agent:** Built using Google's Agent Development Kit (ADK) to effectively orchestrate AI reasoning and tool execution.

## 🛠️ Technologies Used

-   **Language:** Python 3
-   **AI Framework:** Google's Agent Development Kit (ADK)
-   **AI Model:** Google Gemini API (`gemini-1.5-flash`)
-   **Web Search:** Google Custom Search JSON API

## ⚙️ Setup & Installation

Follow these steps to set up and run the project on your local machine.

### 1. Prerequisites

-   Python 3.8 or higher
-   Access to Google Cloud Platform and Google AI Studio

### 2. Clone the Repository

```bash
git clone <your-repository-link>
cd <your-repository-directory>