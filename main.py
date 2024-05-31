from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi import Form
from pydantic import BaseModel

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

# FastAPI uygulamasını oluşturuyoruz
app = FastAPI()

# CORS (Cross-Origin Resource Sharing) politikalarını yapılandırma
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],  # Hangi kaynaklardan gelen isteklere izin verildiği
    allow_credentials=True,  # Kimlik doğrulama bilgilerine izin verilip verilmediği
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # İzin verilen HTTP metodları
    allow_headers=["*"],  # İzin verilen HTTP başlıkları
)

# Ana sayfayı sunan GET isteği
  # index.html dosyasını döndürür

# InputData sınıfı, gelen POST verilerini doğrulamak için kullanılır
class InputData(BaseModel):
    Text1: str = Form(...)  # Formdan gelen Text1 alanı
    Text2: str = Form(...)  # Formdan gelen Text2 alanı

# POST isteği için analiz fonksiyonu
@app.post("/analiz")
def analiz(data: InputData):
    # Gelen metinleri bir listeye koyuyoruz
    metinler = [data.Text1, data.Text2]
    # Metinleri filtreleyip durak kelimelerini çıkarıyoruz
    metinler = [filter_text(metin) for metin in metinler]
    metinler = [remove_stopwords(metin) for metin in metinler]
    
    # Metinleri sayısal vektörlere dönüştürmek için CountVectorizer kullanıyoruz
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(metinler)
    
    # Vektörler arasındaki kosinüs benzerliğini hesaplıyoruz
    similarity_matrix = cosine_similarity(X, X)
    
    # Benzerlik matrisini çiziyoruz
    plt.imshow(similarity_matrix, cmap='viridis', interpolation='nearest')
    plt.colorbar(label='Benzerlik')  # Renk çubuğu ekliyoruz
    plt.title('Benzerlik Matrisi')  # Başlık ekliyoruz
    plt.xlabel('Örnek Numarası')  # X ekseni etiketi
    plt.ylabel('Örnek Numarası')  # Y ekseni etiketi
    plt.xticks(ticks=np.arange(2))  # X ekseni işaretleri
    plt.yticks(ticks=np.arange(2))  # Y ekseni işaretleri
    plt.grid(False)  # Grid çizgilerini kapatıyoruz
    
    # Görseli bellekteki bir byte dizisine kaydediyoruz
    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)  # Belleğin başlangıcına gidiyoruz
    img_base64 = base64.b64encode(img_data.read()).decode()  # Görseli base64 formatına çeviriyoruz
    plt.close()  # Matplotlib penceresini kapatıyoruz
    
    # Yanıt olarak görseli ve benzerlik matrisini döndürüyoruz
    return {"request": "request", "image": f"data:image/png;base64,{img_base64}", "similarity_matrix": similarity_matrix.tolist()}

# Türkçe durak kelimelerini nltk kütüphanesinden alıyoruz
stop_words = set(stopwords.words('turkish'))

# Metinleri filtreleyen fonksiyon
def filter_text(text):
    text = text.encode('ascii', 'ignore').decode('ascii')  # ASCII dışı karakterleri kaldırıyoruz
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Harf ve rakam dışı karakterleri kaldırıyoruz
    text = re.sub(r'\s+', ' ', text)  # Fazla boşlukları tek boşluğa indiriyoruz
    text = text.strip()  # Baş ve sondaki boşlukları kaldırıyoruz
    return text

# Durak kelimelerini çıkaran fonksiyon
def remove_stopwords(text):
    words = word_tokenize(text, "turkish")  # Metni kelimelere ayırıyoruz
    filtered_words = [word for word in words if word.lower() not in stop_words]  # Durak kelimeleri çıkarıyoruz
    return ' '.join(filtered_words)  # Kelimeleri tekrar birleştirip metin haline getiriyoruz
