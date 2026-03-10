import sympy as sp
import re

def clean_expression(expr):

    expr = expr.replace("^", "**")
    expr = re.sub(r'(\d)(x)', r'\1*\2', expr)
    expr = re.sub(r'x(\d)', r'x*\1', expr)

    return expr


def solve_calculus(problem_text):

    x = sp.symbols('x')

    match = re.search(r'f\(x\)\s*=\s*(.*)', problem_text)

    if match:
        expr = match.group(1)
    else:
        expr = problem_text

    expr = clean_expression(expr)

    function = sp.sympify(expr)

    derivative = sp.diff(function, x)

    critical_points = sp.solve(derivative, x)

    values = [function.subs(x, cp) for cp in critical_points]

    if not values:
        return "No critical points found"

    max_value = max(values)

    return {
        "derivative": str(derivative),
        "critical_points": [str(c) for c in critical_points],
        "maximum_value": str(max_value)
    }