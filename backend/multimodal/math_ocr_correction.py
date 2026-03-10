import re


def correct_math_ocr(text: str):

    # remove description words
    text = re.sub(
        r"(Example|Solve|Quadratic|Equation|Find|roots|of|the|equation)",
        "",
        text,
        flags=re.IGNORECASE
    )

    # fix OCR mistakes
    text = text.replace("_", "-")
    text = text.replace("Tx", "7x")

    # insert multiplication
    text = re.sub(r'(\d)x', r'\1*x', text)

    # detect quadratic pattern: ax - bx + c = 0
    match = re.search(r'(\d)\*x\s*-\s*(\d)\*x\s*\+\s*(\d)', text)

    if match:
        a, b, c = match.groups()
        text = f"{a}*x**2 - {b}*x + {c} = 0"

    # clean spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()

