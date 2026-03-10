from fastapi import APIRouter
from backend.agents.solver_agent import solve_problem


router = APIRouter(prefix="/solve_problem", tags=["Solver"])

@router.post("/")
def solve_problem_route(problem: dict):
    equation = problem.get("parsed")
    parsed_problem = {
        "problem_type": "algebra",
        "equation": equation}
    solution = solve_problem(parsed_problem)
    
    return { "solution": solution }

