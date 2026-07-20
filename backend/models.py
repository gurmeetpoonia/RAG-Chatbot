from sqlalchemy import Column, Integer,String,Text, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime 

class User(Base):
    __tablename__= "users"
    id=Column(Integer,primary_key=True, index=True)
    username=Column(String,unique=True)
    email= Column(String,unique=True)
    password=Column(String)
    conversations=relationship("Conversation",back_populates="user",cascade="all,delete")
    pdfs=relationship("PDF",back_populates="user",cascade="all,delete")
 
class Chat(Base):
    __tablename__ = "chats" 
    id=Column(Integer,primary_key=True,index=True)
    question=Column(Text)
    answer=Column(Text)
    conversation_id=Column(Integer,ForeignKey("conversations.id"))
    created_at= Column(DateTime,default=datetime.utcnow)
    conversation = relationship(
        "Conversation",
        back_populates="chats"
    )

class PDF(Base) :
    __tablename__ ="pdfs"
    id=Column(Integer,primary_key=True,index=True)
    filename=Column(String)
    file_hash=Column(String)
    chroma_collection = Column(String)
    user_id=Column(Integer,ForeignKey("users.id"))
    uploaded_at=Column(DateTime,default=datetime.utcnow)
    user=relationship("User", back_populates="pdfs")
    conversations=relationship("ConversationPDF",back_populates="pdf",cascade="all,delete")



class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    pdfs = relationship("ConversationPDF", back_populates="conversation", cascade="all, delete-orphan")
    user = relationship("User", back_populates="conversations")
    chats = relationship("Chat", back_populates="conversation", cascade="all, delete-orphan")

class ConversationPDF(Base):
    __tablename__ = "conversation_pdfs"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"))
    pdf_id = Column(Integer, ForeignKey("pdfs.id", ondelete="CASCADE"))

    conversation = relationship("Conversation", back_populates="pdfs")
    pdf = relationship("PDF", back_populates="conversations")