import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from langchain.embeddings.openai import OpenAIEmbeddings
from .repository.document_repository import DocumentRepository
from .loader.loader import DataLoader
from .services.chatbot import Chatbot

app = FastAPI()

document_repository = DocumentRepository(embeddings=OpenAIEmbeddings())
vector_store = document_repository.get_vector_store()
loop = asyncio.get_event_loop()


class FeedDataRequest(BaseModel):
    urls: List[str]


class ChatEntry(BaseModel):
    question: str
    answer: str


class AnswerQuestionRequest(BaseModel):
    question: str
    chat_history: List[ChatEntry]


class AnswerQuestionResponse(BaseModel):
    question: str
    answer: str


@app.post("/{chatbot_id}/feed_data")
async def load_data(chatbot_id: str, request: FeedDataRequest):
    loader = DataLoader()
    documents = await loop.run_in_executor(None, loader.load_urls, request.urls)
    await loop.run_in_executor(None, document_repository.save_documents, documents, chatbot_id)
    return {"message": "Data loaded successfully!"}


@app.post("/{chatbot_id}/answer", response_model=AnswerQuestionResponse)
async def answer_question(chatbot_id: str, request: AnswerQuestionRequest):
    chatbot = Chatbot(vector_store, chatbot_id)
    chat_history = [(entry.question, entry.answer) for entry in request.chat_history]
    standalone_question, answer = chatbot.generate_question(request.question, chat_history)
    return AnswerQuestionResponse(question=standalone_question, answer=answer)
