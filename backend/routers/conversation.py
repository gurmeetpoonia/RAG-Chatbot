#conversation/create
#history
#conversation/{id}/rename
#conversation/{id}
#conversation/{id}/messages
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import get_current_user
from models import Conversation, ConversationPDF, PDF, Chat, User
from schemas import (
    AddPDFRequest,
    RemovePDFRequest,
    RenameConversationRequest,
)
from Dependencies import get_db
router = APIRouter(prefix="", tags=["Conversation"])


@router.post("/conversation/create")
def create_conversation( current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    
    conversation = Conversation(title="New Chat", user_id=current_user.id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    

    return conversation

@router.get("/history")
def get_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversations = db.query(Conversation).filter(Conversation.user_id == current_user.id).order_by(Conversation.created_at.desc()).all()
    result = []

    for conversation in conversations:
        # Directly table relationships queries fetch karna taaki lazy map issue na aaye
        attached_pdfs = db.query(PDF).join(ConversationPDF, ConversationPDF.pdf_id == PDF.id).filter(
            ConversationPDF.conversation_id == conversation.id
        ).all()

        result.append({
            "id": conversation.id,
            "title": conversation.title,
            "pdfs": [{"id": p.id, "filename": p.filename} for p in attached_pdfs]
        })

    return result

@router.get("/conversation/{conversation_id}/messages")
def get_messages(conversation_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    chats = db.query(Chat).filter(Chat.conversation_id == conversation_id).order_by(Chat.created_at).all()
    return chats

@router.get("/conversation/{conversation_id}/pdfs")
def get_conversation_pdfs(conversation_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Safe SQL Join query loading mapping attributes
    pdfs_data = db.query(PDF).join(ConversationPDF, ConversationPDF.pdf_id == PDF.id).filter(
        ConversationPDF.conversation_id == conversation.id
    ).all()

    return [{"id": pdf.id, "filename": pdf.filename} for pdf in pdfs_data]

@router.put("/conversation/{conversation_id}/rename")
def rename_conversation(conversation_id: int, request: RenameConversationRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    conversation.title = request.title
    db.commit()
    db.refresh(conversation)
    return conversation

@router.delete("/conversation/{conversation_id}")
def delete_conversation(conversation_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    db.delete(conversation)
    db.commit()
    return {"message": "Conversation deleted"}

@router.post("/conversation/add-pdf")
def add_pdf_to_conversation(request: AddPDFRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(
        Conversation.id == request.conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    for pdf_id in request.pdf_ids:
        exists = db.query(ConversationPDF).filter(
            ConversationPDF.conversation_id == conversation.id,
            ConversationPDF.pdf_id == pdf_id
        ).first()

        if exists:
            continue

        pdf = db.query(PDF).filter(PDF.id == pdf_id, PDF.user_id == current_user.id).first()
        if pdf:
            db.add(ConversationPDF(conversation_id=conversation.id, pdf_id=pdf.id))

    db.commit()
    return {"message": "PDF Added Successfully"}

@router.post("/conversation/remove-pdf")
def remove_pdf_from_conversation(request: RemovePDFRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(
        Conversation.id == request.conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    assoc = db.query(ConversationPDF).filter(
        ConversationPDF.conversation_id == conversation.id,
        ConversationPDF.pdf_id == request.pdf_id
    ).first()

    if assoc:
        db.delete(assoc)
        db.commit()
        return {"message": "PDF removed from conversation"}
        
    raise HTTPException(status_code=404, detail="PDF not found in this conversation")