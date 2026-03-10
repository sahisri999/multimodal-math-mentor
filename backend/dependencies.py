from groq import Groq
from backend.config import settings

groq_client = Groq(api_key=settings.GROQ_API_KEY)

def get_groq_client():
    return groq_client