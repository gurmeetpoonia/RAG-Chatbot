#ask
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth import get_current_user
from schemas import QuestionRequest
from services.vector_store import model, collection
from models import User, Chat, Conversation, ConversationPDF
from gemini import ask_gemini, generate_chat_title
from Dependencies import get_db
router = APIRouter(prefix="", tags=["Chat"])

@router.post("/ask")  
async def ask_question(request: QuestionRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(
        Conversation.id == request.conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    if conversation.title == "New Chat":
        try:
            conversation.title = generate_chat_title(request.question)
        except:
            conversation.title = request.question[:40]
        db.commit()
        db.refresh(conversation)    

    question = request.question
    question_embedding = model.encode(question)
    
    conversation_pdfs = db.query(ConversationPDF).filter(
        ConversationPDF.conversation_id == conversation.id
    ).all()
    pdf_ids = [item.pdf_id for item in conversation_pdfs]

    if not pdf_ids:
        raise HTTPException(status_code=404, detail="No PDF attached to this conversation")

    results = collection.query(
        query_embeddings=[question_embedding.tolist()],
        n_results=5,
        where={
            "$and": [
                {"user_id": current_user.id},
                {"pdf_id": {"$in": pdf_ids}}
            ]
        }
    )
    
    documents = results.get("documents", [])
    if not documents or not documents[0]:
        raise HTTPException(status_code=404, detail="No data found in this PDF context")

    context = "\n".join(results["documents"][0])

    history_text = ""
    history = db.query(Chat).filter(Chat.conversation_id == conversation.id).all()
    for chat in history:
        history_text += f"\nUser: {chat.question}\nAI: {chat.answer}\n"
   
    answer = ask_gemini(context=context, question=question, history=history_text)
    
    new_chat = Chat(question=question, answer=answer, conversation_id=conversation.id)   
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    
    return {
        "message": "Question answered successfully",
        "chat": {
            "id": new_chat.id,
            "question": question,
            "answer": answer
        },
        "conversation_id": conversation.id,
        "conversation_title": conversation.title
    }