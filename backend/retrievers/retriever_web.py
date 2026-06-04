from ddgs import DDGS
from backend.schemas.paper import Paper
from backend.agents.source_discovery_agent import discover_sources
from backend.utils.source_to_domain import source_to_domain
from backend.utils.logger import log

WEB_SOURCES = {
    "gov",
    "edu",
    "nasa",
    "nih",
    "researchgate"
}

def search_web(query:str,max_results:int=3):
    with DDGS() as ddgs:
        result = list(
            ddgs.text(query,max_results=max_results)
            )

    return result

def web_retrieve(query: str,source_type: str,max_results: int = 5):

    search_query = (
        f"{query} site:{source_type}"
    )

    results = search_web(
        search_query,
        max_results
    )

    papers = []

    for item in results:

        paper = Paper(
            title=item.get("title","Unknown Title"),
            abstract=item.get("body",""),
            authors=[],
            source=f"web_{source_type}",
            url=item.get("href",""),
            published_year=None
        )

        papers.append(
            paper
        )

    return papers

def domain_web_retrieve(query,max_results=5):

    discovery = (discover_sources(query))

    log(
    f"Web Agent selected: "
    f"{discovery.recommended_sources}"
    )

    papers=[]

    for source in (discovery.recommended_sources):

        if source not in WEB_SOURCES:
            continue

        domain = (source_to_domain(source))

        log(
        f"Searching web source: "
        f"{source}"
        )
        
        if domain:
            papers.extend(
                web_retrieve(
                    query,
                    domain,
                    max_results
                )
            )

    return papers