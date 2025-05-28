import os
import cv2
import pytesseract
import pdfplumber
from PIL import Image

def extract_text_from_file(path):
    ext = os.path.splitext(path)[1].lower()

    if ext == ".txt":
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().strip(), None, 100

    elif ext == ".pdf":
        with pdfplumber.open(path) as pdf:
            text = "\n".join([page.extract_text() or "" for page in pdf.pages])
            return text.strip(), None, 100

    elif ext in [".jpg", ".png"]:
        return extract_text_from_image(path)

    elif ext in [".py", ".java", ".cpp", ".c"]:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().strip(), None, 100

    return "", None, 100  # fallback

def extract_text_from_image(img_path):
    image = cv2.imread(img_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2
    )

    temp_path = "temp_processed.png"
    cv2.imwrite(temp_path, thresh)

    text = pytesseract.image_to_string(Image.open(temp_path), config='--oem 1 --psm 6')
    os.remove(temp_path)

    return text.strip(), img_path, 100  # fixed 100% confidence



