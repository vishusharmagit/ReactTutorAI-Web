# React Tutor AI - Web Version

This Streamlit web app uses Retrieval Augmented Generation (RAG) to answer React questions from PDF books.

## Project Structure

- `books/`: Put your PDF books here.
- `data/chroma_db/`: Local ChromaDB store created by `ingest.py` in the terminal project.
- `streamlit_app.py`: Streamlit web interface.
- `requirements.txt`: Python dependencies.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure `data/chroma_db/` already exists from the terminal project's ingestion step.
4. Create a `.streamlit/secrets.toml` file containing:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```
5. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

## Notes

- This version uses Groq as the language model backend.
- The RAG index is reused from the terminal project.
- Use this app to show students a web-based AI tutor experience.
