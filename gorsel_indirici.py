import requests
import random
import os
import datetime

# Telifsiz, yüksek kaliteli Kabe, Aksa ve Cami görsellerinin havuzu
gorsel_havuzu = [
    "https://images.unsplash.com/photo-1565552643983-c2efd020e58d?w=1080",
    "https://images.unsplash.com/photo-1591462061214-4fb985b8eb83?w=1080",
    "https://images.unsplash.com/photo-1587595431973-160d0d94add1?w=1080",
    "https://images.unsplash.com/photo-1604928113702-8a9d186fde01?w=1080",
    "https://images.unsplash.com/photo-1542281084-2f22f778db86?w=1080",
    "https://images.unsplash.com/photo-1566908906915-0d2cc37a89e9?w=1080"
]

# Rastgele bir görsel seç
secilen_gorsel_url = random.choice(gorsel_havuzu)

print("Görsel indiriliyor...")

# Bot olduğumuzu gizlemek için sahte bir tarayıcı kimliği (User-Agent) ekliyoruz
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Siteye bağlanırken bu sahte kimliği kullanıyoruz
response = requests.get(secilen_gorsel_url, headers=headers)

if response.status_code == 200:
    # Klasörü oluştur
    os.makedirs('kutsal_mekanlar', exist_ok=True)
    
    # Bugünün tarihiyle dosya adını belirle
    tarih = datetime.datetime.now().strftime('%Y-%m-%d')
    dosya_adi = f'kutsal_mekanlar/{tarih}_mekan.jpg'
    
    # Görseli kaydet
    with open(dosya_adi, 'wb') as f:
        f.write(response.content)
    print(f"Başarılı! Görsel '{dosya_adi}' olarak kaydedildi.")
else:
    # Eğer yine hata verirse, sebebini anlamak için durum kodunu yazdır
    print(f"Hata: Görsel indirilemedi. Sunucu şu kodu döndürdü: {response.status_code}")
