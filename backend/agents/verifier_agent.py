from sympy import symbols, sympify, Eq, solve


def verify_solution(equation, solutions):

    try:
        left, right = equation.split("=")

        expr = sympify(left) - sympify(right)

        x = symbols("x")

        for sol in solutions:

            if expr.subs(x, sol) != 0:
                return False

        return True

    except:
        return False