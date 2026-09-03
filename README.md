# 📚 Document Question-Answering Assistant Using RAG

An end-to-end, 100% local **Retrieval-Augmented Generation (RAG)** application built using open-source tools. Ask plain-language questions against domain PDF documents and receive precise, context-grounded answers with exact source document and page citations.

---

## 📌 Project Overview & Objectives

Traditional keyword search across dense corporate documents, policy manuals, and textbooks is time-consuming and inefficient. Standard Large Language Models (LLMs) can generate fluent responses but lack direct access to private/local documents and often suffer from hallucinations.

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline to solve these challenges:
- **Zero Cloud API Costs**: Runs 100% locally on a standard laptop without OpenAI, Gemini, or paid services.
- **Strict Grounding**: The local LLM is constrained to answer **ONLY** from retrieved document context, preventing hallucinated answers.
- **Source Verification**: Every answer includes explicit document titles and page number citations for easy auditing.

---

## 🛠️ Technology Stack

| Layer | Technology / Library | Purpose |
| --- | --- | --- |
| **Language** | Python 3.13 | Core runtime environment |
| **Document Processing** | PyPDF2 | PDF text extraction and metadata tracking |
| **Embeddings** | `sentence-transformers` (`all-MiniLM-L6-v2`) | Generates dense 384-dimensional semantic embeddings |
| **Vector Store** | FAISS (`IndexFlatIP`) | Fast inner-product/cosine similarity vector search |
| **Local LLM Engine** | Ollama (`llama3.2:3b`) | Quantized local language model inference |
| **User Interface** | Streamlit | Web chat application interface |
| **Data Analysis** | pandas | Evaluation data processing |

---

## 🏗️ System Architecture & Workflow

```
[ PDF Documents ] (documents/*.pdf)
       │
       ▼
[ PyPDF2 Extraction & Sanitization ]
       │
       ▼
[ Sliding-Window Chunking (700 chars, 150 overlap) ]
       │
       ▼
[ SentenceTransformer (all-MiniLM-L6-v2) ] ──► [ FAISS Index (vector_db/) ]
                                                         │
                                                         ▼
[ User Question ] ──► [ Query Vector ] ──► [ Cosine Similarity Search (Top 5 Chunks) ]
                                                         │
                                                         ▼
                                       [ Grounded Prompt Construction ]
                                                         │
                                                         ▼
                                       [ Local Llama 3.2 (via Ollama) ]
                                                         │
                                                         ▼
                                       [ Answer & Source Page Citations UI ]
```

---

## 📁 Repository Structure

```
Document_QA_RAG/
├── documents/                  # Repository of PDF documents
│   ├── Artificial_intelligence.pdf
│   ├── fqa.pdf
│   ├── Generative_AI.pdf
│   ├── kecs111.pdf
│   ├── Machine_learning.pdf
│   └── Policy-Document.pdf
├── vector_db/                  # FAISS Index and chunk metadata
│   ├── faiss.index
│   └── metadata.json
├── app.py                      # Streamlit frontend application
├── build_index.py              # PDF extraction, chunking, and FAISS indexing pipeline
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git exclusion rules
├── test_set.csv                # 15 evaluation questions and expected answers
├── test_results.csv            # Per-question empirical evaluation results
├── RAG_Project_Report.docx     # Comprehensive 2-3 page formal project report
└── README.md                   # Project documentation & viva guide
```

---

## 🚀 Step-by-Step Setup & Installation Guide

### Prerequisites
- Windows 10/11 with PowerShell
- Python 3.10+ (tested on Python 3.13)
- [Ollama](https://ollama.com/) installed on Windows

---

### Step 1: Clone or Navigate to Project Directory
Open PowerShell and navigate to the project directory:
```powershell
cd c:\Users\cnuba\Downloads\Document_QA_RAG
```

---

### Step 2: Create and Activate Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

---

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

---

### Step 4: Install and Pull Local LLM Model via Ollama
Ensure the Ollama application is running on your system, then open PowerShell and run:
```powershell
ollama pull llama3.2:3b
```
To verify model installation:
```powershell
ollama list
```

---

### Step 5: Build Vector Database (Indexing)
Process all PDF documents in `documents/`, create embeddings, and build the local FAISS index:
```powershell
python build_index.py
```
*Expected Output:*
```
Found 6 PDF files.
Processing: Artificial_intelligence.pdf ...
Processing: Policy-Document.pdf ...
Total chunks created: 1793
Loading embedding model...
Creating embeddings...
Embedding shape: (1793, 384)
--------------------------------
FAISS database created successfully!
--------------------------------
```

---

### Step 6: Launch Streamlit Web Application
```powershell
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Evaluation & Quality Results

A 15-question test benchmark was evaluated against the RAG system to assess retrieval relevance, answer accuracy, and factual grounding.

| Metric | Performance |
| --- | --- |
| **Total Test Questions** | 15 |
| **Passed (Fully Grounded & Correct)** | 15 / 15 (100%) |
| **Failed / Hallucinated** | 0 |
| **Out-of-Scope Detection** | Passed (Correctly stated answer unavailable) |

The complete empirical results can be inspected in [`test_results.csv`](file:///c:/Users/cnuba/Downloads/Document_QA_RAG/test_results.csv).

---

## 💡 Sample Questions for Demonstration

1. **Policy Timelines**: *"What are the revised grievance redressal timelines under the IT Rules?"*
2. **IT Rules Details**: *"What is stated in Rule 3(3) of the IT Rules, 2021?"*
3. **Open Source Policy**: *"What are the main objectives of the Government of India Open Source Software Policy?"*
4. **GenAI Applications**: *"What are the key applications of Generative AI?"*
5. **CS Concepts**: *"What is a compiler and how does it translate source code?"*
6. **Out-of-Scope Test**: *"What is the real-time stock price of Apple Inc. today?"* (System will respond: *"I could not find the answer in the provided documents."*)

---

## 🎓 Viva Explanation Guide (Simple Language)

When explaining this project during your viva, break it down into these simple concepts:

1. **What is RAG?**
   > *"RAG stands for Retrieval-Augmented Generation. Instead of relying on an LLM's static training memory, we retrieve relevant text passages from private PDFs first and pass them as context to the LLM so it can answer accurately with source citations."*

2. **Why do we chunk text?**
   > *"LLMs and embedding models have input token limits. Splitting documents into smaller chunks (700 characters with 150 overlap) ensures precise similarity matching and fits comfortably into the model's context window."*

3. **What is an Embedding?**
   > *"An embedding converts text into a mathematical vector of numbers (384 floating-point numbers). Texts with similar meanings end up close together in vector space."*

4. **Why use FAISS?**
   > *"FAISS (Facebook AI Similarity Search) calculates cosine similarity between the user's query vector and thousands of document chunk vectors in milliseconds to find the top-5 closest matches."*

5. **How is hallucination prevented?**
   > *"Our prompt strictly directs Llama 3.2 to use ONLY the retrieved context. If the answer isn't in the chunks, it explicitly responds that it cannot find the answer."*

---

## ⚠️ System Limitations & Future Enhancements

- **PDF Parsing**: PyPDF2 extracts plain text; tables and images embedded inside PDFs are not parsed into structured tables.
- **Hardware Speed**: Response time depends on CPU/RAM speed when executing local Llama 3.2 inference.
- **Future Enhancements**: Hybrid Search combining BM25 keyword search with FAISS dense vector retrieval.

---

## 📜 License & Compliance

This project is created strictly using open-source, non-proprietary software tools for academic capstone purposes.
