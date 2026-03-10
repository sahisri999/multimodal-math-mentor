from fastapi import APIRouter
from backend.agents.verifier_agent import verify_solution

router = APIRouter(prefix="/verify_problem", tags=["Verifier"])


@router.post("/")
def verify_problem(problem: dict):

    expression = problem.get("expression")
    variable = problem.get("variable")
    solutions = problem.get("solutions")

    verification = verify_solution(expression, variable, solutions)

    return {
        "verification": verification
    }