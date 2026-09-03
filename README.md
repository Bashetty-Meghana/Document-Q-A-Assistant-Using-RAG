# Document Q&A Assistant Using RAG

An end-to-end local **Retrieval-Augmented Generation (RAG)** application built using open-source tools. Ask plain-language questions against domain PDF documents and receive precise, context-grounded answers with exact source document and page citations.

---

## 1. Project Overview
This project provides a fully offline, local document question-answering assistant. Organizations often store critical knowledge across lengthy policy manuals, FAQs, and textbooks. This assistant enables users to query these local PDF documents in natural language, retrieving relevant passages and generating grounded answers without sending data to external cloud services.

## 2. Problem Statement
Searching through hundreds of pages of PDF documents manually is time-consuming and inefficient. While standard Large Language Models (LLMs) can answer queries, they lack access to private offline documents and frequently hallucinate. This project addresses both issues by combining semantic document retrieval with strict prompt grounding on a local language model.

## 3. Objectives
- Extract and chunk text from local PDF documents while preserving source page metadata.
- Convert text chunks into dense vector embeddings using open-source sentence-transformers.
- Build and query a local FAISS vector database to retrieve top matching document passages.
- Generate grounded, factual responses using a local Llama 3.2 (3B) model via Ollama.
- Provide an intuitive Streamlit web interface displaying generated answers and exact source citations.

## 4. Features
- **100% Local Execution**: Operates entirely offline without cloud APIs (no OpenAI, Gemini, or paid services required).
- **Strict Grounding**: Constrained to answer exclusively using retrieved document context. Automatically indicates when information is unavailable.
- **Source Verification**: Displays document file names and exact page numbers for every answer.
- **Interactive Interface**: Modern Streamlit web UI with clear buttons, document list sidebar, and sample query helpers.

## 5. Technologies Used
- **Language**: Python 3.13
- **Document Loading & Extraction**: PyPDF2
- **Embeddings**: `sentence-transformers` (`all-MiniLM-L6-v2`)
- **Vector Database**: FAISS (`IndexFlatIP`)
- **Local LLM Engine**: Ollama (`llama3.2:3b`)
- **Web Application**: Streamlit
- **Data Processing**: pandas

## 6. System Architecture
```
[ PDF Documents ] (documents/*.pdf)
       │
       ▼
[ PyPDF2 Text Extraction & Cleaning ]
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

## 7. RAG Workflow
1. **Document Ingestion**: PDFs are read page by page using PyPDF2.
2. **Text Preprocessing & Chunking**: Text is cleaned and split into overlapping 700-character segments.
3. **Vector Embedding**: Each chunk is transformed into a 384-dimensional vector using `all-MiniLM-L6-v2`.
4. **FAISS Indexing**: Normalized embeddings are indexed in FAISS (`IndexFlatIP`) for fast cosine similarity search.
5. **Retrieval**: When a query is submitted, FAISS retrieves the top-5 most relevant chunks.
6. **Local LLM Generation**: The retrieved text chunks are formatted into a strict context prompt for Ollama Llama 3.2 (3B).
7. **Display**: The generated answer and source page citations are presented in the Streamlit UI.

## 8. Dataset / Documents
The system indexes 6 open PDF documents:
- `Policy-Document.pdf` — Government IT Policy, IT Rules 2021, and Open Source Software Policy.
- `fqa.pdf` — Frequently Asked Questions regarding IT Grievance Redressal.
- `Generative_AI.pdf` — Overview of Generative AI principles and LLM architectures.
- `Artificial_intelligence.pdf` — Core concepts of AI and machine learning.
- `Machine_learning.pdf` — Supervised, unsupervised, and reinforcement learning fundamentals.
- `kecs111.pdf` — NCERT Class 11 Computer Science textbook chapter (Hardware, OS, Compilers).

## 9. Chunking Strategy
- **Chunk Size**: 700 characters
- **Chunk Overlap**: 150 characters
- **Rationale**: 700 characters captures 3–5 complete sentences, providing sufficient semantic context for the embedding model while maintaining high retrieval precision. Overlapping by 150 characters prevents boundary information loss across split chunks.

## 10. Embedding Model
- **Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Dimensions**: 384 floating-point dimensions
- **Normalization**: Vectors are L2-normalized so that inner product search (`IndexFlatIP`) corresponds to exact cosine similarity.

## 11. FAISS Retrieval
- **Index Type**: `faiss.IndexFlatIP` (Flat Inner Product)
- **Top-K**: 5 chunks retrieved per user query
- **Storage**: `vector_db/faiss.index` (2.75 MB) and `vector_db/metadata.json` (1.30 MB) tracking text content, source file names, and page numbers.

## 12. Local Llama 3.2 Model
- **Model**: `llama3.2:3b` (3 Billion parameters, quantized for laptop inference)
- **Engine**: Ollama local server
- **Grounding Rule**: Instructed to answer strictly from retrieved context and refuse out-of-scope queries with *"I could not find the answer in the provided documents."*

## 13. Ollama Setup
Ollama provides a local REST service for running open-source LLMs offline. Download Ollama for Windows from [ollama.com](https://ollama.com/).

## 14. Streamlit Application
The frontend (`app.py`) provides an interactive web chat layout featuring:
- User query text box with a clear button.
- Sidebar detailing project architecture and loaded PDF documents.
- Sample query list helper.
- Expandable raw retrieved chunk context viewer.

## 15. Project Structure
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

## 16. Installation
Clone or download the repository to your local computer.

## 17. Windows Setup
Open Windows PowerShell and navigate to the project directory:
```powershell
cd c:\Users\cnuba\Downloads\Document_QA_RAG
python -m venv venv
.\venv\Scripts\Activate.ps1
```

## 18. Dependency Installation
```powershell
pip install -r requirements.txt
```

## 19. Ollama Setup (Local LLM Server)
Ensure the Ollama application is installed and running in your Windows system tray.

## 20. Model Setup
Download the local Llama 3.2 3B model:
```powershell
ollama pull llama3.2:3b
```

## 21. Build Vector Database
Generate embeddings and build the FAISS index:
```powershell
python build_index.py
```

## 22. Run Application
Launch the Streamlit web application using the exact working command:
```powershell
streamlit run app.py --server.fileWatcherType none
```
Open `http://localhost:8501` in your browser.

