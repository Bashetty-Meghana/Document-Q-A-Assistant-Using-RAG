from pathlib import Path
import json

import faiss
import numpy as np
import ollama
import streamlit as st
from sentence_transformers import SentenceTransformer


# -----------------------------
# Project paths & Settings
# -----------------------------
VECTOR_DB_DIR = Path("vector_db")
DOCUMENTS_DIR = Path("documents")

INDEX_FILE = VECTOR_DB_DIR / "faiss.index"
METADATA_FILE = VECTOR_DB_DIR / "metadata.json"

MODEL_NAME = "llama3.2:3b"


# -----------------------------
# Load RAG resources
# -----------------------------
@st.cache_resource
def load_rag_resources():
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    index = faiss.read_index(str(INDEX_FILE))

    with open(METADATA_FILE, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    return embedding_model, index, chunks


# -----------------------------
# Retrieve relevant chunks
# -----------------------------
def retrieve_chunks(question, embedding_model, index, chunks, top_k=5):
    query_embedding = embedding_model.encode([question], normalize_embeddings=True)
    query_embedding = np.array(query_embedding, dtype="float32")

    scores, indices = index.search(query_embedding, top_k)

    results = []
    for score, index_number in zip(scores[0], indices[0]):
        if index_number == -1:
            continue

        result = chunks[index_number].copy()
        result["score"] = float(score)
        results.append(result)

    return results


# -----------------------------
# Generate answer using local Llama 3.2
# -----------------------------
def generate_answer(question, retrieved_chunks):
    context_parts = []
    for chunk in retrieved_chunks:
        context_parts.append(
            f"Source: {chunk['source']}\n"
            f"Page: {chunk['page']}\n"
            f"Content:\n{chunk['text']}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""You are a document question-answering assistant.

Answer the user's question using ONLY the information provided in the context below.

If the answer cannot be found in the context, say:
"I could not find the answer in the provided documents."

Do not use outside knowledge.
Use all relevant information from the context to answer the question.
If the question asks for multiple items, include all relevant items supported by the context.
Keep the answer clear and concise.

Context:
{context}

Question:
{question}

Answer:
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


# -----------------------------
# Streamlit Application Layout
# -----------------------------
st.set_page_config(
    page_title="Document Q&A Assistant (RAG)",
    page_icon="📚",
    layout="wide"
)

# Sidebar
with st.sidebar:
    st.header("ℹ️ Project Information")
    st.markdown("""
    **Document Q&A Assistant Using RAG**
    - **LLM**: Local Llama 3.2 (3B via Ollama)
    - **Embeddings**: `all-MiniLM-L6-v2`
    - **Vector Store**: FAISS
    """)

    st.divider()

    st.subheader("📄 Loaded Documents")
    pdf_files = sorted(DOCUMENTS_DIR.glob("*.pdf")) if DOCUMENTS_DIR.exists() else []
    if pdf_files:
        for pdf in pdf_files:
            st.markdown(f"• `{pdf.name}`")
    else:
        st.write("No PDF documents found in `documents/` folder.")

    st.divider()
    st.caption("🔒 100% Local & Offline — No Cloud API required.")


# Main App Title & Description
st.title("📚 Document Question-Answering Assistant")
st.markdown("Ask plain-language questions about your loaded PDF documents. Answers are strictly grounded in retrieved sources.")

# Load resources
try:
    embedding_model, index, chunks = load_rag_resources()
    st.success(f"System ready! Index contains **{len(chunks)}** text chunks.", icon="✅")
except Exception as e:
    st.error(f"Error loading vector database: {e}. Please run `python build_index.py` first.")
    st.stop()

# User Question Input
col1, col2 = st.columns([4, 1])

with col1:
    question = st.text_input(
        "Enter your question:",
        placeholder="e.g., What are the revised grievance redressal timelines under the IT Rules?"
    )

with col2:
    st.write("")
    st.write("")
    clear_button = st.button("Clear Input", use_container_width=True)

if clear_button:
    st.rerun()

# Sample Questions Helper
with st.expander("💡 Sample Questions for Viva & Testing"):
    st.markdown("""
    1. *What are the revised grievance redressal timelines under the IT Rules?*
    2. *What is stated in Rule 3(3) of the IT Rules, 2021?*
    3. *What are the main objectives of the Government of India Open Source Software Policy?*
    4. *What are the benefits of using Open Source Software (OSS) in e-Governance?*
    5. *What are the key applications of Generative AI?*
    6. *What is Artificial Intelligence according to the introductory documents?*
    """)

# Process Question
if question:
    with st.spinner("Searching documents and generating grounded answer..."):
        retrieved_chunks = retrieve_chunks(
            question,
            embedding_model,
            index,
            chunks,
            top_k=5
        )

        answer = generate_answer(
            question,
            retrieved_chunks
        )

    # Display Answer
    st.subheader("💡 Answer")
    st.info(answer)

    # Display Sources
    st.subheader("📍 Retrieved Sources")
    
    # Group unique sources
    unique_sources = set()
    for chunk in retrieved_chunks:
        unique_sources.add((chunk['source'], chunk['page']))

    st.markdown("**Source Pages Cited:**")
    for doc_name, page_num in sorted(unique_sources):
        st.markdown(f"- 📄 **{doc_name}** — Page {page_num}")

    with st.expander("🔍 View Retrieved Text Chunks (Raw Context)"):
        for i, chunk in enumerate(retrieved_chunks, start=1):
            st.markdown(f"**Chunk {i}** — `{chunk['source']}` (Page {chunk['page']}) | Similarity Score: `{chunk['score']:.4f}`")
            st.text(chunk['text'])
            st.divider()