from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from app.dependencies import get_db

from app.services.generative import get_assistant, get_embeddings, get_generative_answer, get_knowledge_by_url, get_prompt, set_embedding
from ..utils.logger import logger
from pydantic import BaseModel
from typing import List

class GenerateQuestion(BaseModel):
    url: List[str]
    assistant: str
    question: str

router = APIRouter(
    prefix="/generative",
    tags=["Generate Question"]
)

@router.post('/')
def read_root(generateQuestion: GenerateQuestion, db: Session = Depends(get_db)):
    try:
        pages = get_knowledge_by_url(generateQuestion.url)
        set_embedding(pages)
        assistant = get_assistant(generateQuestion.assistant, db)
        learning_retriever = get_embeddings(generateQuestion.question)
        template_question = get_prompt(assistant)
        answer = get_generative_answer(template_question, learning_retriever, generateQuestion.question)
        return JSONResponse(content=answer, status_code=200)
    except Exception as ex:
        logger.error(f"Request failed: Error {ex}")
        return JSONResponse(content={"success": False}, status_code=500)




   