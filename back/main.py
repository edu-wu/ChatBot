from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from rag.vector_store import delete_document_vectors
from rag.chatbot import ask_question
from pydantic import BaseModel
import shutil
import os
import uuid

from database.database import (
    init_db,
    get_connection
)

from rag.pdf_loader import extract_text
from rag.vector_store import add_document


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

class Question(BaseModel):
    question: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():

    return {
        "message": "API funcionando"
    }


@app.get("/documents")
def get_documents():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            filename,
            file_path,
            status,
            created_at
        FROM documents
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    documents = []

    for row in rows:

        documents.append({
            "id": row[0],
            "filename": row[1],
            "file_path": row[2],
            "status": row[3],
            "created_at": row[4]
        })

    return documents

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    os.makedirs("uploads", exist_ok=True)

    unique_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(
        "uploads",
        unique_name
    )


    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO documents
        (
            filename,
            file_path,
            status
        )
        VALUES
        (?, ?, ?)
        """,
        (
            file.filename,
            file_path,
            "ready"
        )
    )

    conn.commit()

    document_id = cursor.lastrowid

    conn.close()

    text = extract_text(file_path)

    add_document(
        str(document_id),
        text
    )

    return {
        "id": document_id,
        "filename": file.filename,
        "file_path": file_path,
        "status": "ready"
    }

@app.delete("/documents/{document_id}")
def delete_document(document_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT file_path
        FROM documents
        WHERE id = ?
        """,
        (document_id,)
    )

    row = cursor.fetchone()

    if row:
        file_path = row[0]

        if os.path.exists(file_path):
            os.remove(file_path)
        delete_document_vectors(document_id)

    cursor.execute(
        """
        DELETE FROM documents
        WHERE id = ?
        """,
        (document_id,)
    )

    conn.commit()
    conn.close()

    return {
        "message": "Documento eliminado"
    }

@app.post("/chat")
def chat(data: Question):

    answer = ask_question(
        data.question
    )

    return {
        "response": answer
    }