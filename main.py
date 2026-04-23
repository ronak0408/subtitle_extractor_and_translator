import cv2
import argparse
import os
from ocr import OCRProcessor
from translator import SubtitleTranslator
from subtitle_generator import SubtitleGenerator
from utils import preprocess_image

def main():
    parser = argparse.ArgumentParser(description="Hardcoded Chinese Subtitle Extractor & Translator")
    parser.add_argument("input", help="Path to input video file")
    parser.add_argument("--fps", type=float, default=1.0, help="Frames per second to sample")
    parser.add_argument("--crop_ratio", type=float, default=0.2, help="Bottom portion to crop (0.2 = 20%)")
    parser.add_argument("--use_gpu", action="store_true", help="Use GPU for OCR and Translation")
    args = parser.parse_args()

    print("[1/4] Loading models...")
    ocr_engine = OCRProcessor(use_gpu=args.use_gpu)
    translator_engine = SubtitleTranslator()
    sub_gen = SubtitleGenerator()

    cap = cv2.VideoCapture(args.input)
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    sample_interval = int(video_fps / args.fps)
    crop_height = int(height * args.crop_ratio)
    
    raw_frame_data = []

    print(f"[2/4] Processing video: {args.input}")
    current_frame = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        if current_frame % sample_interval == 0:
            timestamp = current_frame / video_fps
            
            # Crop to subtitle region (Bottom portion only) [cite: 8]
            roi = frame[height - crop_height : height, 0 : width]
            processed_roi = preprocess_image(roi)
            
            # OCR Extraction [cite: 8]
            text = ocr_engine.extract_text(processed_roi)
            if text:
                raw_frame_data.append((timestamp, text))
                print(f"[{timestamp:.2f}s] OCR: {text}")

        current_frame += 1

    cap.release()

    print("[3/4] Grouping and Translating...")
    frame_duration = sample_interval / video_fps
    grouped_subs = sub_gen.process_frames(raw_frame_data, frame_duration)
    
    print(f"Total subtitles: {len(grouped_subs)}")

    for i, sub in enumerate(grouped_subs):
        try:
            print(f"Translating {i+1}/{len(grouped_subs)}: {sub['text']}")
            sub['translated_text'] = translator_engine.translate(sub['text'])
        except Exception as e:
            print(f"Translation failed: {e}")
            sub['translated_text'] = sub['text']

    print("[4/4] Generating SRT...")
    output_filename = os.path.splitext(args.input)[0] + "_english.srt"
    sub_gen.write_srt(grouped_subs, output_filename)
    
    print(f"Done! Subtitles saved to: {output_filename}") 

if __name__ == "__main__":
    main()