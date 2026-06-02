from backend.schemas.paper import Paper
from backend.utils.logger import log
from dotenv import load_dotenv
import requests
import os

load_dotenv()

EMAIL=os.getenv("EMAIL")


def reconstruct_abstract(inverted_index):

    if not inverted_index:
        return ""

    words=[]

    for word,positions in inverted_index.items():
        for pos in positions:
            words.append((pos,word))

    words.sort()

    return " ".join(
        word for _,word in words
    )


def search_papers(query:str,max_results:int):

    papers=[]

    try:

        response=requests.get(
            "https://api.openalex.org/works",
            params={
                "search":query,
                "per-page":max_results,
                "sort":"relevance_score:desc"
            },
            headers={
                "User-Agent":
                f"OpenResearchGPT/1.0 ({EMAIL})"
            },
            timeout=20
        )

        response.raise_for_status()

        items=response.json().get(
            "results",
            []
        )

        for item in items:

            title=item.get(
                "title",
                "No title"
            )

            abstract=reconstruct_abstract(
                item.get(
                    "abstract_inverted_index"
                )
            )

            authors=[
                a.get("author",{})
                .get("display_name")
                for a in item.get(
                    "authorships",
                    []
                )
                if a.get("author",{})
                .get("display_name")
            ]

            year=item.get(
                "publication_year"
            )

            pdf_url=(
                item.get(
                    "open_access",
                    {}
                ).get("oa_url")
                or
                item.get(
                    "primary_location",
                    {}
                ).get("pdf_url")
            )

            papers.append(
                Paper(
                    title=title,
                    abstract=abstract or "Not Available",
                    authors=authors,
                    published_year=year or None,
                    url=pdf_url or "Not Available",
                    source="openalex"
                )
            )

    except Exception as e:
        log(f"OpenAlex Error: {e}")

    return papers