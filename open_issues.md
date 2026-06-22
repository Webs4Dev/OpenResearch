# Issue : Irrelevant Results for Ambiguous Queries

Queries such as "What is RAG?" sometimes retrieve unrelated papers (e.g., RAG genes, string theory) instead of Retrieval-Augmented Generation research.

Current behavior:

* Relevant papers are not ranked highly enough.
* Hybrid retrieval returns irrelevant chunks.
* RAG agent cannot answer despite relevant papers existing.

Potential fixes:

* Add query expansion/disambiguation.
* Improve retrieval ranking.
* Add support for common AI abbreviations (RAG, LLM, RLHF, MARL).
