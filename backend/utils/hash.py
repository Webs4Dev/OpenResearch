import hashlib

def generate_paper_id(paper_code: str):
    return hashlib.sha256(paper_code.encode()).hexdigest()[:16]