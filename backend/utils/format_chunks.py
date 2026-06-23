def format_chunks_pdf(chunks):
    formatted=[]
    for chunk in chunks:
        formatted.append(
            {
                "chunk_id":chunk['chunk_id'],
                "page_no":chunk['page_no'],
                "text":chunk['text']
            }
        )

    return formatted

def format_chunks_context(chunks):

    context = []
    for chunk in chunks:
        context.append(
            f"""
            Paper:
            {chunk["paper_title"]}

            Source:
            {chunk["source"]}

            Chunk ID:
            {chunk["chunk_id"]}

            Text:
            {chunk["text"]}
            """
        )

    return "\n\n".join(
        context
    )