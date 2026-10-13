import os
import re
import time
from typing import List, Dict, Any
from pypdf import PdfReader
from google import genai
from google.genai.errors import ServerError


class RAGEngine:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY bulunamadı.")
        self.client = genai.Client(api_key=self.api_key)
        self.documents: List[Dict[str, Any]] = []

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        return re.findall(r"\b\w+\b", text)

    def text_similarity(self, tokens_a: List[str], tokens_b: List[str]) -> float:
        set_a = set(tokens_a)
        set_b = set(tokens_b)
        if not set_a or not set_b:
            return 0.0
        intersection = set_a.intersection(set_b)
        union = set_a.union(set_b)
        return len(intersection) / len(union)

    def load_pdf(self, file_path: str, chunk_size: int = 500, overlap: int = 50) -> int:
        reader = PdfReader(file_path)
        full_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

        words = full_text.split()
        chunks = []
        step = chunk_size - overlap
        if step <= 0:
            step = chunk_size

        for i in range(0, len(words), step):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append({
                    "text": chunk,
                    "tokens": self._tokenize(chunk)
                })

        self.documents = chunks
        return len(chunks)

    # main.py içindeki çağrı için eşleştirme
    def process_pdf(self, file_path: str, chunk_size: int = 500, overlap: int = 50) -> int:
        return self.load_pdf(file_path, chunk_size, overlap)

    def query(self, question: str, top_k: int = 3) -> Dict[str, Any]:
        if not self.documents:
            return {
                "answer": "Henüz sisteme yüklenmiş bir doküman bulunmuyor.",
                "context": []
            }

        q_tokens = self._tokenize(question)

        scored = []
        for doc in self.documents:
            score = self.text_similarity(q_tokens, doc["tokens"])
            scored.append((score, doc["text"]))

        scored.sort(key=lambda x: x[0], reverse=True)
        top_chunks = [item[1] for item in scored[:top_k]]
        context = "\n---\n".join(top_chunks)

        prompt = f"""Aşağıdaki bağlamı kullanarak soruyu yanıtla. Bağlamda bilgi yoksa uydurma, 'Dokümanda bu bilgi yer almamaktadır' de.

Bağlam:
{context}

Soru: {question}
Cevap:"""

        max_retries = 3
        last_error = None
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )
                return {
                    "answer": response.text,
                    "context": top_chunks
                }
            except Exception as exc:
                last_error = exc
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue

        raise last_error