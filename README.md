# DocuQuery AI — RAG-based PDF Q&A Platform

DocuQuery AI, kullanıcıların yüklediği PDF dokümanlarını parçalayarak (chunking) analiz eden, vektör/benzerlik arama yöntemleriyle ilgili bağlamı getiren ve Google Gemini modelleri üzerinden soru-cevap üreten FastAPI tabanlı bir RAG (Retrieval-Augmented Generation) asistanıdır.

---

##  Temel Özellikler

- **RESTful API Mimarisi:** FastAPI ile asenkron uç noktalar üzerinden doküman yükleme ve sorgu işleme.
- **RAG Pipeline:** Yüklenen PDF metinlerinin çıkarımı, anlamsal parçalama (chunking) ve bağlama dayalı yanıt üretimi.
- **LLM Entegrasyonu:** Google GenAI SDK ile `gemini-2.0-flash` model entegrasyonu.
- **Dayanıklılık & Hata Yönetimi:** Dış LLM servislerindeki anlık yoğunluklara (503 Service Unavailable) karşı otomatik yeniden deneme (retry) mekanizması.
- **Docker Desteği:** Konteyner mimarisi ile kolay kurulum ve dağıtım.

---

##  Kullanılan Teknolojiler

- **Backend:** Python 3.11+, FastAPI, Uvicorn, Pydantic
- **LLM & Entegrasyon:** Google GenAI SDK (`google-genai`), PyPDF
- **Ortam & Yapılandırma:** python-dotenv, Docker

---

##  Kurulum ve Çalıştırma

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/zranadegirmenci/rag-pdf-qa-fastapi.git
cd rag-pdf-qa-fastapi
```
### 2. Sanal Ortamı Kurun ve Bağımlılıkları Yükleyin 
```bash
python -m venv .venv
# Windows için:
.venv\Scripts\activate
# macOS / Linux için:
source .venv/bin/activate

pip install -r requirements.txt 
```
### 3. Ortam Değişkenlerini Tanımlayın
Kök dizinde .env dosyası oluşturun ve Gemini API anahtarınızı ekleyin: 
```env  
GEMINI_API_KEY=your_gemini_api_key_here
```
### 4. Sunucuyu Başlatın
```bash
  uvicorn app.main:app --reload 
```
Uygulama varsayılan olarak [http://127.0.0.1:8000](http://127.0.0.1:8000) adresinde çalışacaktır.
İnteraktif Swagger API dokümantasyonuna [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) adresinden erişebilirsiniz.

