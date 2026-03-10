import sympy as sp
from sympy import Matrix


def solve_linear_algebra(problem_text: str):
    """
    Solve basic linear algebra problems such as:
    - system of linear equations
    - determinant
    - matrix inverse
    """

    try:

        # ------------------------------------------------
        # CASE 1 — SYSTEM OF LINEAR EQUATIONS
        # Example: Solve 2x + y = 5 and x - y = 1
        # ------------------------------------------------
        if "solve" in problem_text.lower() and "=" in problem_text:

            x, y, z = sp.symbols('x y z')

            equations = []

            parts = problem_text.replace("Solve", "").replace("solve", "").split("and")

            for eq in parts:
                lhs, rhs = eq.split("=")
                equations.append(sp.Eq(sp.sympify(lhs.strip()), sp.sympify(rhs.strip())))

            solution = sp.solve(equations)

            return solution

        # ------------------------------------------------
        # CASE 2 — DETERMINANT
        # Example: determinant of [[1,2],[3,4]]
        # ------------------------------------------------
        if "determinant" in problem_text.lower():

            matrix_text = problem_text.split("[[")[1].split("]]")[0]

            rows = matrix_text.split("],[")

            matrix = []

            for row in rows:
                matrix.append([int(x) for x in row.split(",")])

            M = Matrix(matrix)

            return M.det()

        # ------------------------------------------------
        # CASE 3 — MATRIX INVERSE
        # ------------------------------------------------
        if "inverse" in problem_text.lower():

            matrix_text = problem_text.split("[[")[1].split("]]")[0]

            rows = matrix_text.split("],[")

            matrix = []

            for row in rows:
                matrix.append([int(x) for x in row.split(",")])

            M = Matrix(matrix)

            return M.inv()

        # ------------------------------------------------
        # DEFAULT
        # ------------------------------------------------
        return "Unable to solve linear algebra problem"

    except Exception as e:

        return f"Error solving linear algebra problem: {str(e)}"