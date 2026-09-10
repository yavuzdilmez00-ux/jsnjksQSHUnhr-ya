import requests
import random
import os
import datetime
import urllib.parse

# Yapay zekaya vereceğimiz İngilizce çizim komutları (Prompts)
cizim_fikirleri = [
    "A hyper-realistic photography of the Kaaba in Mecca, beautiful golden hour lighting, 8k resolution, cinematic",
    "A majestic Islamic mosque with intricate geometric tiles, glowing warm light at sunset, highly detailed",
    "Masjid al-Aqsa in Jerusalem during morning mist, peaceful and serene atmosphere, photorealistic",
    "A beautiful modern mosque interior with light rays shining through stained glass windows, unreal engine 5 render",
    "A stunning grand mosque in the mountains, surrounded by nature and peace, highly detailed photography"
]

# Rastgele bir çizim komutu seç
secilen_komut = random.choice(cizim_fikirleri)
print(f"Yapay zekaya verilen komut: {secilen_komut}")

# Komutu URL formatına (boşlukları %20 yapacak şekilde) dönüştür
url_uyumlu_komut = urllib.parse.quote(secilen_komut)

# Rastgelelik katmak için sonuna rastgele bir sayı ekliyoruz (her seferinde farklı çizsin diye)
rastgele_seed = random.randint(1, 100000)

# Şifresiz AI çizim servisi URL'si
ai_cizim_url = f"https://image.pollinations.ai/prompt/{url_uyumlu_komut}?width=1080&height=1080&seed={rastgele_seed}&nologo=true"

print("Yapay zeka şu anda sıfırdan görseli çiziyor (bu biraz sürebilir)...")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(ai_cizim_url, headers=headers)

if response.status_code == 200:
    # Klasörü oluştur
    os.makedirs('ai_kutsal_mekanlar', exist_ok=True)
    
    # Bugünün tarihiyle dosya adını belirle
    tarih = datetime.datetime.now().strftime('%Y-%m-%d')
    dosya_adi = f'ai_kutsal_mekanlar/{tarih}_ai_mekan.jpg'
    
    # Çizilen görseli kaydet
    with open(dosya_adi, 'wb') as f:
        f.write(response.content)
    print(f"Mükemmel! Yapay zeka görseli çizdi ve '{dosya_adi}' olarak kaydedildi.")
else:
    print(f"Hata: Görsel çizilemedi. Kod: {response.status_code}")
