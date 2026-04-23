import cv2
import numpy as np

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # sharpening
    kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
    gray = cv2.filter2D(gray, -1, kernel)

    # threshold
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # convert back to 3 channel
    thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    return thresh

def format_timestamp(seconds):
    """
    Converts seconds to SRT format: HH:MM:SS,ms [cite: 9]
    """
    td_ms = int((seconds % 1) * 1000)
    td_sec = int(seconds)
    mm, ss = divmod(td_sec, 60)
    hh, mm = divmod(mm, 60)
    return f"{hh:02d}:{mm:02d}:{ss:02d},{td_ms:03d}"