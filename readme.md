# Multi-Agent AI Platform

This Streamlit application provides a unified interface for interacting with multiple AI agents:

*   **Video Analyzer:**  Analyzes uploaded videos using Gemini 2.0, answering user-specified questions about the video content.
*   **Financial Agent:**  Provides financial data and analysis for a given stock ticker, including analyst recommendations and news summaries.  Uses Groq, YFinance, and DuckDuckGo.
*   **PDF Assistant:**  Allows users to upload a PDF file and ask questions about its content. Uses Groq, ChromaDB, and PhiData's PDF knowledge base capabilities.

## Features

*   **Modular Design:** Each agent is implemented as a separate class, making the code easy to maintain and extend.
*   **Streamlit Interface:**  Provides a user-friendly web interface for interacting with the agents.
*   **Theme Selection:**  Users can choose between a light and dark theme.
*   **Error Handling:**  Includes basic error handling to gracefully handle invalid inputs and API issues.
*   **URL Sanitization:**  The Financial Agent sanitizes URLs from web searches to prevent Markdown parsing errors.

## Getting Started

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
    cd YOUR_REPOSITORY_NAME
    ```

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    conda create -n venv python=3.10
    conda activate venv
    ```
    (Or use `python3 -m venv venv` and `source venv/bin/activate` if you prefer `venv`.)

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Environment Variables:**

    Create a `.env` file in the root directory and add your API keys:

    ```
    GOOGLE_API_KEY=your_google_api_key
    GROQ_API_KEY=your_groq_api_key
    OPENAI_API_KEY=your_openai_api_key
    DATABASE_URL=postgresql+psycopg://ai:ai@localhost:5532/ai  # If using PostgreSQL
    ```

    **Important:**  *Never* commit your `.env` file to Git!  It's included in the `.gitignore` file to prevent this.

5.  **Run the Application:**

    ```bash
    streamlit run app.py
    ```


## Future Enhancements

*   User Authentication
*   More detailed error handling
*   Asynchronous operations for long-running tasks
*   Caching for frequently accessed data
*   Additional features for each agent (see original project description for ideas)

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

[MIT](https://choosealicense.com/licenses/mit/)