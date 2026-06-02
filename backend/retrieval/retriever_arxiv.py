import urllib.request
import arxiv
import os
from dotenv import load_dotenv
from backend.schemas.paper import Paper
from backend.utils.logger import log
load_dotenv()

EMAIL = os.getenv("EMAIL")

opener = urllib.request.build_opener()
opener.addheaders = [
    ("User-Agent", f"OpenResearch/1.0 ({EMAIL})")
]
urllib.request.install_opener(opener)

client = arxiv.Client(
    num_retries=1,
    delay_seconds=5,
    page_size=5
)

def search_papers(query: str, max_results: int):

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    papers=[]

    try:
        for paper in client.results(search):

            papers.append(
                Paper(
                    title=paper.title,
                    abstract=paper.summary or "Not Available",   
                    authors=[a.name for a in paper.authors],
                    published_year=paper.published.year or None,
                    url=paper.pdf_url or "Not Available",
                    source="arxiv"
                )
            )

    except Exception as e:
        log(f"ArXiv Error: {e}")

    return papers