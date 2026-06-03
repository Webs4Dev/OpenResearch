from Bio import Entrez
from backend.schemas.paper import Paper
from backend.utils.logger import log
from dotenv import load_dotenv
import os

load_dotenv()

Entrez.email=os.getenv("EMAIL")
Entrez.api_key=os.getenv("PUBMED_API_KEY")

def get_pdf_url(pmid):

    try:

        handle=Entrez.elink(
            dbfrom="pubmed",
            db="pmc",
            id=pmid
        )

        records=Entrez.read(handle)
        handle.close()

        links=records[0].get(
            "LinkSetDb",
            []
        )
        if links:

            pmc_id=links[0]["Link"][0]["Id"]

            return (
                f"https://pmc.ncbi.nlm.nih.gov/articles/PMC{pmc_id}/pdf"
            )
    except:
        pass

    return f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

def search_papers(query:str,max_results:int):

    papers=[]

    try:

        search=Entrez.esearch(
            db="pubmed",
            term=query,
            retmax=max_results,
            sort="relevance"
        )

        ids=Entrez.read(
            search
        )["IdList"]

        search.close()

        if not ids:
            return []

        fetch=Entrez.efetch(
            db="pubmed",
            id=",".join(ids),
            rettype="medline",
            retmode="xml"
        )

        articles=Entrez.read(
            fetch
        )["PubmedArticle"]

        fetch.close()

        for article in articles:

            data=article[
                "MedlineCitation"
            ]["Article"]

            title=data.get(
                "ArticleTitle",
                "No title"
            )

            abstract=" ".join(
                str(x)
                for x in data.get(
                    "Abstract",
                    {}
                ).get(
                    "AbstractText",
                    []
                )
            )

            authors=[
                f"{a['ForeName']} {a['LastName']}"
                for a in data.get(
                    "AuthorList",
                    []
                )
                if "ForeName" in a
                and "LastName" in a
            ]

            year=None
            try:
                year=int(
                    data["Journal"]
                    ["JournalIssue"]
                    ["PubDate"]
                    ["Year"]
                )
            except:
                pass

            pmid=str(
                article[
                    "MedlineCitation"
                ]["PMID"]
            )

            papers.append(
                Paper(
                    title=title,
                    abstract=abstract or "Not Available",
                    authors=authors,
                    published_year=year or None,
                    url=get_pdf_url(pmid) or "Not Available",
                    source="pubmed"
                )
            )

    except Exception as e:
        log(f"PubMed Error: {e}")
        raise
    return papers