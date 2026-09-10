import requests
import random
import os
import datetime
import urllib.parse

# Yapay zekanın kusursuz çizdiği, mimari hatalara düşmeyeceği harika komutlar
cizim_fikirleri = [
    "A hyper-realistic stunning interior of a grand Islamic mosque, beautiful glowing stained glass windows, intricate geometric tile patterns, soft volumetric light rays, 8k resolution, photorealistic",
    "A beautiful silhouette of a grand mosque with tall minarets against a breathtaking sunset sky, golden hour, cinematic lighting, highly detailed",
    "An open Holy Quran on a beautifully carved wooden rehal (book rest) inside a peaceful mosque, glowing warm light, hyper-realistic, 8k",
    "Stunning Islamic geometric patterns and Arabic calligraphy carved in white marble with glowing gold accents, close up, highly detailed, photorealistic",
    "A glowing traditional Ramadan lantern (fanoos) resting on a beautiful prayer rug in a dimly lit mosque, peaceful atmosphere, photorealistic"
]

secilen_komut = random.choice(cizim_fikirleri)
print(f"Yapay zekaya verilen komut: {secilen_komut}")

# Komutu URL'ye uygun hale getir
url_uyumlu_komut = urllib.parse.quote(secilen_komut)
rastgele_seed = random.randint(1, 1000000)

# Flux modeli ile yüksek kaliteli ve logosuz çizim URL'si
ai_cizim_url = f"https://image.pollinations.ai/prompt/{url_uyumlu_komut}?width=1080&height=1080&seed={rastgele_seed}&nologo=true&model=flux"

print("Yapay zeka bu muazzam manzarayı çiziyor, lütfen bekle...")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

try:
    response = requests.get(ai_cizim_url, headers=headers, timeout=60)
    
    if response.status_code == 200:
        os.makedirs('ai_kutsal_mekanlar', exist_ok=True)
        tarih = datetime.datetime.now().strftime('%Y-%m-%d')
        dosya_adi = f'ai_kutsal_mekanlar/{tarih}_ai_sanat.jpg'
        
        with open(dosya_adi, 'wb') as f:
            f.write(response.content)
        print(f"Harika! Kusursuz görsel çizildi ve '{dosya_adi}' olarak kaydedildi.")
    else:
        print(f"Hata: Görsel çizilemedi. Sunucu kodu: {response.status_code}")
except Exception as e:
    print(f"Sistemsel bir hata oluştu: {e}")
