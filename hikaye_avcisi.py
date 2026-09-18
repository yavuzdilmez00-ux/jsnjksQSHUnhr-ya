import os
import re
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
from concurrent.futures import ThreadPoolExecutor, as_completed
from langdetect import detect, LangDetectException # Dil dedektifi eklendi

ARAMA_TERIMLERI = [
    "yaşanmış dini hikayeler kıssadan hisse",
    "sahabelerden yaşanmış ibretlik olaylar",
    "evliyaların hayatından hikmetli kıssalar",
    "gerçek yaşanmış islami hikayeler"
]

KATEGORILER = {
    "Sahabe_ve_Peygamberler": ["sahabe", "peygamber", "hz.", "ebubekir", "ömer", "ali", "osman", "amr bin vud"],
    "Evliyalar_ve_Alimler": ["evliya", "alim", "şeyh", "hoca", "mevlana", "şems", "yunus emre", "hüdayi"],
    "Ahlak_ve_Erdem": ["dürüstlük", "ihsan", "ihlas", "tevazu", "takva", "nefis", "sabır"],
    "Diger_Ibretlikler": []
}

HAFIZA_DOSYASI = "gecmis.txt"

def gecmisi_yukle():
    if not os.path.exists(HAFIZA_DOSYASI):
        return set()
    with open(HAFIZA_DOSYASI, "r", encoding="utf-8") as f:
        return set(f.read().splitlines())

def dosya_adi_temizle(baslik):
    temiz = re.sub(r'[\\/*?:"<>|]', "", baslik)
    temiz = temiz.strip().replace(" ", "_")
    return temiz[:50]

def metin_ve_detay_cek(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8' 
        soup = BeautifulSoup(response.text, 'html.parser')
        
        h1 = soup.find('h1')
        baslik = h1.get_text().strip() if h1 else (soup.title.get_text().strip() if soup.title else "Hikmetli Kıssa")
        baslik = re.split(r'[-–|]', baslik)[0].strip()
        
        paragraflar = [p.get_text().strip() for p in soup.find_all('p') if len(p.get_text().strip()) > 50]
        if not paragraflar or len(" ".join(paragraflar)) < 300:
            return url, None, None, None

        hikaye_metni = "\n\n".join(paragraflar)

        # KESİN TÜRKÇE FİLTRESİ
        try:
            if detect(hikaye_metni) != 'tr':
                return url, None, None, None # Türkçe değilse direkt atla
        except LangDetectException:
            return url, None, None, None # Dili algılayamazsa atla

        hisse = None
        kalan_paragraflar = []
        
        for p in paragraflar:
            eslesme = re.search(r'(kıssadan hisse|hisse|ibret|öğüt)\s*[:\-]\s*(.*)', p, re.IGNORECASE)
            if eslesme and not hisse:
                hisse = eslesme.group(2).strip() or p
            else:
                kalan_paragraflar.append(p)
                
        if not hisse and kalan_paragraflar:
            son_paragraf = kalan_paragraflar[-1]
            if len(son_paragraf) < 250: 
                hisse = kalan_paragraflar.pop()
            else:
                hisse = "Her işte Allah'ın rızasını gözetmek ve samimiyetle amel etmektir."

        son_metin = "\n\n".join(kalan_paragraflar)
        return url, baslik, son_metin, hisse
    except Exception:
        pass
    return url, None, None, None

def kategori_bul(metin, baslik):
    birlesik = f"{baslik} {metin}".lower()
    for kategori, kelimeler in KATEGORILER.items():
        if any(kelime in birlesik for kelime in kelimeler):
            return kategori
    return "Diger_Ibretlikler"

def main():
    tarama_gecmisi = gecmisi_yukle()
    cekilecek_urller = set()

    print("İnternetten yeni kıssalar aranıyor...")
    with DDGS() as ddgs:
        for terim in ARAMA_TERIMLERI:
            sonuclar = ddgs.text(terim, region='tr-tr', max_results=30)
            if sonuclar:
                for sonuc in sonuclar:
                    url = sonuc.get('href')
                    if url and url not in tarama_gecmisi:
                        cekilecek_urller.add(url)

    basarili_kayit = 0
    yeni_gecmis = list(tarama_gecmisi)

    with ThreadPoolExecutor(max_workers=10) as executor:
        gelecek_gorevler = {executor.submit(metin_ve_detay_cek, url): url for url in cekilecek_urller}
        
        for gorev in as_completed(gelecek_gorevler):
            url, baslik, hikaye_metni, hisse = gorev.result()
            yeni_gecmis.append(url)
            
            if hikaye_metni and baslik:
                kategori = kategori_bul(hikaye_metni, baslik)
                os.makedirs(kategori, exist_ok=True)
                
                temiz_baslik = dosya_adi_temizle(baslik)
                dosya_yolu = f"{kategori}/{temiz_baslik}.md"
                
                icerik = f"""# {baslik}

{hikaye_metni}

<br>

> ❝ **Kıssadan Hisse:** {hisse} ❞

---
*Kaynak: {url}*
"""
                with open(dosya_yolu, "w", encoding="utf-8") as f:
                    f.write(icerik)
                basarili_kayit += 1

    with open(HAFIZA_DOSYASI, "w", encoding="utf-8") as f:
        f.write("\n".join(yeni_gecmis))

    print(f"Toplam {basarili_kayit} yeni Türkçe hikaye başarıyla eklendi.")

if __name__ == "__main__":
    main()
