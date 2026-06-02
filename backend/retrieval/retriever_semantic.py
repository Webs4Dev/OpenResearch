from backend.schemas.paper import Paper
from backend.utils.logger import log
from semanticscholar import SemanticScholar
from dotenv import load_dotenv
import os

load_dotenv()

S2_API_KEY = os.getenv("S2_API_KEY")

sch = SemanticScholar(api_key=S2_API_KEY)

def search_papers(query: str,max_results: int):
    papers=[]

    try:

        response = sch.search_paper(
            query=query,
            limit=max_results
        )

        for paper in response.items:

            pdf_url = None

            # Try getting direct open-access PDF
            if (
                hasattr(paper, "openAccessPdf")
                and paper.openAccessPdf
            ):

                pdf_url = (
                    paper.openAccessPdf
                    .get("url")
                )

            # Fallback to Semantic Scholar page
            if not pdf_url:
                pdf_url = paper.url

            papers.append(
                Paper(
                    title=paper.title,
                    abstract=paper.abstract or "Not Available",
                    authors=[a.name for a in paper.authors],
                    published_year=paper.year or None,
                    url=pdf_url or "Not Available",
                    source="semantic_scholar"
                )
            )

    except Exception as e:
        log(f"Semantic Scholar Error: {e}")

    return papers