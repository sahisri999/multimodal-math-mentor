from backend.agents.parser_agent import parse_problem
from backend.agents.solver_agent import solve_problem
from backend.agents.verifier_agent import verify_solution
from backend.agents.explainer_agent import generate_explanation
from backend.rag.retriever import retrieve_context

from backend.memory.memory_store import retrieve_conversation, store_conversation
from backend.memory.db import SessionLocal

# topic specific solvers
from backend.tools.probability_solver import solve_probability
from backend.tools.calculus_solver import solve_calculus
from backend.tools.linear_algebra_solver import solve_linear_algebra


def run_pipeline(problem_text):

    db = SessionLocal()

    try:

        # -----------------------------
        # STEP 1 — MEMORY CHECK
        # -----------------------------
        memory = retrieve_conversation(db, problem_text)

        if memory:
            return {
                "solution": memory.solution,
                "verified": True,
                "explanation": memory.explanation,
                "context": "Retrieved from memory"
            }

        # -----------------------------
        # STEP 2 — PARSE PROBLEM
        # -----------------------------
        parsed = parse_problem(problem_text)

        topic = parsed.get("topic")
        equation = parsed.get("expression")

        # -----------------------------
        # STEP 3 — ROUTE TO SOLVER
        # -----------------------------

        # ALGEBRA
        if topic == "algebra" and equation:

            solution = solve_problem(equation)
            verified = verify_solution(equation, solution)

        # CALCULUS
        elif topic == "calculus":

            solution = solve_calculus(problem_text)
            verified = True

        # PROBABILITY
        elif topic == "probability":

            solution = solve_probability(problem_text)
            verified = True

        # LINEAR ALGEBRA
        elif topic == "linear_algebra":

            solution = solve_linear_algebra(problem_text)
            verified = True

        # FALLBACK
        else:

            solution = "Could not classify problem"
            verified = False

        # -----------------------------
        # STEP 4 — GENERATE EXPLANATION
        # -----------------------------
        explanation = generate_explanation(problem_text, solution)

        # -----------------------------
        # STEP 5 — RETRIEVE RAG CONTEXT
        # -----------------------------
        context = retrieve_context(problem_text)

        # -----------------------------
        # STEP 6 — STORE MEMORY
        # -----------------------------
        if solution and "error" not in str(solution):

            store_conversation(
                db,
                problem_text,
                str(solution),
                explanation
            )

        # -----------------------------
        # FINAL RESPONSE
        # -----------------------------
        return {
            "solution": solution,
            "verified": verified,
            "explanation": explanation,
            "context": context
        }

    finally:
        db.close()