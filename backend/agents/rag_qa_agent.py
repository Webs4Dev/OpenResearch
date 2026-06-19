from openai import OpenAI
import json
import os
from dotenv import load_dotenv

from prompts.rag_qa_prompt import RAG_QA_PROMPT
from backend.schemas.rag_response import RAGResponse,RAGSource
from backend.utils.format_chunks import format_chunks_context
from backend.rag.paper_store import get_paper_metadata
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def answer_research_question(question,chunks):
    prompt = (
        RAG_QA_PROMPT.format(
            question=question,
            chunks=format_chunks_context(chunks)
        )
    )

    response = (
        client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        )
    )
    parsed = json.loads(response.choices[0].message.content)

    sources=[]
    for chunk in chunks:
        metadata = get_paper_metadata(chunk["paper_title"])
        source = {
            "paper_title":chunk["paper_title"],
            "source":metadata["source"],
            "url":metadata.get("url"),
            "year":metadata.get("year"),
            "relevance_score":chunk["relevance_score"]
        }
        if source not in sources:
            sources.append(source)

    return RAGResponse(
        answer=parsed["answer"],
        confidence=parsed["confidence"],
        sources=[RAGSource(**s) for s in sources]
    )    