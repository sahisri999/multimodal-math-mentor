from fastapi import APIRouter
from backend.agents.router_agent import run_pipeline

router = APIRouter(prefix="/agent", tags=["Agent Router"])

@router.post("/solve")
def solve(problem: dict):

    text = problem.get("problem")

    result = run_pipeline(text)

    return result