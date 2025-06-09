import os, pickle, fitz, faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from config import *

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def load_pdf_text(path):
    doc = fitz.open(path)
    return "\n".join(page.get_text() for page in doc)

def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    words = text.split()
    return [" ".join(words[i:i + size]) for i in range(0, len(words), size - overlap)]

def save_index_and_chunks(index, chunks):
    faiss.write_index(index, EMBEDDINGS_PATH)
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)

def load_index_and_chunks():
    if os.path.exists(EMBEDDINGS_PATH) and os.path.exists(CHUNKS_PATH):
        index = faiss.read_index(EMBEDDINGS_PATH)
        with open(CHUNKS_PATH, "rb") as f:
            chunks = pickle.load(f)
        return index, chunks
    return None, None

def build_or_load_index():
    index, chunks = load_index_and_chunks()
    if index and chunks:
        return index, chunks
    text = load_pdf_text(PDF_PATH)
    chunks = chunk_text(text)
    embeddings = embed_model.encode(chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    save_index_and_chunks(index, chunks)
    return index, chunks

def get_relevant_chunks(query, index, chunks, top_k=3):
    query_embedding = embed_model.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)
    return [chunks[i] for i in indices[0]]
