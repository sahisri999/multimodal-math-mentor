from fastapi import APIRouter

router = APIRouter(prefix="/retrieve_context", tags=["RAG"])

@router.post("/")
def retrieve_context(data: dict):

    return {
        "query": data.get("query"),
        "retrieved_docs": []
    }