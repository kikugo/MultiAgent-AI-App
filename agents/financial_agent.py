# agents/financial_agent.py
import streamlit as st
from agno.agent import Agent
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools
import re
import time
import random
from dotenv import load_dotenv
from utils.helpers import sanitize_url
import yfinance as yf
import pandas as pd
from agno.models.openai import OpenAIChat

load_dotenv()

class FinancialAgent:
    """
    Agent for fetching and displaying financial data using yfinance and web search.
    """
    def __init__(self):
        """Initializes the FinancialAgent with necessary tools and configurations."""

        # Initialize OpenAI model
        self.model = OpenAIChat(id="gpt-4o-mini-2024-07-18")

        # Web search agent for general information retrieval
        self.web_search_agent = Agent(
            name="Web Search Agent",
            role="Search the web for information",
            model=self.model,
            tools=[DuckDuckGoTools()],
            instructions=["Always include sources"],
            show_tool_calls=True,
            markdown=True,
        )

        # Finance agent for fetching financial data using yfinance tools
        self.finance_agent = Agent(
            name="Finance AI Agent",
            model=self.model,
            tools=[
                YFinanceTools(
                    stock_price=True,
                    analyst_recommendations=True,
                    stock_fundamentals=True,
                    company_news=True
                ),
            ],
            instructions=["Use tables to display the data"],
            show_tool_calls=True,
            markdown=True,
        )

        # Multi-agent combining web search and finance tools for comprehensive analysis
        self.multi_ai_agent = Agent(
            model=self.model,
            team=[self.web_search_agent, self.finance_agent],
            instructions=[
                "Summarize analyst recommendations and latest news for a given stock ticker using web search and financial tools."
            ],
            show_tool_calls=True,
            markdown=True,
        )

    def run(self, ticker=""):
        """
        Fetches and displays financial data for a given stock ticker.

        Handles user input, displays loading spinners, and error messages.
        """
        if ticker:
            with st.spinner(f"Fetching data for {ticker}..."):
                try:
                    response = self.fetch_data_with_retry(ticker)

                    if response and response.messages and response.messages[-1].content:
                        final_response = response.messages[-1].content
                        def replace_url(match):
                            return sanitize_url(match.group(0))
                        sanitized_response = re.sub(r'https?://[^\s<>"]+|www\.[^\s<>"]+', replace_url, final_response)
                        st.markdown(sanitized_response)

                    else:
                        st.error("Error: Could not retrieve response content.")

                except Exception as e:
                    st.error(f"Error fetching data: {e}")
        else:
            st.warning("Please enter a stock ticker.")

    def fetch_data_with_retry(self, ticker):
        """
        Fetches data with exponential backoff for rate limiting.

        Retries API calls with increasing delay if rate limit errors are encountered.
        """
        retries = 0
        max_retries = 5
        base_delay = 1

        while retries < max_retries:
            try:
                response = self.multi_ai_agent.run(f"Summarize analyst recommendation and share the latest news for {ticker}", stream=False)
                return response

            except Exception as e:
                # Handle rate limit errors specifically
                if "rate_limit_exceeded" in str(e).lower() or "429" in str(e):
                    retries += 1
                    delay = base_delay * (2 ** retries) + random.uniform(0, 1)
                    st.warning(f"Rate limit exceeded. Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                else:
                    raise

        raise Exception("Max retries exceeded. API rate limit.")