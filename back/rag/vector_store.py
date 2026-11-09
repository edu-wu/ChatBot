from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

embeddings = OllamaEmbeddings(
    model="mxbai-embed-large"
)


vector_db = Chroma(
    collection_name="documents",
    persist_directory="./chroma_db",
    embedding_function=embeddings
)


def add_document(document_id, text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=250
    )

    chunks = splitter.split_text(text)

    documents = []

    for chunk in chunks:
        if len(chunk.strip()) < 100:
            continue

        doc = Document(
            page_content=chunk,
            metadata={
                "document_id": document_id
            }
        )

        documents.append(doc)

    vector_db.add_documents(documents)

def delete_document_vectors(document_id):

    vector_db.delete(
        where={
            "document_id": str(document_id)
        }
    )
