import json
from google import genai
from google.genai import types

class RAGEvaluator:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.instruction = """
Sen RAG sistemlerini denetleyen tarafsız bir Baş Yapay Zekâ Denetçisisin.
Verilen soru, bağlam ve yanıta göre şu metrikleri 1-5 arası puanla ve saf JSON döndür:
{
    "baglam_uyumu": 1-5,
    "soru_uygunlugu": 1-5,
    "denetci_gerekcesi": "Açıklama"
}
"""

    def evaluate(self, question: str, context: str, answer: str):
        prompt = f"Soru: {question}\nBağlam: {context}\nYanıt: {answer}"
        response = self.client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.instruction,
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)