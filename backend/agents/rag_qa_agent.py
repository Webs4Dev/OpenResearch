from openai import OpenAI
import json
import os
from dotenv import load_dotenv

from prompts.rag_qa_prompt import RAG_QA_PROMPT
from backend.schemas.rag_response import RAGResponse,RAGSource
from backend.utils.format_chunks import format_chunks_context
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
        source = {
            "paper_title":chunk["paper_title"],
            "source":chunk["source"],
            "url":chunk.get("url")
        }
        if source not in sources:
            sources.append(source)

        return RAGResponse(
            answer=parsed["answer"],
            confidence=parsed["confidence"],
            sources=[RAGSource(**s) for s in sources]
        )