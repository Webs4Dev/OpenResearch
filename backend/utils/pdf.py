def has_pdf(paper):

    if not paper.url:
        return False

    url = paper.url.lower()

    return (
        ".pdf" in url or "/pdf/" in url
    )