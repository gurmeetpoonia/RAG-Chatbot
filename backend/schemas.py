from pydantic import BaseModel
from typing import List


class QuestionRequest(BaseModel):
    question: str
    conversation_id: int


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class AddPDFRequest(BaseModel):
    conversation_id: int
    pdf_ids: List[int]


class RemovePDFRequest(BaseModel):
    conversation_id: int
    pdf_id: int


class RenameConversationRequest(BaseModel):
    title: str