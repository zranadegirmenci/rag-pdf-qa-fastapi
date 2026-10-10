# End-to-End Production-Ready RAG API (PDF Q&A System)

Bu proje, kurum içi PDF dokümanları üzerinden anlamsal arama (semantic retrieval) yaparak kanıta dayalı yanıtlar üreten ve üretilen yanıtları otomatik olarak denetleyen uçtan uca bir **RAG (Retrieval-Augmented Generation)** mimarisidir.

---

## Temel Özellikler
* **Vektör Veritabanı:** `sentence-transformers/all-MiniLM-L6-v2` ile yerel embedding ve `ChromaDB` ile yüksek performanslı anlamsal indeksleme.
* **Akıl Yürütme Motoru:** `Gemini 3.8 Flash` ile bağlama sıkı sıkıya bağlı metin üretimi ve sıfır halüsinasyon hedefi.
* **API Mimarisi:** `FastAPI` tabanlı REST API (`/upload-pdf`, `/ask`).
* **Evaluation (LLM-as-a-Judge):** Yanıtların bağlam doğruluğu (`faithfulness`) ve soru uygunluğu (`answer relevance`) metriklerini denetleyen otomatik değerlendirme katmanı.
* **Konteynerizasyon:** `Docker` ve `Dockerfile` ile platform bağımsız dağıtım mimarisi.

---

## Sistem Mimarisi

```text
[Kullanıcı / İstemci]
        │
        ▼
   [FastAPI] ─── (PDF Yükleme) ───► [Chunking & Embedding (MiniLM)]
        │                                      │
        │                                      ▼
        │                                 [ChromaDB]
        │                                      │
        ├── (Soru Sorma & Arama) ──────────────┘
        │
        ▼
[Gemini 3.8 Flash] ──► [Kanıta Dayalı Yanıt]
        │
        ▼
[LLM-as-a-Judge] ────► [Evaluation Skoru (1-5 Puan)]# rag-pdf-qa-fastapi
Production-ready PDF Q&amp;A system using FastAPI, ChromaDB, Gemini Flash, and LLM-as-a-judge evaluation.
