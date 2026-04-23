# 🎬 Chinese Subtitle Extractor & Translator (Local Tool)

A fully local Python tool that extracts **hardcoded Simplified Chinese subtitles** from a video and converts them into **English `.srt` subtitles**.

---

## 🚀 Features

- 📽️ Works with videos containing **burned-in (hardcoded) subtitles**
- 🧠 Uses OCR (Tesseract) to detect Chinese text from frames
- 🌍 Translates Chinese → English using offline model (MarianMT)
- ⏱️ Generates accurate timestamps
- 📄 Outputs clean `.srt` subtitle file
- ⚡ Runs completely **offline (no paid APIs)**

---

## 🧠 How It Works
Video → Frame Sampling → Crop Subtitle Area → OCR → Clean Text → Translate → Generate SRT

---

## 📦 Project Structure

```

project/
│
├── main.py
├── ocr.py
├── translator.py
├── subtitle_generator.py
├── utils.py
├── requirements.txt

🛠️ Requirements
🔹 Python
Python 3.9 – 3.11

Install dependencies
pip install -r requirements.txt

Install Tesseract OCR

Download from:
👉 https://github.com/UB-Mannheim/tesseract/wiki

⚠️ IMPORTANT (During Installation)

✔ Check:

Add to PATH
Chinese (Simplified) → chi_sim

Verify installation
tesseract --version
tesseract --list-langs

Expected:

eng
chi_sim
▶️ Usage
python main.py input_video.mp4
⚙️ Optional Arguments
python main.py input.mp4 --fps 0.5 --crop_ratio 0.15
Argument	Description
--fps	Frames per second to sample (default: 1.0)
--crop_ratio	Bottom portion of frame to scan (default: 0.2)
--use_gpu	(Optional, not used for Tesseract)
📄 Output
input_video_english.srt

Example:

1
00:00:05,000 --> 00:00:07,000
Hello Miss Hu

2
00:00:08,000 --> 00:00:10,000
Come in, please
⚠️ Known Limitations
OCR accuracy depends on video quality
Watermarks may sometimes be detected
Translation may not always be perfect
Complex fonts can reduce accuracy
🧹 Improvements Implemented
Removed watermark text (mdapp, madou, etc.)
Filtered non-Chinese noise
Reduced duplicate subtitles
Optimized cropping to subtitle region
🚀 Future Improvements
Better OCR model (PaddleOCR support)
Subtitle line merging
GUI interface
Batch video processing
Higher accuracy translation
🧑‍💻 Tech Stack
OpenCV
Tesseract OCR
Transformers (HuggingFace)
Python
📌 Notes
Fully local tool (no API usage)
Works best with clear, high-resolution subtitles
Recommended crop ratio: 0.15 – 0.25
⭐ Credits

Built as a custom solution for extracting subtitles from videos with hardcoded Chinese text.
