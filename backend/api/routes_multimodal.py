from fastapi import APIRouter, UploadFile, File
import shutil

from backend.multimodal.ocr_processor import extract_text_from_image
from backend.multimodal.math_ocr_correction import correct_math_ocr
from backend.tools.math_parser import parse_math_expression

router = APIRouter(prefix="/multimodal", tags=["multimodal"])


@router.post("/image")
async def solve_from_image(file: UploadFile = File(...)):

    file_location = f"temp_{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_image(file_location)

    corrected = correct_math_ocr(text)

    return {
        "parsed_problem": corrected,
    }
    