from backend.llm.groq_client import structured_completion

SYSTEM_PROMPT = """
You are a mathematics tutor.

Solve probability problems step by step.

Return only the final answer.
"""

def solve_probability(problem):

    answer = structured_completion(SYSTEM_PROMPT, problem)

    return answer