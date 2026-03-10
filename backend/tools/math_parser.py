import sympy as sp
import re


def sanitize_expression(text):

    # keep only math characters
    text = re.sub(r"[^0-9xX+\-*/^=() ]", "", text)

    # normalize x
    text = text.replace("X", "x")

    # convert x^2 → x**2
    text = text.replace("^", "**")

    # insert multiplication (2x → 2*x)
    text = re.sub(r'(\d)x', r'\1*x', text)

    # remove duplicate spaces
    text = re.sub(r"\s+", " ", text)
    
    text = text.replace("** ", "**")

    return text.strip()


def parse_math_expression(text):

    cleaned = sanitize_expression(text)

    # if no equation detected return empty solution
    if "=" not in cleaned:
        return []

    try:
        left, right = cleaned.split("=")

        x = sp.symbols("x")

        equation = sp.Eq(sp.sympify(left), sp.sympify(right))

        solution = sp.solve(equation, x)

        return solution

    except Exception:
        return []