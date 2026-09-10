import requests
import random
import os
import datetime

# Telifsiz, yüksek kaliteli Kabe, Aksa ve Cami görsellerinin havuzu
gorsel_havuzu = [
    "https://images.unsplash.com/photo-1565552643983-c2efd020e58d?w=1080", # Kabe 1
    "https://images.unsplash.com/photo-1591462061214-4fb985b8eb83?w=1080", # Kabe 2
    "https://images.unsplash.com/photo-1587595431973-160d0d94add1?w=1080", # Mescid-i Aksa (Kubbet'üs Sahra)
    "https://images.unsplash.com/photo-1604928113702-8a9d186fde01?w=1080", # Mescid-i Nebevi
    "https://images.unsplash.com/photo-1542281084-2f22f778db86?w=1080", # İhtişamlı bir cami
    "https://images.unsplash.com/photo-1566908906915-0d2cc37a89e9?w=1080"  # Cami silüeti
]

# Rastgele bir görsel seç
secilen_gorsel_url = random.choice(gorsel_havuzu)

print("Görsel indiriliyor...")
response = requests.get(secilen_gorsel_url)

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
    print("Hata: Görsel indirilemedi.")
