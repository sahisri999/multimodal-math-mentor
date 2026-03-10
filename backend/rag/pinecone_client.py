import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")

pc = Pinecone(api_key=PINECONE_API_KEY)

INDEX_NAME = "math-mentor-index"


def get_index():

    if INDEX_NAME not in pc.list_indexes().names():

        pc.create_index(
            name=INDEX_NAME,
            dimension=1024,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region=PINECONE_ENV
            )
        )

    return pc.Index(INDEX_NAME)