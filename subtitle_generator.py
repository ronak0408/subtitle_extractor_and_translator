from difflib import SequenceMatcher

from utils import format_timestamp

class SubtitleGenerator:
    def __init__(self):
        self.subtitles = []

    def get_similarity(self, a, b):
        # Change detection using sequence matching [cite: 9]
        return SequenceMatcher(None, a, b).ratio()

    def process_frames(self, frame_data, frame_duration):
        """
        Groups frame-by-frame OCR results into subtitle blocks with durations. [cite: 9]
        """
        if not frame_data:
            return []

        processed_subs = []
        current_sub = None

        for timestamp, text in frame_data:
            if current_sub and text == current_sub["text"]:
                continue
            if not text:
                if current_sub:
                    processed_subs.append(current_sub)
                    current_sub = None
                continue
            if processed_subs and text == processed_subs[-1]["text"]:
                continue

            if current_sub is None:
                current_sub = {"text": text, "start": timestamp, "end": timestamp + frame_duration}
            else:
                # If similarity > 0.85, it is considered the same subtitle block [cite: 9]
                if self.get_similarity(text, current_sub["text"]) > 0.7:
                    current_sub["end"] = timestamp + frame_duration
                else:
                    processed_subs.append(current_sub)
                    current_sub = {"text": text, "start": timestamp, "end": timestamp + frame_duration}

        if current_sub:
            processed_subs.append(current_sub)
            
        return processed_subs

    def write_srt(self, subtitles, output_path):
        # Writes final SRT with sequential numbering and proper formatting [cite: 9]
        with open(output_path, "w", encoding="utf-8") as f:
            for i, sub in enumerate(subtitles, 1):
                f.write(f"{i}\n")
                f.write(f"{format_timestamp(sub['start'])} --> {format_timestamp(sub['end'])}\n")
                f.write(f"{sub['translated_text']}\n\n")