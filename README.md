# 🤖 RAG Chatbot

An AI-powered Retrieval-Augmented Generation (RAG) Chatbot built using **FastAPI, React, ChromaDB, Google Gemini, and JWT Authentication**. Users can securely upload PDF, DOCX, and TXT files, ask questions, and receive context-aware answers generated from their own documents.

---

## 🚀 Features

- 🔐 User Authentication (JWT Login/Register)
- 📄 Upload PDF, DOCX & TXT files
- 🧠 Google Gemini Embeddings
- 📚 ChromaDB Vector Database
- 💬 Chat with uploaded documents
- 🔍 Semantic Search using RAG
- 📂 User-specific document storage
- 🗑️ Delete uploaded documents
- 📱 Responsive React UI
- ⚡ FastAPI Backend

---

## 🛠️ Tech Stack

### Frontend
- React.js
- Vite
- Axios
- React Router
- React Hot Toast
- CSS

### Backend
- FastAPI
- SQLAlchemy
- JWT Authentication
- Passlib (bcrypt)
- ChromaDB
- Google Gemini API
- PyMuPDF
- python-docx
- pytesseract

### Database
- SQLite
- ChromaDB (Vector Database)

---

## 📂 Project Structure

```
RAG-Chatbot/
│
├── backend/
│   ├── routers/
│   ├── services/
│   ├── models.py
│   ├── auth.py
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/RAG-Chatbot.git
cd RAG-Chatbot
```

---

### Backend

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload
```

---

### Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## 🔑 Environment Variables

Create a `.env` file inside the backend folder.

```env
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY

SECRET_KEY=YOUR_SECRET_KEY

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## 📸 Screenshots

- Login Page
- Register Page
- Chat Interface
- PDF Upload
- AI Responses

(Add screenshots here)

---

## 🌐 Live Demo

### Frontend

https://YOUR_FRONTEND_URL

### Backend API

https://YOUR_BACKEND_URL

---

## 👨‍💻 Author

**Gurmeet Punia**

B.Tech Artificial Intelligence

Vaish College of Engineering, Rohtak

GitHub: https://github.com/YOUR_USERNAME

LinkedIn: https://linkedin.com/in/YOUR_LINKEDIN

---

## ⭐ Support

If you like this project, please ⭐ the repository.