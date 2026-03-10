import easyocr
from PIL import Image

reader = easyocr.Reader(['en'])

def extract_text_from_image(image_path: str):

    result = reader.readtext(image_path)

    text = ""
    for r in result:
        text += r[1] + " "

    return text.strip()