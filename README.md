# ODF AI Chatbot

ODF AI Chatbot is an offline document question-answering system that allows users to upload PDF documents and ask questions about their contents using a locally running Large Language Model (LLM).

Instead of sending documents or questions to a cloud AI service, the system processes documents locally, generates semantic embeddings, stores them in a local vector database, retrieves relevant document sections, and uses Ollama to generate answers from the retrieved context.

## Features

- User login authentication
- Multiple PDF document upload
- Automatic PDF text extraction
- OCR support for scanned PDFs
- Semantic document search
- Local vector database using ChromaDB
- Sentence-transformer embeddings
- Local LLM inference using Ollama
- Source tracking with document names and page numbers
- Duplicate PDF detection using SHA-256 hashing
- Context-based question answering
- Answers restricted to uploaded document content
- No OpenAI API or cloud LLM required

## How It Works

The system follows a Retrieval-Augmented Generation (RAG) style pipeline.

    User
      |
      v
    Login
      |
      v
    Upload PDF
      |
      v
    PDF Text Extraction
      |
      +------> OCR for scanned pages
      |
      v
    Text Chunking
      |
      v
    Sentence Embeddings
      |
      v
    ChromaDB
      |
      v
    User Question
      |
      v
    Semantic Search
      |
      v
    Additional Ranking
      |
      v
    Relevant Document Context
      |
      v
    Ollama Local LLM
      |
      v
    Answer + Sources

## Document Processing Pipeline

### 1. PDF Upload

Users can upload multiple PDF documents through the web interface.

Each uploaded document is stored locally and processed by the chatbot backend.

### 2. PDF Text Extraction

The application uses PyMuPDF to extract text from each PDF page.

If a page contains insufficient extractable text, the application renders the page as an image and performs OCR using Tesseract.

This allows the system to process both normal text-based PDFs and scanned documents.

### 3. Text Chunking

Extracted text is cleaned and divided into smaller overlapping chunks.

The current implementation uses:

- Chunk size: 120 words
- Overlap: 30 words

Overlapping chunks help preserve context between neighboring sections.

### 4. Embedding Generation

Each text chunk is converted into a semantic vector using:

    BAAI/bge-small-en-v1.5

The embeddings allow the system to search for document content based on semantic similarity rather than only exact keyword matches.

### 5. Vector Storage

The generated embeddings are stored in a local ChromaDB collection.

Each stored chunk contains metadata including:

- Original file name
- PDF page number
- SHA-256 document hash

### 6. Semantic Search

When a user asks a question, the question is converted into an embedding and compared against the stored document embeddings.

The system initially retrieves multiple candidate chunks from ChromaDB.

Additional ranking is then applied using:

- Word overlap
- Exact phrase matching
- Short-question boosting

The highest-ranked document sections are selected as the final context.

### 7. Local AI Generation

The selected document context is sent to a locally running Ollama model.

The model is instructed to answer only using the retrieved document context.

The system also instructs the model to:

- Avoid outside knowledge
- Avoid guessing
- Mention when information is unavailable
- Combine relevant sections
- Preserve conflicting information when present
- Keep answers concise and factual

### 8. Source Information

The application returns the document sources associated with the retrieved context.

Sources contain the original PDF filename and page number.

This allows users to identify where the answer came from.

## Technologies Used

### Backend

- Python
- FastAPI
- Uvicorn

### Artificial Intelligence

- Ollama
- Sentence Transformers
- BAAI/bge-small-en-v1.5

### Retrieval & Vector Database

- ChromaDB
- Semantic embeddings
- Custom document ranking

### PDF Processing

- PyMuPDF
- Tesseract OCR
- PyTesseract
- Pillow

### Database

- SQLite

### Frontend

- HTML
- CSS
- JavaScript
- Jinja2 templates

## Project Structure

    ODF-AI-Chatbot/
    |
    ├── app.py
    ├── chatbot.py
    ├── config.py
    ├── database.py
    ├── database.db
    ├── requirements.txt
    ├── README.md
    |
    ├── static/
    │   ├── script.js
    │   └── style.css
    |
    └── templates/
        ├── index.html
        └── login.html

The following directories are created/used by the application during execution:

    uploads/
    knowledge/
        └── chroma/

## Main Components

### app.py

The main FastAPI application.

Responsibilities include:

- Starting the web application
- Handling user login
- Managing sessions
- Serving HTML pages
- Handling PDF uploads
- Processing user questions
- Returning AI answers and document sources
- Handling logout

### chatbot.py

The core document intelligence module.

Responsibilities include:

- Loading the embedding model
- Initializing ChromaDB
- Processing PDF documents
- Performing OCR
- Generating embeddings
- Searching document chunks
- Ranking retrieved results
- Communicating with Ollama
- Generating document-grounded answers

### database.py

Handles SQLite database operations.

The database stores user authentication information and provides the login functionality.

### config.py

Contains application configuration including:

- Upload directory
- ChromaDB directory
- Ollama API address
- Embedding model
- Number of retrieved document chunks

### templates/

Contains the HTML pages used by the web interface.

    login.html
    index.html

### static/

Contains frontend resources.

    style.css
    script.js

