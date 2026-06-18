# OpenResearch — Open Issues

This document tracks known issues, their impact, and proposed fixes for the OpenResearch project.

## Issue 1 — Unify PDF Availability Detection

### Problem

Ranking and ingestion use different PDF-detection logic. As a result, some papers are marked as having PDFs during ranking but are skipped during ingestion.

### Proposed solution

Use a single PDF verification flow for both pipelines. Prefer download-based validation over simple URL pattern matching to ensure PDFs are actually retrievable.

---

## Issue 2 — Hybrid Retrieval `$in` Filter Issue

### Problem

Using a ChromaDB query like:

```python
where = {
    "paper_title": {"$in": paper_titles}
}
```

returns zero results.

### Proposed solution

Query each paper individually, merge the results, sort by relevance, and return the top chunks. This avoids relying on a failing `$in` filter in ChromaDB.

---

## Issue 3 — Missing URL and Year in RAG Sources

### Problem

Chunk metadata sometimes lacks the original paper URL and publication year, causing RAG citations to include null values, e.g.:

```json
{
  "url": null,
  "year": null
}
```

### Proposed solution

Use the chunk's `paper_title` to look up full metadata from the `paper_metadata` collection and enrich citations with `url`, `year`, and `source` fields.

---

## Issue 4 — Papers Without Chunks in Hybrid Retrieval

### Problem

The `paper_metadata` collection contains all known papers, but `pdf_chunks` only includes papers whose PDFs were successfully ingested. Hybrid retrieval can select papers that have no chunks, leading to wasted retrieval attempts.

### Proposed solution

Add a `has_chunks` boolean field to `paper_metadata` and update it after ingestion completes. During hybrid retrieval, only select papers where `has_chunks == True`.

### Benefit

Ensures selected papers have searchable chunk data, improving retrieval effectiveness and reducing wasted work.
