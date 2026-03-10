import sympy as sp

def solve_problem(parsed_problem):
    if isinstance(parsed_problem, str):
        equation = parsed_problem
    else:
        equation = parsed_problem.get("equation")

    if "=" not in equation:
        return {"error": "Equation not detected"}

    x = sp.symbols("x")

    left, right = equation.split("=")

    eq = sp.Eq(sp.sympify(left), sp.sympify(right))

    solution = sp.solve(eq, x)

    return [str(s) for s in solution]
