import os
import json
import time
import re
import concurrent.futures
from bs4 import BeautifulSoup
from curl_cffi import requests 

LETTERS = [
    'a', 'b', 'c', 'cc', 'd', 'e', 'f', 'g', 'h', 'i', 'ii', 'j', 'k', 
    'l', 'm', 'n', 'o', 'oo', 'p', 'r', 's', 'ss', 't', 'u', 'uu', 'v', 'y', 'z'
]

# Ortak başlık eşleştirme için temizleyici fonksiyon
def clean_title(title):
    t = title.lower()
    t = re.sub(r'ne anlama gelir\??', '', t)
    t = re.sub(r'ne demek\??', '', t)
    t = re.sub(r'neye yorumlanır\??', '', t)
    t = re.sub(r'neye işarettir\??', '', t)
    t = re.sub(r'nedir\??', '', t)
    t = re.sub(r'\(\s*.*?\s*\)', '', t)
    return t.strip()

# ==========================================
# 1. RUYATABIRLERI.COM İŞLEMLERİ
# ==========================================
def get_ruyatabirleri_links(letter, session):
    links = []
    page = 1
    base_url = "https://www.ruyatabirleri.com"
    
    while True:
        url = f"{base_url}/yorum/harf/{letter}" if page == 1 else f"{base_url}/yorum/harf/{letter}/page/{page}"
        try:
            response = session.get(url, timeout=20)
            if response.status_code != 200:
                break 
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.select('.singlebox-wrapper a')
            if not articles:
                articles = soup.select('.singlebox h2')
                if not articles:
                    break
                else:
                    articles = [h2.find_parent('a') for h2 in articles if h2.find_parent('a')]
            for a in articles:
                if a and a.get('href'):
                    links.append(a.get('href'))
            page += 1
        except:
            break
    return links

def scrape_ruyatabirleri(url, session):
    try:
        response = session.get(url, timeout=20)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.select_one('.entery')
        if not content_div:
            return None
            
        title_tag = content_div.select_one('h2')
        title = title_tag.get_text(strip=True) if title_tag else "Başlıksız"
        
        for selector in ['.ads', '.ads2', '.ads3', '.ads-bottom', '.socials', 'script', 'style', 'h2']:
            for el in content_div.select(selector):
                el.decompose()
                
        text_elements = content_div.find_all(['p', 'h3'])
        content_parts = [el.get_text(strip=True) for el in text_elements if el.get_text(strip=True)]
        
        if content_parts:
            return {"baslik": title, "icerik": "\n\n".join(content_parts)}
    except:
        pass
    return None

# ==========================================
# 2. MILLIYET PEMBENAR İŞLEMLERİ
# ==========================================
def get_milliyet_links(letter, session):
    links = []
    page = 1
    base_url = "https://www.milliyet.com.tr/pembenar/ruya-tabirleri/"
    
    # Milliyet arama parametresini büyük harf isteyebilir
    search_letter = letter.upper().replace('CC', 'Ç').replace('II', 'İ').replace('OO', 'Ö').replace('SS', 'Ş').replace('UU', 'Ü')
    
    while True:
        url = f"{base_url}?search={search_letter}&page={page}"
        try:
            response = session.get(url, timeout=20)
            if response.status_code != 200:
                break
                
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.select('.dream-results__item')
            
            if not items:
                break
                
            for item in items:
                href = item.get('href')
                if href:
                    if href.startswith('/'):
                        href = "https://www.milliyet.com.tr" + href
                    links.append(href)
            
            # Sayfalama butonu yoksa son sayfadayız demektir
            if not soup.select_one('.dream-dictionary__load-more-area'):
                break
                
            page += 1
        except:
            break
    return links

def scrape_milliyet(url, session):
    try:
        response = session.get(url, timeout=20)
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.select_one('.dream-detail__title')
        content_div = soup.select_one('.dream-detail__text')
        
        if not content_div or not title_tag:
            return None
            
        title = title_tag.get_text(strip=True)
        
        text_elements = content_div.find_all(['p', 'h2', 'h3'])
        content_parts = [el.get_text(strip=True) for el in text_elements if el.get_text(strip=True)]
        
        if content_parts:
            return {"baslik": title, "icerik": "\n\n".join(content_parts)}
    except:
        pass
    return None

# ==========================================
# ANA ÇALIŞTIRMA MANTIĞI
# ==========================================
def main():
    if not os.path.exists('veri'):
        os.makedirs('veri')

    all_merged_data = {}
    session = requests.Session(impersonate="chrome120")

    for letter in LETTERS:
        print(f"'{letter}' harfi için linkler toplanıyor...")
        
        ruya_links = get_ruyatabirleri_links(letter, session)
        milliyet_links = get_milliyet_links(letter, session)
        
        print(f"Ruyatabirleri: {len(ruya_links)} link | Milliyet: {len(milliyet_links)} link bulundu.")
        
        letter_merged = {}
        
        # 1. Ruyatabirleri verilerini çek
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            ruya_results = list(executor.map(lambda url: scrape_ruyatabirleri(url, session), set(ruya_links)))
            
        # 2. Milliyet verilerini çek
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            milliyet_results = list(executor.map(lambda url: scrape_milliyet(url, session), set(milliyet_links)))

        # BİRLEŞTİRME VE KAYNAK GİZLEME İŞLEMİ
        for res in filter(None, ruya_results + milliyet_results):
            c_title = clean_title(res['baslik'])
            
            if c_title in letter_merged:
                # Daha önce bu başlık varsa içeriği altına ekle
                letter_merged[c_title]['icerik'] += f"\n\n---\n\n{res['icerik']}"
            else:
                # İlk defa geliyorsa temiz başlığıyla oluştur (URL kaydetmiyoruz!)
                letter_merged[c_title] = {
                    "baslik": res['baslik'].replace(" Ne Anlama Gelir?", "").replace(" Ne Demek?", ""), 
                    "icerik": res['icerik']
                }
                
        # Harfe özel JSON dosyasını kaydet (sadece değerleri listeye çevirip kaydediyoruz)
        final_letter_list = list(letter_merged.values())
        
        file_path = os.path.join('veri', f"{letter}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(final_letter_list, f, ensure_ascii=False, indent=4)
            
        # Genel listeye ekle
        all_merged_data.update(letter_merged)
        print(f"'{letter}' harfi tamamlandı. ({len(final_letter_list)} birleştirilmiş kayıt)")

    # Tüm verileri tek bir JSON dosyasında kaydet
    final_all_list = list(all_merged_data.values())
    all_file_path = os.path.join('veri', "tumu.json")
    with open(all_file_path, 'w', encoding='utf-8') as f:
        json.dump(final_all_list, f, ensure_ascii=False, indent=4)
        
    print(f"Tüm işlemler tamamlandı! Toplam {len(final_all_list)} benzersiz kayıt çekildi ve kaynaklar gizlendi.")

if __name__ == "__main__":
    main()
