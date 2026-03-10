from fastapi import APIRouter
from backend.agents.explainer_agent import generate_explanation

router = APIRouter(prefix="/explain_problem", tags=["Explainer"])


@router.post("/")
def explain_problem(data: dict):

    problem_text = data.get("problem")
    solution = data.get("solution")

    explanation = generate_explanation(problem_text, solution)

    return {
        "problem": problem_text,
        "solution": solution,
        "explanation": explanation
    }