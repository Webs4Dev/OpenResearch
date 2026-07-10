# OpenResearchGPT

OpenResearchGPT is an open-source multi-agent research discovery and analysis platform designed to help users find, understand, rank, and interact with research papers from multiple sources.

Unlike traditional paper search tools, OpenResearchGPT focuses on explainability and research understanding — helping users discover relevant papers, understand *why* they matter, and connect research findings directly to their own projects.

The project now ships with a full web frontend (search, PDF workspace, in-PDF highlighting, and per-paper Q&A) on top of the FastAPI backend and multi-agent retrieval pipeline.

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

Results-per-source and which sources to query are both configurable per search, from the UI or the API.

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

The frontend renders the actual PDF (via `react-pdf`) with relevant chunks highlighted directly in the text, numbered to match the reasoning cards alongside it — not just a list of extracted snippets.

---

### Citation-Aware RAG

Interact with research papers through conversational retrieval while preserving citations and contextual understanding.

---

### Ingestion Deduplication

Before a PDF is chunked and embedded, the backend checks ChromaDB for an existing entry with the same identifier and skips re-processing if it's already stored — avoiding duplicate embeddings and wasted API calls on repeat uploads.

---

## Frontend

A Vite + React + TypeScript app that talks to the FastAPI backend over `/api/v1/*`.

- **Dashboard** — entry points into the two tools, plus a recent-activity feed (last 8 searches, ingests, analyses, and questions asked) persisted locally so it survives refreshes.
- **Search Papers** — query, optional project description, results-per-source, and a source picker; returns ranked cards with score, source, year, PDF link, and the explanation behind the ranking.
- **PDF Workspace** — upload a PDF, then choose between:
  - **Analyse** — scores chunks against a project description and renders them as highlighted regions directly in the PDF, numbered and color-matched to reasoning cards (relevance score, chunk type, reason, suggested use).
  - **Ingest and ask** — ingests the paper into ChromaDB, then opens a chat scoped only to that paper.

---

## Planned Features

- Research gap detection
- Automated literature review generation
- Fine-tuned explanation model (LoRA)
- Personalized research memory
- Citation graph visualization
- Model evaluation pipeline
- Local model support
- Pixel-accurate highlight bounding boxes (current highlighting matches on text content, not stored coordinates)
- Content-hash-based ingestion dedup (currently deduplicates by filename)

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

### Ingest and Ask Pipeline

This path persists the paper to ChromaDB so it can be queried conversationally.

```text
PDF Upload
    ↓
Already ingested (by filename)? ── yes ──→ Skip straight to Ready for questions
    ↓ no
Parser (PyMuPDF)
    ↓
Page-Aware Overlap Chunking
    ↓
Embeddings (OpenAI)
    ↓
ChromaDB — chunk_collection + paper_collection
    ↓
Ready for questions
    ↓
User Question
    ↓
Hybrid Retrieval (vector search over chunk_collection,
scoped to paper_title)
    ↓
PDF QA Agent
    ↓
Answer + confidence + source chunks/pages
```

### Analysis Pipeline

This path never touches ChromaDB or embeddings — it's a direct LLM scoring
pass over freshly-parsed chunks, independent of whether the paper has ever
been ingested.

```text
PDF Upload + Project Description
    ↓
Parser (PyMuPDF)
    ↓
Page-Aware Overlap Chunking
    ↓
Project-Relevance Agent (gpt-4o-mini)
    ↓ (scores every chunk against the project description in one LLM call)
Relevant Chunks
    (relevance_score, chunk_type, reason, suggested_use, page_no)
    ↓
Frontend: PDF rendered with numbered,
color-matched highlights per chunk
```

### Frontend Request Flow

```text
Dashboard ──→ Search Papers ──→ POST /api/v1/search ──→ ranked result cards
    │
    └──→ PDF Workspace ──→ upload PDF
              │
              ├── Analyse ──→ POST /api/v1/analyze ──→ PDF rendered with
              │                                        numbered highlights
              │
              └── Ingest and ask ──→ POST /api/v1/ingest ──→ POST /api/v1/ask
                                                              (chat, scoped
                                                              to that paper)
```

---

## Current Progress

### Backend

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
- ✅ Day 27 — ChromaDB Paper Storage & RAG QA Endpoint
- ✅ Day 28 — Fixed Minor Issues & Added Relevance Score
- ✅ Day 29 — PDF Ingestion Pipeline
- ✅ Day 30 — Integration PDF Ingestion in Search
- ✅ Day 31 — Creating Separate Chunk & Paper Collection
- ✅ Day 32 — Hybrid Retrieval using Chunk & Paper Collection
- ✅ Day 33 — Fixing RAG source metadata
- ✅ Day 34 — Chunk-aware Paper Filtering & Fixing Pipeline
- ✅ Day 35 — Resolve has_chunks Metadata Update in Hybrid Retrieval
- ✅ Day 36 — PDF Endpoint v2
- ✅ Day 37 — Adding chunk_text to the PDF Analysis Pipeline
- ✅ Day 38 — Storing PDF
- ✅ Day 39 — Ingestion deduplication
- ✅ Day 40 — CORS configuration for frontend integration

### Frontend

- ✅ Day 41 — App shell, sidebar navigation, and Dashboard
- ✅ Day 41 — Search Papers — query, project description, results-per-source, source picker, ranked result cards
- ✅ Day 41 — PDF Workspace — upload flow with Analyse / Ingest-and-ask choice
- ✅ Day 41 — Ingest-and-ask — inline chat scoped to the ingested paper
- ✅ Day 42 — Analyse — real PDF rendering with numbered, color-matched chunk highlighting
- ✅ Day 42 — Recent activity feed on the Dashboard, persisted locally
- ✅ Day 43 — Branding (logo, sidebar identity)
- ⬜ Pixel-exact highlight bounding boxes (pending backend support)
- ⬜ Deployed instance (frontend on Netlify, backend host TBD)

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

### Frontend

- React + TypeScript + Vite
- Tailwind CSS
- TanStack Query (request state for search/ingest/analyze/ask)
- Zustand (shared workspace state, persisted activity log)
- react-pdf / pdf.js (in-browser PDF rendering and highlighting)

### Deployment

- Docker (backend)
- Netlify (frontend)

---

## Getting Started

### Backend

```bash
uvicorn backend.main:app --reload
```

Runs on `http://localhost:8000` by default. Enable CORS for the frontend's origin in `backend/main.py` (see `frontend/README.md` for the exact snippet).

### Frontend

```bash
cd frontend
npm install
cp .env.example .env   # set VITE_API_URL to your backend URL
npm run dev
```

Runs on `http://localhost:5173` by default. See `frontend/README.md` for Netlify deployment steps and known gaps between the frontend and backend schemas.

---