### database.db

SQLite database used for user authentication.

## Requirements

Before running the project, make sure you have:

- Python 3
- pip
- Tesseract OCR
- Ollama
- An Ollama-compatible local language model
- Sufficient disk space for the embedding model and document database

The Python dependencies are listed in:

    requirements.txt

## Installation

### 1. Clone the Repository

    git clone https://github.com/KDHKSai789/ODF-AI-Chatbot.git

### 2. Enter the Project Directory

    cd ODF-AI-Chatbot

### 3. Create a Virtual Environment

Linux/macOS:

    python3 -m venv .venv

Windows:

    python -m venv .venv

### 4. Activate the Virtual Environment

Linux/macOS:

    source .venv/bin/activate

Windows:

    .venv\Scripts\activate

### 5. Install Python Dependencies

    pip install -r requirements.txt

## Install Tesseract OCR

Tesseract is used when a PDF page does not contain enough extractable text.

### Ubuntu/Debian

    sudo apt update
    sudo apt install tesseract-ocr

Verify the installation:

    tesseract --version

## Install Ollama

ODF AI Chatbot uses Ollama to run the language model locally.

Install Ollama according to your operating system.

After installation, verify it with:

    ollama --version

Start the Ollama service:

    ollama serve

Keep Ollama running while using the chatbot.

## Download a Local AI Model

For example:

    ollama pull gemma3:4b

You can also use another model that is available in your Ollama installation.

The available models are detected by the application through the Ollama API.

## Running the Application

### 1. Enter the Project Directory

    cd ODF-AI-Chatbot

### 2. Activate the Virtual Environment

Linux/macOS:

    source .venv/bin/activate

### 3. Start Ollama

In a separate terminal:

    ollama serve

### 4. Start the FastAPI Application

From the project directory:

    uvicorn app:app --host 0.0.0.0 --port 8000

The application will start on:

    http://127.0.0.1:8000

### 5. Open the Web Interface

Open a browser and visit:

    http://localhost:8000

## Login

The current database contains a default administrator account:

    Username: admin
    Password: admin123

For production use, the default credentials should be changed and passwords should be securely hashed.

## Using the Application

### Step 1: Login

Open the application and log in using the available credentials.

### Step 2: Upload Documents

Upload one or more PDF documents.

The application processes each document and stores its searchable representation locally.

### Step 3: Select an Ollama Model

The application retrieves the available Ollama models and makes them available for answering questions.

### Step 4: Ask a Question

Enter a question related to the uploaded documents.

The system will:

1. Convert the question into an embedding.
2. Search the ChromaDB knowledge base.
3. Retrieve relevant document sections.
4. Rank the retrieved sections.
5. Build document context.
6. Send the context to the selected Ollama model.
7. Generate a document-grounded answer.
8. Return the answer with document sources.

## Privacy

The project is designed around local document processing and local AI inference.

Documents are processed locally, embeddings are stored in a local ChromaDB database, and the language model is accessed through the local Ollama API.

No OpenAI API key is required.

## Duplicate Document Detection

Uploaded PDFs are hashed using SHA-256.

If the same document has already been processed, the system detects the existing hash and avoids processing the document again.

This helps prevent duplicate document entries in the knowledge base.

## Configuration

Application settings are defined in:

    config.py

Current configuration includes:

    OLLAMA_URL = "http://localhost:11434/api"

    EMBED_MODEL = "BAAI/bge-small-en-v1.5"

    TOP_K = 3

The upload and ChromaDB storage directories are also configured in this file.

## API Routes

The FastAPI application currently provides routes for:

    GET  /
    POST /login
    GET  /home
    POST /upload
    POST /ask
    GET  /logout

These routes handle authentication, document processing, question answering, and session management.

## Important Notes

### Local AI Model

The chatbot requires Ollama to be running locally.

If Ollama is not running, the application cannot retrieve available models or generate answers.

### OCR

Tesseract is required for scanned PDFs or PDF pages where normal text extraction is insufficient.

### First Startup

The sentence-transformer embedding model may need to be downloaded the first time the application starts.

After the model is available locally, subsequent startups can reuse it.

## Limitations

- Currently focused on PDF documents
- Requires a locally installed Ollama model
- OCR depends on Tesseract
- Authentication currently uses a default account
- User passwords are stored directly in the SQLite database
- No persistent chat history
- No multi-user management
- No real-time streaming responses

## Future Improvements

- Secure password hashing
- Multiple user accounts
- Role-based access control
- Persistent chat history
- DOCX and TXT document support
- Streaming AI responses
- Hybrid keyword + vector retrieval
- Improved document ranking
- Document management and deletion
- Conversation history
- Better authentication and session security
- Support for additional local LLM providers

## Purpose

ODF AI Chatbot demonstrates how document question answering can be implemented using local AI technologies.

The project combines:

    PDF Processing
          +
    OCR
          +
    Semantic Embeddings
          +
    Vector Search
          +
    Local LLM
          =
    Offline Document Question Answering

It provides an example of building a privacy-focused RAG-style application without requiring a cloud-based AI API.

## License

This project is intended for educational and development purposes.
