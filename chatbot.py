import os, io, hashlib, requests
import fitz, chromadb, pytesseract
from PIL import Image
from sentence_transformers import SentenceTransformer
from config import UPLOAD_FOLDER, CHROMA_FOLDER, OLLAMA_URL, EMBED_MODEL, TOP_K

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CHROMA_FOLDER, exist_ok=True)

print("Loading embedding model...")
embedder = SentenceTransformer(EMBED_MODEL)
print("Embedding model loaded.")

client = chromadb.PersistentClient(path=CHROMA_FOLDER)
collection = client.get_or_create_collection("knowledge")


def get_models():
    try:
        return [m["name"] for m in requests.get(f"{OLLAMA_URL}/tags").json()["models"]]
    except (requests.RequestException, KeyError, ValueError):
        return []


def file_hash(filepath):
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            sha.update(chunk)
    return sha.hexdigest()


def split_text(text, chunk_size=120, overlap=30):
    words = " ".join(text.split()).split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks


def read_page(page):
    text = page.get_text("text")
    if len(text.strip()) > 30:
        return " ".join(text.split())
    image = Image.open(io.BytesIO(page.get_pixmap(dpi=300).tobytes("png")))
    return " ".join(pytesseract.image_to_string(image).split())


def upload_pdf(filepath):
    filename = os.path.basename(filepath)
    pdf_hash = file_hash(filepath)

    if any(m["hash"] == pdf_hash for m in collection.get().get("metadatas", [])):
        return "PDF already exists."

    print("Reading PDF...")
    doc = fitz.open(filepath)
    chunk_id = 0

    for page_no, page in enumerate(doc):
        print(f"Page {page_no+1}/{len(doc)}")
        for chunk in split_text(read_page(page)):
            collection.add(
                ids=[f"{pdf_hash}_{chunk_id}"],
                embeddings=[embedder.encode(chunk, normalize_embeddings=True).tolist()],
                documents=[chunk],
                metadatas=[{
                    "file": filename,
                    "page": page_no + 1,
                    "hash": pdf_hash
                }]
            )
            chunk_id += 1

    return "PDF uploaded successfully."


def search(question):
    embedding = embedder.encode(question, normalize_embeddings=True).tolist()
    results = collection.query(query_embeddings=[embedding], n_results=20)

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    q_words = set(question.lower().split())
    q_lower = question.lower()
    short = len(question.split()) <= 4

    def score(doc):
        d = doc.lower()
        s = len(q_words & set(d.split()))
        s += d.count(q_lower) * 5
        if short:
            s += sum(d.count(w) * 2 for w in q_words)
        return s

    ranked = sorted(zip(docs, metas), key=lambda x: score(x[0]), reverse=True)

    context_parts = []
    sources = set()
    used = set()

    for doc, meta in ranked:
        if doc in used:
            continue
        used.add(doc)
        context_parts.append(doc)
        sources.add(f'{meta["file"]} (Page {meta["page"]})')
        if len(used) >= TOP_K:
            break

    return "\n\n".join(context_parts), sorted(sources)


def ask_ollama(question, model):
    context, sources = search(question)

    prompt = f"""You are ODF AI Assistant.

Answer ONLY from the provided document context.

Rules:
1. Never use outside knowledge.
2. Never guess.
3. If the answer is not clearly available in the documents, reply exactly:
"I couldn't find this information in the uploaded documents."
4. Combine relevant information from multiple retrieved sections.
5. Prefer specific information over general information.
6. Do not mix names, dates, numbers, roles, designations or values from different sections.
7. If the context contains conflicting information, mention both.
8. If a term, abbreviation, acronym, designation, product name or role is mentioned but not explicitly defined, state that it is not defined in the uploaded documents.
9. Keep answers concise, factual and easy to understand.

DOCUMENT CONTEXT:

{context}

QUESTION:

{question}

ANSWER:"""

    answer = requests.post(
        f"{OLLAMA_URL}/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    ).json()["response"]

    return answer, sources
