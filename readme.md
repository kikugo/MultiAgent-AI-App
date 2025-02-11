# Multi-Agent AI App

# AI Agent Hub

This Streamlit application provides a unified interface for interacting with several AI-powered agents:

*   **Video Analyzer:**  Analyzes uploaded videos using Gemini 2.0, answering user-specified questions about the content.
*   **Financial Agent:** Provides financial data and analysis (analyst recommendations, news) for a stock ticker. Uses Groq, YFinance, and DuckDuckGo.
*   **PDF Assistant:**  Allows users to upload a PDF and ask questions about its content. Uses Groq, ChromaDB, and PhiData.

## Features

*   **Modular Design:** Each agent is a separate class.
*   **Streamlit Interface:**  User-friendly web interface.
*   **Theme Selection:** Light and dark themes.
*   **Error Handling:** Handles invalid inputs and API issues.
*   **URL Sanitization:**  Financial Agent sanitizes URLs.

## Getting Started

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/kikugo/MultiAgent-AI-App.git  # Use YOUR repo URL
    cd ai-agent-hub
    ```

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    conda create -n ai-agent-env python=3.10
    conda activate ai-agent-env
    ```
    (Or use `python3 -m venv venv` and `source venv/bin/activate`.)

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Environment Variables:**

    Create a `.env` file:

    ```
    GOOGLE_API_KEY=your_google_api_key
    GROQ_API_KEY=your_groq_api_key
    OPENAI_API_KEY=your_openai_api_key
    DATABASE_URL=postgresql+psycopg://ai:ai@localhost:5532/ai  # For PDF Assistant
    ```
    *Never* commit your `.env` file!

5.  **Run the Application:**

    ```bash
    streamlit run app.py
    ```

## Important Notes: PDF Assistant & PgVector

The PDF Assistant uses PgVector for storing and searching the PDF content.  You'll need a running PostgreSQL database with the `vector` extension enabled.  Here's a quick way to set it up using Docker (as per PhiData documentation):

1.  **Start the PgVector Docker Container:**

    ```bash
    docker run -d \
      -e POSTGRES_DB=ai \
      -e POSTGRES_USER=ai \
      -e POSTGRES_PASSWORD=ai \
      -e PGDATA=/var/lib/postgresql/data/pgdata \
      -v pgvolume:/var/lib/postgresql/data \
      -p 5532:5432 \
      --name pgvector \
      agnohq/pgvector:16
    ```
    This command creates a Docker container named `pgvector` running PostgreSQL with the necessary configurations.  Make sure you have Docker installed and running.  The `-v pgvolume:/var/lib/postgresql/data` part creates a persistent volume, so your data isn't lost when the container stops.  The `-p 5532:5432` maps port 5432 (the default PostgreSQL port) inside the container to port 5532 on your host machine.  You can access the database using `psql -h localhost -p 5532 -U ai -d ai` and the password `ai`.

2. **First Run of PDF Assistant:**  The *first* time you run the PDF Assistant and upload a PDF, the `knowledge_base.load(recreate=True, upsert=True)` line will create the necessary tables and populate the database.  You should *comment out* this line *after* the first successful run to avoid recreating the database every time. The provided code already handles it using session state, so no need to manually comment/uncomment anything!

3.  **DATABASE_URL:** The `DATABASE_URL` environment variable in your `.env` file should be set to `postgresql+psycopg://ai:ai@localhost:5532/ai` to connect to this database.  This is already included in the instructions above.

## Changing LLMs (Optional)

The agents are configured to use specific, cost-effective LLMs. If you wish to experiment with different models, refer to the PhiData documentation for instructions on how to change the `llm` parameter in the agent initialization.  You can find links to PhiData documentation in the original project description.  Look for comments like `# Users can change the model in phi data docs` in the agent code.

## Future Enhancements

*   User Authentication
*   More detailed error handling
*   Asynchronous operations
*   Caching
*   Additional agent features

## Contributing

Contributions are welcome!

## License

[MIT](https://choosealicense.com/licenses/mit/)