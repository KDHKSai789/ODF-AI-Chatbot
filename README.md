# ODF AI Chatbot

An offline AI-powered document question answering system that allows users to upload PDF documents and ask questions using a local Large Language Model (LLM) through Ollama.

---

## Features

- User login authentication
- Upload multiple PDF documents
- Automatic text extraction from PDFs
- OCR support for scanned PDFs using Tesseract
- Semantic search using sentence embeddings
- ChromaDB vector database
- Local AI inference using Ollama
- Source citation with page numbers
- Offline operation (No OpenAI API required)

---

## Tech Stack

### Backend
- Python
- FastAPI

### Frontend
- HTML
- CSS
- JavaScript

### AI & Machine Learning
- Ollama
- Sentence Transformers
- BAAI/bge-small-en-v1.5

### Database
- SQLite
- ChromaDB

### PDF Processing
- PyMuPDF (fitz)
- PyTesseract
- Pillow

---

## Project Structure

```
odf_ai_chatbot/
│
├── app.py
├── chatbot.py
├── database.py
├── config.py
├── requirements.txt
│
├── templates/
│   ├── login.html
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── uploads/
│
├── knowledge/
│   └── chroma/
│
└── database.db
```

---

## Working

### 1. User Login

The user logs into the application using a username and password stored in the SQLite database.

Default credentials:

```
Username : admin
Password : admin123
```

---

### 2. Upload PDF

Users can upload one or more PDF documents.

The application:

- Saves the PDF
- Extracts text
- Uses OCR if required
- Splits the text into overlapping chunks

---

### 3. Embedding Generation

Each chunk is converted into a semantic embedding using

```
BAAI/bge-small-en-v1.5
```

The embeddings are stored inside ChromaDB together with metadata such as

- File name
- Page number
- Document hash

---

### 4. Semantic Search

When the user asks a question

- The question is converted into an embedding
- ChromaDB retrieves similar document chunks
- Custom ranking improves retrieval accuracy

Ranking uses

- Word overlap
- Exact phrase boost
- Short question boost

---

### 5. AI Response

The retrieved document context is sent to Ollama.

The local language model generates the answer strictly from the uploaded documents.

The answer together with document sources is returned to the user.

---

## Installation

Install the project

Create virtual environment

```bash
python3 -m venv .venv
```

Activate environment

Linux

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Install Tesseract OCR

Ubuntu

```bash
sudo apt install tesseract-ocr
```

Install Ollama

Download from

https://ollama.com

Install the required model

```bash
ollama pull gemma3:4b
```

or

```bash
ollama pull qwen2.5:7b
```

Run Ollama

```bash
ollama serve
```

Run the application

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Open

```
http://localhost:8000
```

---

## Default Login

```
Username : admin
Password : admin123
```

---

## Main Libraries

- FastAPI
- Uvicorn
- ChromaDB
- Sentence Transformers
- PyMuPDF
- Pillow
- PyTesseract
- SQLite
- Ollama

---

## Future Improvements

- Multiple user accounts
- Role-based authentication
- Chat history
- Support for DOCX and TXT files
- Streaming AI responses
- Voice input
- Better ranking algorithms
- Hybrid keyword + vector search

---

## Author

K. Dindi Hemanth Kumar

B.Tech Computer Science and Engineering

Gitam University
