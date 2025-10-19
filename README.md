# StockPriceBot

A real-time stock price chatbot that demonstrates OpenAI's function calling capabilities, integrating with Yahoo Finance data and featuring a Gradio interface. This project was created specifically to practice and showcase the implementation of OpenAI's function calling feature in a real-world application.

## Project Purpose

This is a focused learning project designed to:

- Master OpenAI's function calling feature by implementing practical use cases
- Demonstrate how to structure and register custom functions with OpenAI's API
- Show effective integration of external APIs (Yahoo Finance) through function calling
- Practice handling the back-and-forth flow between the LLM and custom functions
- Implement a clean interface for showcasing function calling capabilities

Whether you're also learning or just curious about the implementation, feel free to explore and use this code as a reference for your own learning journey!

## Features

- Real-time stock price queries using Yahoo Finance API
- Natural language processing powered by OpenAI GPT-4o-mini
- Interactive chat interface built with Gradio
- Company name to stock symbol conversion
- Detailed stock information including open, high, low, close prices, and volume
- Responsive and user-friendly web interface

## Prerequisites

- Python 3.x
- OpenAI API key
- Internet connection for real-time stock data

## Required Packages

```bash
pip install python-dotenv openai pydantic requests yfinance gradio
```

## Setup

1. Clone the repository
2. Create a `.env` file in the root directory
3. Add your OpenAI API key to the `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Run the application:
   ```bash
   python StockPriceBot.py
   ```
2. Open the provided Gradio interface URL in your web browser
3. Start chatting with the bot! You can ask questions like:
   - "What's the current price of Apple stock?"

### Stock Symbol Lookup

- Automatically converts company names to stock symbols
- Supports US-listed companies

  - Current price
  - Trading volume
  - Timestamp of data

- Clean and intuitive Gradio web interface
- Persistent chat history

## Technical Details

- Stateful chat history management
- Custom user agent handling for API requests

- Yahoo Finance API for stock data
- OpenAI GPT-4o-mini for natural language processing
- Gradio for web interface

## Learning Notes

Feel free to experiment with the code, suggest improvements, or use it as inspiration for your own learning projects!
