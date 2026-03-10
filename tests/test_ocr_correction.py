import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.multimodal.math_ocr_correction import correct_math_ocr

text = "Solve x2 - 5x + 6 = 0"

print(correct_math_ocr(text))