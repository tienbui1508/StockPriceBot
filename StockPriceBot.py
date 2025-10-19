from dotenv import load_dotenv
from openai import OpenAI
import os
import inspect
from pydantic import TypeAdapter
import requests
import yfinance as yf
import json
import gradio as gr

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


def get_symbol(company: str) -> str:
    """
    Retrieve the stock symbol for a specified company using the Yahoo Finance API.
    :param company: The name of the company for which to retrieve the stock symbol, e.g., 'Nvidia'.
    :output: The stock symbol for the specified company.
    """
    url = "https://query2.finance.yahoo.com/v1/finance/search"
    params = {"q": company, "country": "United States"}
    user_agents = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
    }
    res = requests.get(url=url, params=params, headers=user_agents)

    data = res.json()
    symbol = data["quotes"][0]["symbol"]
    return symbol


def get_stock_price(symbol: str):
    """
    Retrieve the most recent stock price data for a specified company using the Yahoo Finance API via the yfinance Python library.
    :param symbol: The stock symbol for which to retrieve data, e.g., 'NVDA' for Nvidia.
    :output: A dictionary containing the most recent stock price data.
    """
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1d", interval="1m")
    latest = hist.iloc[-1]
    return {
        "timestamp": str(latest.name),
        "open": latest["Open"],
        "high": latest["High"],
        "low": latest["Low"],
        "close": latest["Close"],
        "volume": latest["Volume"],
    }


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_symbol",
            "description": inspect.getdoc(get_symbol),
            "parameters": TypeAdapter(get_symbol).json_schema(),
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": inspect.getdoc(get_stock_price),
            "parameters": TypeAdapter(get_stock_price).json_schema(),
        },
    },
]

FUNCTION_MAP = {"get_symbol": get_symbol, "get_stock_price": get_stock_price}


def get_completion(messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, tools=tools, temperature=0
    )
    return response


def chat_logic(message, chat_history):
    """
    message: User message (string)
    chat_history: List of messages, each message is a pair (message, bot_message)
    """
    # Transform the chat history so that OpenAI can read it
    messages = [
        {
            "role": "system",
            "content": "You are a helpful customer support assistant. Use the supplied tools to assist the user. You are friendly,  witty, smart, analytical and sarcasm. Answer in the same language as the user.",
        },
    ]
    for user_message, bot_message in chat_history:
        messages.append({"role": "user", "content": user_message})
        messages.append({"role": "assistant", "content": bot_message})

    for user_message, bot_message in chat_history:
        messages.append({"role": "user", "content": user_message})
        messages.append({"role": "assistant", "content": bot_message})

    # Add the new user message
    messages.append({"role": "user", "content": message})

    response = get_completion(messages)
    first_choice = response.choices[0]
    finish_reason = first_choice.finish_reason

    while finish_reason != "stop":
        tool_call = first_choice.message.tool_calls[0]
        tool_call_function = tool_call.function
        tool_call_arguments = json.loads(tool_call_function.arguments)

        tool_function = FUNCTION_MAP[tool_call_function.name]
        result = tool_function(**tool_call_arguments)

        messages.append(first_choice.message)
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call_function.name,
                "content": json.dumps({"result": result}),
            }
        )

        # Wait for LLM response
        response = get_completion(messages)
        first_choice = response.choices[0]
        finish_reason = first_choice.finish_reason

    bot_message = first_choice.message.content
    chat_history.append((message, bot_message))
    return "", chat_history


# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# StockPriceBot - Real-time stock quotes")
    gr.Markdown(
        "### Quotes provided by Yahoo Finance - Insights powered by OpenAI GPT-4o-mini"
    )

    message = gr.Textbox(label="Your question:")
    chatbot = gr.Chatbot(label="StockPriceBot", height=600)
    message.submit(chat_logic, [message, chatbot], [message, chatbot])

demo.launch()
