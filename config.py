import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SECRET_KEY = "a-very-secret-key"

EMBEDDINGS_PATH = os.path.join(BASE_DIR, "data", "pdf_embeddings.index")
CHUNKS_PATH = os.path.join(BASE_DIR, "data", "pdf_chunks.pkl")
PDF_PATH = os.path.join(BASE_DIR, "manuals", "my_manual.pdf")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

SYSTEM_INSTRUCTION = "You are an assistant with knowledge of the samsung galaxy phone that talks like a pirate."
STARTING_MESSAGE = "Arrr, how can I help ye today?"
