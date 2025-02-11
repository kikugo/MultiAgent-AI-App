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
from agno.models.openai import OpenAIChat


load_dotenv()

class FinancialAgent:
    def __init__(self):

        # Initialize OpenAI model
        self.model = OpenAIChat(id="gpt-4o-mini-2024-07-18") # Users can change model from phi data docs

        self.web_search_agent = Agent(
            name="Web Search Agent",
            role="Search the web for information",
            model=self.model,
            tools=[DuckDuckGoTools()],
            instructions=["Always include sources"],
            show_tool_calls=True,
            markdown=True,
        )

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
        retries = 0
        max_retries = 5
        base_delay = 1

        while retries < max_retries:
            try:
                response = self.multi_ai_agent.run(f"Summarize analyst recommendation and share the latest news for {ticker}", stream=False)
                return response

            except Exception as e:
                if "rate_limit_exceeded" in str(e).lower() or "429" in str(e):
                    retries += 1
                    delay = base_delay * (2 ** retries) + random.uniform(0, 1)
                    st.warning(f"Rate limit exceeded. Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                else:
                    raise

        raise Exception("Max retries exceeded. API rate limit.")