# OpenResearchGPT

OpenResearchGPT is an open-source multi-agent research discovery and analysis platform designed to help users find, understand, rank, and interact with research papers from multiple sources.

Unlike traditional paper search tools, OpenResearchGPT focuses on explainability and research understanding — helping users discover relevant papers, understand *why* they matter, and connect research findings directly to their own projects.

---

## Core Features

### Multi-Source Research Retrieval

Retrieve research papers from multiple academic sources:

- arXiv
- Semantic Scholar
- PubMed
- OpenAlex
- CrossRef
- Government research portals
- University repositories
- Additional web-based sources

---

### Web Retrieval Agent

Discover research papers from websites that do not provide APIs or official Python libraries.

Examples:

- Government research portals
- Research lab websites
- University repositories
- Organization publications

---

### Paper Ranking Agent

Rank research papers using multiple factors:

- Semantic similarity
- Recency
- Citation count
- Methodology similarity
- Source quality
- Project relevance

---

### Explanation Agent

Explain *why* a paper was recommended.

Example:

**Paper:** *Memory Architectures for LLM Agents*

**Why it was selected:**

- Matches multi-agent memory systems
- Strong methodology overlap
- Recent publication
- High semantic similarity

---

### PDF Deep Dive Agent

Upload a research paper and let the system:

- Identify important sections
- Highlight useful content
- Explain difficult concepts
- Answer questions
- Connect research ideas to your project

---

### Citation-Aware RAG

Interact with research papers through conversational retrieval while preserving citations and contextual understanding.

---

## Planned Features

- Research gap detection
- Automated literature review generation
- Fine-tuned explanation model (LoRA)
- Personalized research memory
- Citation graph visualization
- Model evaluation pipeline
- Local model support
- PDF highlighting generation

---

## Project Architecture

### Research Retrieval Pipeline

```text
User Query
    ↓
Query Understanding Agent
    ↓
Retrieval Manager
        ↓
        ├── arXiv Retriever
        ├── Semantic Scholar Retriever
        ├── PubMed Retriever
        ├── OpenAlex Retriever
        ├── CrossRef Retriever
        └── Web Retrieval Agent
                    ↓
              Government Sites
              University Repositories
              Research Websites
    ↓
Ranking Agent
    ↓
Explanation Agent
    ↓
Results
```

### PDF Analysis Pipeline

```text
PDF Upload
    ↓
Parser
    ↓
Chunking
    ↓
Embeddings
    ↓
Project-Relevance Agent
    ↓
Highlighted Sections
    ↓
Q&A Agent
```

---

## Current Progress

- ✅ Day 1 — Project setup
- ✅ Day 2 — arXiv paper retrieval
- ✅ Day 3 — Semantic Scholar retrieval
- ✅ Day 4 — Retrieval manager and logging
- ✅ Day 5 — PubMed, OpenAlex, and CrossRef retrieval
- ✅ Day 6 — Source Discovery and Web Retrieval foundation
- ✅ Day 7 — Ranking Agent v1
- ✅ Day 8 — Ranking Result Schema and JSON Parser
- ✅ Day 9 — FastAPI Endpoint (Ranking)
- ✅ Day 10 — Fixing Endpoint issues  
- ✅ Day 11 — Concurrent Retrieval using ThreadPoolExecutor  
- ✅ Day 12 — Concurrent Ranking using ThreadPoolExecutor
- ✅ Day 13 — Paper Deduplication Layer
- ✅ Day 14 — Edge Case Handling and Ranking Robustness
- ✅ Day 15 — LLM-powered Source Discovery Agent
- ✅ Day 16 — Web Retrieval Agent v1
- ✅ Day 17 — Web Retrieval Agent Integration
- ✅ Day 18 — Retrieval Statistics & Pipeline Stabilization
- ✅ Day 19 — PDF Upload and Text Extraction Pipeline
- ✅ Day 20 — PDF Chunking Pipeline
- ✅ Day 21 — Project Relevance Agent
- ✅ Day 22 — PDF QA Agent
- ✅ Day 23 — PDF Deep Dive Endpoint
- ✅ Day 24 — Page-Aware Overlap Chunking
- ✅ Day 25 — ChromaDB Vector Storing
- ✅ Day 26 — Paper Metadata Addition to DB
- ✅ Day 27 — ChromaDB Paper Storage & Rag QA Endpoint  

---

## Tech Stack

### Backend

- Python
- FastAPI
- LangGraph

### AI / ML

- OpenAI API
- LoRA fine-tuning
- Retrieval-Augmented Generation (RAG)

### Database

- ChromaDB

### PDF Processing

- PyMuPDF

### Deployment

- Docker

---

## Contributing

Contributions, ideas, feature requests, and feedback are welcome.
Contribution guidelines will be added in future updates.

---

## License

This project is licensed under the MIT License.
