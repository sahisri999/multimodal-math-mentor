import re


def correct_math_speech(text: str):

    text = text.lower()

    replacements = {
        "equals to": "=",
        "equals": "=",
        "equal to": "=",
        "equal": "=",
        "minus": "-",
        "plus": "+",
        "times": "*",
        "multiplied by": "*",
        "square": "^2",
        "squared": "^2"
    }

    for word, symbol in replacements.items():
        text = text.replace(word, symbol)

    numbers = {
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9"
    }

    for word, digit in numbers.items():
        text = text.replace(word, digit)

    # remove unnecessary words
    text = re.sub(r"(solve|equation)", "", text)

    # insert multiplication
    text = re.sub(r'(\d)x', r'\1*x', text)

    text = text.replace("^", "**")

    text = re.sub(r"\s+", " ", text)

    return text.strip()