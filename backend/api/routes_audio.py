import os
from fastapi import APIRouter, UploadFile, File

from backend.multimodal.speech_to_text import transcribe_audio
from backend.multimodal.math_speech_correction import correct_math_speech
from backend.tools.math_parser import parse_math_expression

router = APIRouter(prefix="/multimodal", tags=["Multimodal"])


@router.post("/audio")
async def solve_from_audio(file: UploadFile = File(...)):

    os.makedirs("temp", exist_ok=True)

    file_path = f"temp/{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Step 1: Speech → Text
    transcript = transcribe_audio(file_path)

    # Step 2: Convert spoken math → symbolic math
    corrected = correct_math_speech(transcript)

    # Step 3: Solve equation
    solution = parse_math_expression(corrected)

    solution = [str(s) for s in solution]

    return {
        "transcription": transcript,
    }