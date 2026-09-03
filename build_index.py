from pathlib import Path
import json
import re

import faiss
import numpy as np
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer


# -----------------------------
# Project paths
# -----------------------------
DOCUMENTS_DIR = Path("documents")
VECTOR_DB_DIR = Path("vector_db")

INDEX_FILE = VECTOR_DB_DIR / "faiss.index"
METADATA_FILE = VECTOR_DB_DIR / "metadata.json"


# -----------------------------
# Settings
# -----------------------------
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

CHUNK_SIZE = 700
CHUNK_OVERLAP = 150


# -----------------------------
# Clean text
# -----------------------------
def clean_text(text):
    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# -----------------------------
# Split text into chunks
# -----------------------------
def create_chunks(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):

    text = clean_text(text)

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


# -----------------------------
# Load all PDF documents
# -----------------------------
def load_documents():

    all_chunks = []

    pdf_files = sorted(DOCUMENTS_DIR.glob("*.pdf"))

    print(f"Found {len(pdf_files)} PDF files.")

    for pdf_file in pdf_files:

        print(f"\nProcessing: {pdf_file.name}")

        reader = PdfReader(str(pdf_file))

        print(f"Pages: {len(reader.pages)}")

        for page_number, page in enumerate(reader.pages, start=1):

            text = page.extract_text()

            if not text:
                continue

            text = clean_text(text)

            page_chunks = create_chunks(text)

            for chunk in page_chunks:

                all_chunks.append(
                    {
                        "text": chunk,
                        "source": pdf_file.name,
                        "page": page_number
                    }
                )

    return all_chunks


# -----------------------------
# Create FAISS database
# -----------------------------
def build_index():

    VECTOR_DB_DIR.mkdir(exist_ok=True)

    print("\nLoading documents...")

    chunks = load_documents()

    print(f"\nTotal chunks created: {len(chunks)}")

    if not chunks:
        print("No text chunks were created.")
        return

    print("\nLoading embedding model...")

    model = SentenceTransformer(EMBEDDING_MODEL)

    texts = [chunk["text"] for chunk in chunks]

    print("\nCreating embeddings...")

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    print(f"Embedding shape: {embeddings.shape}")

    # Inner product works as cosine similarity
    # because embeddings are normalized.
    index = faiss.IndexFlatIP(
        embeddings.shape[1]
    )

    index.add(embeddings)

    # Save FAISS index
    faiss.write_index(
        index,
        str(INDEX_FILE)
    )

    # Save metadata
    with open(
        METADATA_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            chunks,
            file,
            ensure_ascii=False,
            indent=2
        )

    print("\n--------------------------------")
    print("FAISS database created successfully!")
    print("--------------------------------")

    print(f"Index: {INDEX_FILE}")
    print(f"Metadata: {METADATA_FILE}")
    print(f"Total chunks: {len(chunks)}")


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    build_index()