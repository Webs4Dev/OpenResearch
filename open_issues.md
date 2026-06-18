# OpenResearch - Open Issues

## 1. Unify PDF Availability Detection

### Problem

Ranking and ingestion use different PDF detection logic. Some papers are marked as having PDFs but are skipped during ingestion.

### Solution

Use a single PDF verification flow across both pipelines and prefer download-based validation over URL pattern matching.

---

## 2. Hybrid Retrieval `$in` Filter Issue

### Problem

```python
where={
    "paper_title":{
        "$in": paper_titles
    }
}
```

returns zero results in ChromaDB.

### Solution

Query each paper individually, merge the results, sort by relevance, and return the top chunks.

---

## 3. Missing URL and Year in RAG Sources

### Problem

Chunk metadata does not contain URL or publication year, causing RAG citations to return:

```json
{
  "url": null,
  "year": null
}
```

### Solution

Use the chunk's `paper_title` to lookup metadata from the `paper_metadata` collection and enrich the final citations with URL, year, and source information.
