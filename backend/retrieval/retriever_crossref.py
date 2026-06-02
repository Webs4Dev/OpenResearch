from backend.schemas.paper import Paper
from backend.utils.logger import log
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests
import os

load_dotenv()

EMAIL = os.getenv("EMAIL")

session = requests.Session()

retries = Retry(
    total=3,
    backoff_factor=2,
    status_forcelist=[429,500,502,503,504]
)

session.mount(
    "https://",
    HTTPAdapter(max_retries=retries)
)


def search_papers(query:str,max_results:int):

    papers=[]

    try:

        response=session.get(
            "https://api.crossref.org/works",
            params={
                "query":query,
                "rows":max_results,
                "sort":"relevance"
            },
            headers={
                "User-Agent":
                f"OpenResearchGPT/1.0 ({EMAIL})"
            },
            timeout=30
        )

        response.raise_for_status()

        items=response.json()["message"]["items"]

        for item in items:

            title=item.get(
                "title",
                ["No title"]
            )[0]

            abstract=item.get(
                "abstract",
                ""
            )

            authors=[
                f"{a.get('given','')} {a.get('family','')}".strip()
                for a in item.get("author",[])
            ]

            year=None

            try:
                year=item["published-print"]["date-parts"][0][0]

            except:
                try:
                    year=item["published-online"]["date-parts"][0][0]
                except:
                    pass

            url=None

            for link in item.get("link",[]):

                if link.get("content-type")=="application/pdf":

                    url=link.get("URL")
                    break

            if not url:

                doi=item.get("DOI")

                if doi:
                    url=f"https://doi.org/{doi}"

            papers.append(
                Paper(
                    title=title,
                    abstract=abstract or "Not Available",
                    authors=authors,
                    published_year=year or None,
                    url=url or "Not Available",
                    source="crossref"
                )
            )

    except requests.exceptions.Timeout:
        log("Crossref Timeout Error")

    except requests.exceptions.RequestException as e:
        log(f"Crossref Request Error: {e}")

    except Exception as e:
        log(f"Crossref Error: {e}")

    return papers