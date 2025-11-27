# Financial News Sentiment Analyzer (Capstone Project)

## Overview

This project is a Financial News Sentiment Analyzer designed to scrape financial news articles, summarize their content, and evaluate the potential market impact on specific companies. It leverages a local Large Language Model (LLM), specifically a fine-tuned version of Llama 3.1 (`fin-llama3.1-8b`), to perform advanced natural language processing tasks tailored for the financial domain.

## Features

- **News Scraping**: Automatically scrapes the latest financial news headlines and articles from LiveMint.
- **Article Summarization**: Generates concise, one-sentence summaries of financial articles, focusing on core financial topics and events.
- **Sentiment & Impact Analysis**: Evaluates the summarized text to assign impact scores (from -1.0 to 1.0) to mentioned companies, reflecting the potential effect on their stock performance.
- **REST API**: Provides a Flask-based REST API endpoint (`/analyze`) to process articles and return impact scores in JSON format.
- **Middleware Integration**: Uses a dedicated middleware to interface with the local Ollama LLM instance.

## Prerequisites

Before running the project, ensure you have the following installed:

- **Python 3.x**: The programming language used for the backend.
- **Ollama**: A tool for running LLMs locally.
- **FinLlama Model**: You need to pull the specific model used in this project:

  ```bash
  ollama pull hf.co/us4/fin-llama3.1-8b:Q5_K_M
  ```

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory.
2. **Install Python dependencies**:
    It is recommended to use a virtual environment.

    ```bash
    pip install flask requests beautifulsoup4 ollama
    ```

## Usage

### 1. Start the Backend Server

The Flask application serves as the API for analyzing articles.

```bash
python backend/app.py
```

The server will start on `http://localhost:5000`.

### 2. Run the News Scraper

The scraper fetches the latest news and sends it to the backend for analysis.

```bash
python backend/NewsScrapper.py
```

This script will:

1. Scrape the latest article link from LiveMint.
2. Extract the article content.
3. Send the content to the running Flask API.
4. Print the JSON response containing company names and their impact scores.

## Project Structure

- `backend/app.py`: The Flask API server handling analysis requests.
- `backend/FinLlama_Middleware.py`: Contains functions `Summarize` and `Evaluate` that interact with the Ollama LLM.
- `backend/NewsScrapper.py`: Script to scrape news and trigger analysis.
- `backend/StockNames.csv`: A CSV file containing a list of stock names (used by the middleware).