## 23. Evaluation Benchmark Questions (15 Questions from test_set.csv)

### Evaluation Benchmark Set (Exact 15 Questions from test_set.csv):
1. *What are the revised grievance redressal timelines under the IT Rules?* (Source: `Policy-Document.pdf`)
2. *What is stated in Rule 3(3) of the IT Rules, 2021?* (Source: `Policy-Document.pdf`)
3. *What are the main objectives of the Government of India Open Source Software Policy?* (Source: `Policy-Document.pdf`)
4. *What are the benefits of using Open Source Software (OSS) in e-Governance?* (Source: `Policy-Document.pdf`)
5. *What are the key applications of Generative AI?* (Source: `Generative_AI.pdf`)
6. *What is Artificial Intelligence according to the introductory document?* (Source: `Artificial_intelligence.pdf`)
7. *What are the main types of Machine Learning algorithms?* (Source: `Machine_learning.pdf`)
8. *What is the difference between supervised and unsupervised machine learning?* (Source: `Machine_learning.pdf`)
9. *What is a compiler and how does it translate source code?* (Source: `kecs111.pdf`)
10. *What is the primary role of an operating system in a computer system?* (Source: `kecs111.pdf`)
11. *What is the difference between primary memory and secondary memory?* (Source: `kecs111.pdf`)
12. *What are common frequently asked questions regarding IT grievance procedures?* (Source: `fqa.pdf`)
13. *What is the role of deep learning in modern AI technology?* (Source: `Artificial_intelligence.pdf`)
14. *What are transformer models in Generative AI?* (Source: `Generative_AI.pdf`)
15. *What is the real-time stock price of Apple Inc. today?* (Out-of-Scope Test Question — Expected Response: *"I could not find the answer in the provided documents."*)

### Optional Quick Test Samples (Available in UI Helper Expander):
- *What are the revised grievance redressal timelines under the IT Rules?*
- *What is stated in Rule 3(3) of the IT Rules, 2021?*
- *What are the main objectives of the Government of India Open Source Software Policy?*
- *What are the key applications of Generative AI?*

## 24. Evaluation Methodology & Results Summary
The system was evaluated on a 15-question benchmark recorded in `test_set.csv`. The final test results showed grounded and relevant responses for the benchmark questions, including source document/page information.

In `test_results.csv`, all 15 benchmark questions (15 / 15) met the evaluation criterion of returning grounded answers supported by retrieved document passages with valid page citations, or correctly returning the refusal response for the out-of-scope question. Note: This result represents performance against the specific 15-question test benchmark set, not a general model accuracy score.

- **In-Scope Benchmark Queries (Q1–Q14)**: All 14 in-scope questions retrieved relevant context passages from the target PDF documents and generated factual responses with valid source document names and page numbers.
- **Out-of-Scope Test Query (Q15)**: The out-of-scope query regarding real-time stock prices was correctly rejected by the model with the exact grounding response *"I could not find the answer in the provided documents."*

Full per-question outputs, retrieved source citations, and evaluation comments are recorded in [`test_results.csv`](file:///c:/Users/cnuba/Downloads/Document_QA_RAG/test_results.csv).

## 25. Limitations
- **PDF Text Parsing**: PyPDF2 extracts plain text; complex embedded tables or image diagrams in PDFs are not converted into structured data tables.
- **Hardware Performance**: Local LLM inference speed depends on system CPU and available RAM.

## 26. Troubleshooting
- **Ollama Error**: Verify Ollama is running and `ollama list` shows `llama3.2:3b`.
- **Vector DB Missing**: Run `python build_index.py` to create `vector_db/faiss.index`.
- **PyPDF2 Import Error**: Ensure virtual environment is activated (`.\venv\Scripts\Activate.ps1`) and run `pip install -r requirements.txt`.
