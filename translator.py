from transformers import MarianMTModel, MarianTokenizer
import torch

class SubtitleTranslator:
    def __init__(self, model_name="Helsinki-NLP/opus-mt-zh-en"):
        # Local offline translation using HuggingFace [cite: 5, 9]
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.model = MarianMTModel.from_pretrained(model_name).to(self.device)

    def translate(self, text):
        if not text:
            return ""
        
        # Tokenize and generate translation [cite: 9]
        batch = self.tokenizer([text], return_tensors="pt", padding=True).to(self.device)
        gen = self.model.generate(**batch)
        
        translated_text = self.tokenizer.batch_decode(gen, skip_special_tokens=True)
        return translated_text[0]
    
    def translate_batch(self, texts):
        batch = self.tokenizer(texts, return_tensors="pt", padding=True, truncation=True).to(self.device)
        gen = self.model.generate(**batch)
        return self.tokenizer.batch_decode(gen, skip_special_tokens=True)