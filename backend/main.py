from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from models import Base

from routers.auth import router as auth_router
from routers.conversation import router as conversation_router
from routers.pdf import router as pdf_router
from routers.chat import router as chat_router

app = FastAPI()

# 1. CORS Allow All (Production Safe for Testing)
origins = ["*"]  # Saare domains se requests allow karega

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Database Tables Creation on Startup
@app.on_event("startup")
def startup_db_client():
    Base.metadata.create_all(bind=engine)

# 3. Include Routers
app.include_router(pdf_router)
app.include_router(auth_router)
app.include_router(conversation_router)
app.include_router(chat_router)

@app.get("/")
def home():
    return {"message": "Backend Running Successfully"}