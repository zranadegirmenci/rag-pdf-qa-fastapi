import streamlit as st
import requests

st.set_page_config(page_title="PDF Q&A Bot", page_icon="📄", layout="wide")

API_BASE_URL = "http://127.0.0.1:8000"

st.title("📄 PDF Destekli Akıllı Asistan (RAG)")
st.caption("FastAPI & Google Gemini ile güçlendirilmiş doküman tabanlı soru-cevap sistemi")

# Sol Panel: Doküman Yükleme
with st.sidebar:
    st.header("📌 Doküman Yükle")
    uploaded_file = st.file_uploader("Bir PDF dosyası seçin", type=["pdf"])
    
    if uploaded_file is not None:
        if st.button("Dokümanı İndeksle", type="primary"):
            with st.spinner("Doküman analiz ediliyor ve parçalanıyor..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                try:
                    res = requests.post(f"{API_BASE_URL}/upload-pdf", files=files)
                    if res.status_code == 200:
                        st.success("✅ Doküman başarıyla indekslendi!")
                    else:
                        st.error(f"Hata oluştu: {res.text}")
                except Exception as e:
                    st.error(f"Sunucuya bağlanılamadı: {e}")

# Sohbet Geçmişi Durumu
if "messages" not in st.session_state:
    st.session_state.messages = []

# Önceki mesajları ekranda göster
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "context" in msg and msg["context"]:
            with st.expander("🔍 Kaynak Bağlam (Referans Metin)"):
                for idx, c in enumerate(msg["context"], 1):
                    st.markdown(f"**Parça {idx}:** {c}")

# Soru Giriş Alanı
if prompt := st.chat_input("Doküman hakkında bir soru sorun..."):
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # API'ye istek at
    with st.chat_message("assistant"):
        with st.spinner("Cevap hazırlanıyor..."):
            try:
                payload = {"question": prompt, "evaluate": False}
                res = requests.post(f"{API_BASE_URL}/ask", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    answer = data.get("answer", "Cevap alınamadı.")
                    context = data.get("context", [])

                    st.markdown(answer)
                    if context:
                        with st.expander("🔍 Kaynak Bağlam (Referans Metin)"):
                            for idx, c in enumerate(context, 1):
                                st.markdown(f"**Parça {idx}:** {c}")

                    # Asistan yanıtını kaydet
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "context": context
                    })
                else:
                    st.error(f"API Hatası: {res.text}")
            except Exception as e:
                st.error(f"Bağlantı hatası: {e}")