from backend.llm.groq_client import structured_completion


def generate_explanation(problem_text, solution):

    system_prompt = """

You are a mathematics tutor.

Explain the solution step-by-step.

Rules:
- Use numbered steps
- Use simple language
- Do not use markdown formatting
- Return plain text explanation
"""

    user_prompt = f"""
Problem:
{problem_text}

Solution:
{solution}

Explain how this solution is obtained step by step.
"""

    explanation = structured_completion(system_prompt, user_prompt)

    return explanation