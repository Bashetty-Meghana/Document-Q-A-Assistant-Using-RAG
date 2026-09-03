# Document Question-Answering Assistant Using RAG

An end-to-end local **Retrieval-Augmented Generation (RAG)** application built using open-source tools. Ask plain-language questions against domain PDF documents and receive precise, context-grounded answers with exact source document and page citations.

---

## 📌 Project Overview & Features

- **100% Local Execution**: Runs entirely on a local machine using open-source tools. Requires no paid APIs, cloud services, or external accounts.
- **Strict Fact Grounding**: Constrained to answer exclusively using retrieved document context. Automatically indicates when information is unavailable in the document set.
- **Source Page Verification**: Displays source document names and page numbers for every generated answer.
- **Interactive UI**: Built with Streamlit, providing an intuitive chat interface, document list sidebar, and sample query helpers.

---

## 🛠️ Technology Stack

| Layer | Tool / Library | Description |
| --- | --- | --- |
| **Language** | Python 3.13 | Core programming language |
| **Document Loader** | PyPDF2 | PDF text extraction and page metadata tracking |
| **Embeddings** | `sentence-transformers` (`all-MiniLM-L6-v2`) | Generates dense 384-dimensional vector embeddings |
| **Vector Store** | FAISS (`IndexFlatIP`) | High-performance vector similarity search |
| **Local LLM Engine** | Ollama (`llama3.2:3b`) | Quantized local language model inference |
| **Web Interface** | Streamlit | Web frontend application framework |
| **Data Processing** | pandas | Data handling and evaluation metrics |

---

## 🏗️ System Architecture

```
[ PDF Documents ] (documents/*.pdf)
       │
       ▼
[ PyPDF2 Extraction & Text Cleaning ]
       │
       ▼
[ Sliding-Window Chunking (700 chars, 150 overlap) ]
       │
       ▼
[ SentenceTransformer (all-MiniLM-L6-v2) ] ──► [ FAISS Index (vector_db/) ]
                                                         │
                                                         ▼
[ User Question ] ──► [ Query Vector ] ──► [ Cosine Similarity Search (Top-5 Chunks) ]
                                                         │
                                                         ▼
                                       [ Grounded Context Prompt ]
                                                         │
                                                         ▼
                                       [ Local Llama 3.2 (via Ollama) ]
                                                         │
                                                         ▼
                                       [ Answer & Source Citations UI ]
```

---

## 📁 Repository Structure

```
Document_QA_RAG/
├── documents/                  # Directory containing input PDF documents
│   ├── Artificial_intelligence.pdf
│   ├── fqa.pdf
│   ├── Generative_AI.pdf
│   ├── kecs111.pdf
│   ├── Machine_learning.pdf
│   └── Policy-Document.pdf
├── vector_db/                  # FAISS index and chunk metadata
│   ├── faiss.index
│   └── metadata.json
├── app.py                      # Streamlit web application
├── build_index.py              # Document processing, embedding, and indexing script
├── requirements.txt            # Python dependencies list
├── .gitignore                  # Git exclusion rules
├── test_set.csv                # 15 evaluation benchmark questions
├── test_results.csv            # Detailed evaluation test matrix
├── RAG_Project_Report.docx     # Formal project report document
└── README.md                   # Project documentation
```

---

## 🚀 Setup & Execution Guide

### Prerequisites
- Windows 10/11 with PowerShell
- Python 3.10+
- [Ollama](https://ollama.com/) installed and running locally

---

### Step 1: Install Dependencies
Open PowerShell in the project root directory:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

### Step 2: Download Local LLM Model
```powershell
ollama pull llama3.2:3b
```

---

### Step 3: Build Vector Database Index
Process all PDF documents in `documents/` and generate the FAISS vector index:
```powershell
python build_index.py
```

---

### Step 4: Run Streamlit Web Application
```powershell
streamlit run app.py
```
Access the application in your web browser at `http://localhost:8501`.

---

## 🧪 Evaluation Results

The system was evaluated against a 15-question benchmark covering all domain documents, policy timelines, and out-of-scope queries:

| Metric | Result |
| --- | --- |
| **Total Test Questions** | 15 |
| **Passed (Grounded & Correct)** | 15 / 15 (100%) |
| **Hallucination Rate** | 0% |
| **Out-of-Scope Handling** | Passed |

Refer to [`test_results.csv`](file:///c:/Users/cnuba/Downloads/Document_QA_RAG/test_results.csv) for full evaluation output.

---

## 💡 Sample Test Questions

1. **Grievance Timelines**: *"What are the revised grievance redressal timelines under the IT Rules?"*
2. **IT Rules Details**: *"What is stated in Rule 3(3) of the IT Rules, 2021?"*
3. **Open Source Policy**: *"What are the main objectives of the Government of India Open Source Software Policy?"*
4. **GenAI Applications**: *"What are the key applications of Generative AI?"*
5. **Computer Science**: *"What is a compiler and how does it translate source code?"*
6. **Out-of-Scope Test**: *"What is the real-time stock price of Apple Inc. today?"* *(Expected: Answer unavailable)*

---

## ⚠️ System Limitations

- **Text Extraction**: PyPDF2 extracts plain text; complex nested tables or figures in PDFs are not parsed as structured tables.
- **Hardware Performance**: Local LLM inference speed depends on available system CPU and memory resources.
