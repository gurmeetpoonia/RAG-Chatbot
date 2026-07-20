#upload
#my-pdfs
#pdf/{id}
#conversation/add-pdf
#conversation/remove-pdf

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import hashlib
import uuid
import fitz
from auth import get_current_user
from models import PDF, User
import fitz
import io
import pytesseract
from PIL import Image
from docx import Document

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from services.vector_store import model, collection
from langchain_text_splitters import RecursiveCharacterTextSplitter
from Dependencies import get_db
router = APIRouter(prefix="", tags=["PDF"])

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    extension = file.filename.split(".")[-1].lower()

    text = ""
    pdf_bytes = await file.read()
    file_hash=hashlib.sha256(pdf_bytes).hexdigest()
    existing_pdf = db.query(PDF).filter(
    PDF.file_hash == file_hash,
    PDF.user_id == current_user.id
).first()
    if existing_pdf:
        return {"filename": existing_pdf.filename, "pdf_id": existing_pdf.id, "message": "File already exists in your library"}

    try:

        # ==========================
        # PDF
        # ==========================

        if extension == "pdf":

            pdf = fitz.open(
                stream=pdf_bytes,
                filetype="pdf"
            )

            for page in pdf:
                text += page.get_text()

            if len(text.strip()) == 0:

                print("Scanned PDF detected. Running OCR...")

                pdf = fitz.open(
                    stream=pdf_bytes,
                    filetype="pdf"
                )

                for page in pdf:

                    pix = page.get_pixmap(dpi=300)

                    img = Image.open(
                        io.BytesIO(
                            pix.tobytes("png")
                        )
                    )

                    text += pytesseract.image_to_string(img)

        # ==========================
        # TXT
        # ==========================

        elif extension == "txt":

            text = pdf_bytes.decode(
                "utf-8",
                errors="ignore"
            )

        # ==========================
        # DOCX
        # ==========================

        elif extension == "docx":

            document = Document(
                io.BytesIO(pdf_bytes)
            )

            for para in document.paragraphs:

                text += para.text + "\n"

        # ==========================
        # Unsupported
        # ==========================

        else:

            raise HTTPException(
                status_code=400,
                detail="Only PDF, TXT and DOCX files are supported."
            )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=f"Unable to read file : {str(e)}"
        )

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_text(text)

    if not chunks or len(text.strip()) == 0:
        raise HTTPException(
            status_code=400, 
            detail="No readable text found inside document."
        )

    embeddings = model.encode(chunks)
    
    # Save to SQL Database
    new_pdf = PDF(filename=file.filename,file_hash=file_hash, user_id=current_user.id, chroma_collection="pdf_data")
    db.add(new_pdf)
    db.commit()
    db.refresh(new_pdf)
    
    # Save to Vector Database (ChromaDB)
    try:
        collection.add(
            documents=chunks,
            embeddings=embeddings.tolist(),
            ids=[str(uuid.uuid4()) for _ in chunks],
            metadatas=[
                {
                    "filename": file.filename,
                    "user_id": current_user.id,
                    "pdf_id": new_pdf.id
                }
                for _ in chunks
            ]
        )
    except Exception as e:
        db.delete(new_pdf)
        db.commit()
        raise HTTPException(status_code=500, detail=f"Vector DB entry failed: {str(e)}")

    return {"filename": file.filename, "pdf_id": new_pdf.id,
             "message": "Uploaded successfully"}

@router.delete("/pdf/{pdf_id}")
def delete_pdf(pdf_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    pdf = db.query(PDF).filter(PDF.id == pdf_id, PDF.user_id == current_user.id).first()
    if pdf is None:
        raise HTTPException(status_code=404, detail="PDF not found")
    
    try:
        collection.delete(where={"pdf_id": pdf_id, "user_id": current_user.id})
    except Exception:
        pass 
        
    db.delete(pdf)
    db.commit()
    return {"message": "document deleted successfully"}

@router.get("/my-pdfs")
def get_my_pdfs(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    pdfs = db.query(PDF).filter(PDF.user_id == current_user.id).all()
    return [{"id": pdf.id, "filename": pdf.filename} for pdf in pdfs]
