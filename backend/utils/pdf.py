def has_pdf(url: str):

    if not url:
        return False

    url = url.lower()

    pdf_patterns = [
        ".pdf",
        "/pdf",
        "pdf?",
        "pdf#"
    ]

    return any(
        pattern in url
        for pattern in pdf_patterns
    )