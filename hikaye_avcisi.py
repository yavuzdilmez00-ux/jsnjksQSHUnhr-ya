import os
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime

ARAMA_TERIMLERI = [
    "yaşanmış dini hikayeler",
    "ibretlik kıssadan hisseler",
    "sahabelerden yaşanmış olaylar",
    "evliyaların hayatından ibretlik hikayeler",
    "gerçek islami hikayeler"
]

KATEGORILER = {
    "Sahabe ve Peygamberler": ["sahabe", "peygamber", "hz.", "ebubekir", "ömer", "ali", "osman"],
    "Evliyalar ve Alimler": ["evliya", "alim", "şeyh", "hoca", "mevlana", "şems", "yunus emre"],
    "Ahlak ve Erdem": ["dürüstlük", "yardımlaşma", "sadakat", "takva", "ihsan", "sabır"],
    "Diğer İbretlikler": []
}

HAFIZA_DOSYASI = "gecmis.txt"

def gecmisi_yukle():
    if not os.path.exists(HAFIZA_DOSYASI):
        return set()
    with open(HAFIZA_DOSYASI, "r", encoding="utf-8") as f:
        return set(f.read().splitlines())

def metin_cek(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        paragraflar = soup.find_all('p')
        metin = "\n\n".join([p.get_text().strip() for p in paragraflar if len(p.get_text()) > 80])
        
        if len(metin) > 400:
            return url, metin
    except Exception:
        pass
    return url, None

def kategori_bul(metin):
    metin_kucuk = metin.lower()
    for kategori, kelimeler in KATEGORILER.items():
        if any(kelime in metin_kucuk for kelime in kelimeler):
            return kategori
    return "Diğer İbretlikler"

def main():
    tarih = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    tarama_gecmisi = gecmisi_yukle()
    cekilecek_urller = set()

    print("Bağlantılar toplanıyor...")
    
    with DDGS() as ddgs:
        for terim in ARAMA_TERIMLERI:
            sonuclar = ddgs.text(terim, region='tr-tr', max_results=50)
            if sonuclar:
                for sonuc in sonuclar:
                    url = sonuc.get('href')
                    if url and url not in tarama_gecmisi:
                        cekilecek_urller.add(url)

    basarili_kayit = 0
    yeni_gecmis = list(tarama_gecmisi)

    with ThreadPoolExecutor(max_workers=20) as executor:
        gelecek_gorevler = {executor.submit(metin_cek, url): url for url in cekilecek_urller}
        
        for gorev in as_completed(gelecek_gorevler):
            url, metin = gorev.result()
            yeni_gecmis.append(url)
            
            if metin:
                kategori = kategori_bul(metin)
                klasor_adi = kategori.replace(" ", "_")
                os.makedirs(klasor_adi, exist_ok=True)
                
                dosya_yolu = f"{klasor_adi}/hikaye_{basarili_kayit}_{tarih}.md"
                icerik = f"# İbretlik Hikaye\n\n**Kategori:** {kategori}\n**Kaynak:** {url}\n\n## İçerik\n{metin}\n"
                
                with open(dosya_yolu, "w", encoding="utf-8") as f:
                    f.write(icerik)
                basarili_kayit += 1

    with open(HAFIZA_DOSYASI, "w", encoding="utf-8") as f:
        f.write("\n".join(yeni_gecmis))

    print(f"Toplam {basarili_kayit} yeni hikaye çekildi.")

if __name__ == "__main__":
    main()
