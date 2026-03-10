import os
import fitz
from docx import Document

from backend.rag.chunker import chunk_text
from backend.rag.embedder import embed_text
from backend.rag.pinecone_client import get_index

DATA_PATH = "data/math_corpus"

index = get_index()


def read_pdf(path):

    text = ""

    doc = fitz.open(path)

    for page in doc:
        text += page.get_text()

    return text


def read_docx(path):

    doc = Document(path)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def read_txt(path):

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_document(path):

    if path.endswith(".pdf"):
        return read_pdf(path)

    elif path.endswith(".docx"):
        return read_docx(path)

    elif path.endswith(".txt") or path.endswith(".md"):
        return read_txt(path)

    else:
        return ""


def ingest():

    vector_id = 0

    print("Starting ingestion...")

    for filename in os.listdir(DATA_PATH):

        path = os.path.join(DATA_PATH, filename)

        print(f"Processing file: {filename}")

        text = load_document(path)

        if not text:
            print("Skipping empty document")
            continue

        chunks = chunk_text(text)

        print(f"Chunks created: {len(chunks)}")

        for chunk in chunks:

            embedding = embed_text(chunk)

            index.upsert([
                (
                    str(vector_id),
                    embedding,
                    {"text": chunk}
                )
            ])

            vector_id += 1

    print("Ingestion finished.")


if __name__ == "__main__":
    ingest()