import re 

def normalize_title(title:str):
    title = title.lower()
    title = re.sub(r"[^a-z0-9\s]","",title)
    title = " ".join(title.split())

    return title

def deduplicate_papers(papers):
    unique=[]
    seen_titles=set()

    for paper in papers:
        normalized = normalize_title(paper.title)
        if normalized not in seen_titles:
            seen_titles.add(normalized)
            unique.append(paper)

    return unique