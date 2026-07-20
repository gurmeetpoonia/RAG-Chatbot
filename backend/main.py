from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from models import Base


from routers.auth import router as auth_router
from routers.conversation import router as conversation_router
from routers.pdf import router as pdf_router
from routers.chat import router as chat_router


Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(pdf_router)
app.include_router(auth_router)
app.include_router(conversation_router)
app.include_router(chat_router)

@app.get("/")
def home():
    return {"message": "Backend Running Successfully"}


    
