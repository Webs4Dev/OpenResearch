def format_chunks(chunks):
    formatted=[]
    for chunk in chunks:
        formatted.append(
            {
                "chunk_id":chunk.chunk_id,
                "text":chunk.text
            }
        )

    return formatted