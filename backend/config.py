import os
from dotenv import load_dotenv

load_dotenv()

class Settings:

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV = os.getenv("PINECONE_ENV")

    DATABASE_URL = os.getenv("NEON_DATABASE_URL")

settings = Settings()