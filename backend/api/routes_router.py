from fastapi import APIRouter
from backend.agents.router_agent import run_math_pipeline

router = APIRouter(prefix="/agent", tags=["Math Agent"])


@router.post("/solve")

def solve(problem: dict):

    text = problem.get("problem")

    result = run_math_pipeline(text)

    return result