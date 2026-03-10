from fastapi import FastAPI
from backend.api import (
    routes_parse,
    routes_retrieve,
    routes_solve,
    routes_verify,
    routes_explain,
    routes_memory,
    
)

from backend.memory.db import init_db  
from backend.api import routes_multimodal
from backend.api import routes_audio
from backend.api import routes_agent
from backend.api.routes_feedback import router as feedback_router

app = FastAPI(
    title="Multimodal Math Mentor",
    description="RAG + Multi-Agent Math Solver",
    version="1.0"
)

init_db()

app.include_router(routes_parse.router)
app.include_router(routes_retrieve.router)
app.include_router(routes_solve.router)
app.include_router(routes_verify.router)
app.include_router(routes_explain.router)
app.include_router(routes_memory.router)
app.include_router(routes_multimodal.router)
app.include_router(routes_audio.router)
app.include_router(routes_agent.router)
app.include_router(feedback_router)


@app.get("/")
def root():
    return {"message": "Multimodal Math Mentor API Running"}