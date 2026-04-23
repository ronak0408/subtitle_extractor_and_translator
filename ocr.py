import pytesseract
import cv2
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class OCRProcessor:
    def __init__(self, use_gpu=False):
        pass

    def extract_text(self, image):
        text = pytesseract.image_to_string(image, lang='chi_sim')

        if not text:
            return ""

        text = text.strip()

        # ❌ Remove watermark patterns
        blacklist = ["mdapp", "madou", "tv", "com", "www"]
        if any(word in text.lower() for word in blacklist):
            return ""

        # ❌ Remove very short garbage
        if len(text) < 3:
            return ""

        # ❌ Keep mostly Chinese text
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
        if len(chinese_chars) < 2:
            return ""

        # ✅ Clean unwanted symbols
        text = re.sub(r"[^\u4e00-\u9fff0-9a-zA-Z\s]", "", text)

        return text.strip()