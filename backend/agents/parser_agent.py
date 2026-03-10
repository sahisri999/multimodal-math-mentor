import json
from backend.llm.groq_client import structured_completion


SYSTEM_PROMPT = """
You are a mathematical problem parser.

Your task is to analyze a math problem and return structured JSON.

Identify:

1. topic (choose one):
   - algebra
   - probability
   - calculus
   - linear_algebra

2. expression (if present)
   - For algebra or calculus problems extract the mathematical expression.

3. variables (if present)

4. needs_equation_solver
   - true if equation solving is required
   - false if it is a reasoning problem (probability etc.)

Return ONLY JSON in this format:

{
 "problem_text": "...",
 "topic": "algebra | probability | calculus | linear_algebra",
 "expression": "...",
 "variables": [],
 "needs_equation_solver": true
}

Rules:
- Probability questions usually contain words like:
  probability, chance, random, cards, balls, dice.

- Calculus questions contain:
  derivative, limit, maximum, minimum, optimize.

- Algebra questions contain equations.

- Linear algebra questions contain matrices or systems of equations.
"""


def parse_problem(user_input: str):

    response = structured_completion(
        SYSTEM_PROMPT,
        user_input
    )

    try:
        parsed = json.loads(response)
        return parsed

    except Exception:

        return {
            "problem_text": user_input,
            "topic": "algebra",
            "expression": user_input,
            "variables": [],
            "needs_equation_solver": True
        }
    if "probability" in user_input.lower():
       topic = "probability"

    elif "maximum" in user_input.lower() or "derivative" in user_input.lower():
       topic = "calculus"