import os

# ==========================
# Folders
# ==========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

CHROMA_FOLDER = os.path.join(
    BASE_DIR,
    "knowledge",
    "chroma"
)

# ==========================
# Ollama
# ==========================

OLLAMA_URL = "http://localhost:11434/api"

# ==========================
# Embedding Model
# ==========================

EMBED_MODEL = "BAAI/bge-small-en-v1.5"

# ==========================
# Search
# ==========================

TOP_K = 3
