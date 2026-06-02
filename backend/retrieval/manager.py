from backend.retrieval.retriever_arxiv import search_papers as arxiv_search
from backend.retrieval.retriever_semantic import search_papers as semantic_search
from backend.retrieval.retriever_pubmed import search_papers as pubmed_search
from backend.retrieval.retriever_openalex import search_papers as openalex_search
from backend.retrieval.retriever_crossref import search_papers as crossref_search
from backend.retrieval.retriever_web import domain_web_retrieve
from backend.retrieval.deduplicator import deduplicate_papers
from backend.utils.logger import log
from concurrent.futures import ThreadPoolExecutor,as_completed


ALL_SOURCES = {
    "arxiv": arxiv_search,
    "semantic_scholar": semantic_search,
    "pubmed": pubmed_search,
    "openalex": openalex_search,
    "crossref": crossref_search,
    "web":domain_web_retrieve
}


def retrieve_source(source_name,retriever,query,max_results):
    try:
        results = retriever(
            query=query,
            max_results=max_results
        )
        return (
            source_name,
            results,
            None
        )
    except Exception as e:
        return (source_name,[],str(e))


def retrieve_all(query: str,max_results: int,sources: list[str] | None = None) -> tuple[list, dict]:
    """
    Returns:
        papers        - flat list of Paper objects
        source_report - { source_name: { count, status, error } }
    """

    active = sources if sources else list(ALL_SOURCES.keys())
    unknown = [s for s in active if s not in ALL_SOURCES]

    if unknown:
        raise ValueError(f"Unknown sources: {unknown}. Valid: {list(ALL_SOURCES.keys())}")

    papers = []     
    report = {}

    # Run all retrievers simultaneously instead of sequentially.
    with ThreadPoolExecutor(max_workers=len(active)) as executor: 

        futures={
            executor.submit(retrieve_source,name,ALL_SOURCES[name],query,max_results):
            name for name in active
        }

        for future in as_completed(futures):
            source_name=(futures[future])
            name,results,error=(
                future.result()
            )

            papers.extend(results)

            if error:
                report[name]={
                    "count":0,
                    "status":"error",
                    "error":error
                }
                log(f"[{name}] failed: {error}")

            else:
                report[name]={
                    "count":len(results),
                    "status":"ok",
                    "error":None
                }
                log(f"[{name}] -> {len(results)} papers")

    log(f"[Retrieved Papers] -> {len(papers)}")
    papers = deduplicate_papers(papers)
    log(f"[Unique Papers] -> {len(papers)}")

    return papers, report