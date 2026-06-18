import hashlib

def generate_paper_id(paper_title: str):
    return hashlib.sha256(paper_title.encode()).hexdigest()[:16]