import requests
import random
import os
import datetime
import urllib.parse

# Yapay zekaya verilecek çok daha detaylı, gerçekçi (photorealistic) İngilizce komutlar
cizim_fikirleri = [
    "A hyper-realistic, National Geographic style photography of the Holy Kaaba in Mecca, highly detailed black cloth with gold embroidery, clear bright day, 8k resolution, photorealistic",
    "The Dome of the Rock (Masjid al-Aqsa) in Jerusalem, glowing beautiful golden dome, detailed blue tile mosaics, clear blue sky, highly detailed architectural photography, 8k",
    "A realistic and majestic view of Al-Masjid an-Nabawi in Medina, beautiful green dome, tall minarets, peaceful morning light, highly detailed, photorealistic",
    "Inside a magnificent grand Islamic mosque, symmetrical beautiful arches, intricate geometric tile patterns, soft glowing sunlight shining through windows, 8k realistic architectural render"
]

# Rastgele bir komut seç
secilen_komut = random.choice(cizim_fikirleri)
print(f"Yapay zekaya verilen detaylı komut: {secilen_komut}")

# Komutu URL'ye uygun hale getir
url_uyumlu_komut = urllib.parse.quote(secilen_komut)
rastgele_seed = random.randint(1, 100000)

# DİKKAT: URL'nin sonuna '&model=flux' ekledik. 
# Bu, çok daha gerçekçi ve yüksek kaliteli çizen gelişmiş bir yapay zeka modelidir.
ai_cizim_url = f"https://image.pollinations.ai/prompt/{url_uyumlu_komut}?width=1080&height=1080&seed={rastgele_seed}&nologo=true&model=flux"

print("Yapay zeka şu anda yüksek kalitede görseli çiziyor (Flux modeli kullanıldığı için birkaç saniye daha uzun sürebilir)...")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

response = requests.get(ai_cizim_url, headers=headers)

if response.status_code == 200:
    # Klasörü oluştur
    os.makedirs('ai_kutsal_mekanlar', exist_ok=True)
    
    # Tarihli dosya adı
    tarih = datetime.datetime.now().strftime('%Y-%m-%d')
    dosya_adi = f'ai_kutsal_mekanlar/{tarih}_ai_mekan.jpg'
    
    # Görseli kaydet
    with open(dosya_adi, 'wb') as f:
        f.write(response.content)
    print(f"Harika! Çok daha gerçekçi yapay zeka görseli çizildi ve '{dosya_adi}' olarak kaydedildi.")
else:
    print(f"Hata: Görsel çizilemedi. Sunucu kodu: {response.status_code}")
