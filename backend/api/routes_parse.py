from fastapi import APIRouter
from pydantic import BaseModel
from backend.agents.parser_agent import parse_problem

router = APIRouter()


class ParseRequest(BaseModel):
    problem: str


@router.post("/parse_problem/")
def parse_problem_endpoint(request: ParseRequest):

    parsed = parse_problem(request.problem)

    return parsed