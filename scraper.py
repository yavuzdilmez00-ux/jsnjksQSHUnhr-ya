import os
import json
import concurrent.futures
from bs4 import BeautifulSoup
from curl_cffi import requests 

# Site üzerindeki harf URL yapıları (Ç->cc, Ş->ss vb.)
LETTERS = [
    'a', 'b', 'c', 'cc', 'd', 'e', 'f', 'g', 'h', 'i', 'ii', 'j', 'k', 
    'l', 'm', 'n', 'o', 'oo', 'p', 'r', 's', 'ss', 't', 'u', 'uu', 'v', 'y', 'z'
]

BASE_URL = "https://www.ruyatabirleri.com"

def get_article_links(letter):
    """Bir harfe ait tüm sayfalardaki rüya linklerini toplar."""
    links = []
    page = 1
    
    # Chrome 120 TLS parmak izini taklit ederek Cloudflare'i aşıyoruz
    session = requests.Session(impersonate="chrome120")
    
    while True:
        if page == 1:
            url = f"{BASE_URL}/yorum/harf/{letter}"
        else:
            url = f"{BASE_URL}/yorum/harf/{letter}/page/{page}"
            
        try:
            response = session.get(url, timeout=30)
            
            # HİÇBİR ŞEYİ SİLMEDEN EKLENEN KISIM: 403 veya CF engeli gelirse Proxy üzerinden tekrar dene
            if response.status_code == 403 or (response.status_code == 200 and "Just a moment" in response.text):
                proxy_url = f"https://api.allorigins.win/raw?url={url}"
                response = session.get(proxy_url, timeout=30)

            if response.status_code != 200:
                if response.status_code != 404:
                    print(f"HATA: Durum Kodu ({letter} - Sayfa {page}): {response.status_code}")
                break 
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            if soup.title and ("Just a moment" in soup.title.text or "Cloudflare" in soup.title.text):
                print(f"UYARI: Bot korumasına takıldı (Cloudflare): {url}")
                break

            articles = soup.select('.singlebox-wrapper a')
            
            if not articles:
                articles = soup.select('.singlebox h2')
                if not articles:
                    print(f"BİLGİ: '{letter}' harfi {page}. sayfada içerik bitti veya bulunamadı.")
                    break
                else:
                    articles = [h2.find_parent('a') for h2 in articles if h2.find_parent('a')]
                
            for a in articles:
                if a:
                    href = a.get('href')
                    if href:
                        links.append(href)
            
            page += 1
        except Exception as e:
            print(f"SİSTEM HATASI ({letter} - Sayfa {page}): {e}")
            break
            
    return links

def scrape_article(url):
    """Tek bir rüya tabiri sayfasından başlık ve içeriği çeker."""
    session = requests.Session(impersonate="chrome120")
    try:
        response = session.get(url, timeout=30)
        
        # HİÇBİR ŞEYİ SİLMEDEN EKLENEN KISIM: İçerik çekerken CF engeli gelirse Proxy üzerinden tekrar dene
        if response.status_code == 403 or (response.status_code == 200 and "Just a moment" in response.text):
            proxy_url = f"https://api.allorigins.win/raw?url={url}"
            response = session.get(proxy_url, timeout=30)

        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.select_one('.entery')
        
        if not content_div:
            return None
            
        title_tag = content_div.select_one('h2')
        title = title_tag.get_text(strip=True) if title_tag else "Başlıksız"
        
        unwanted_selectors = ['.ads', '.ads2', '.ads3', '.ads-bottom', '.socials', 'script', 'style', 'h2']
        for selector in unwanted_selectors:
            for el in content_div.select(selector):
                el.decompose()
                
        text_elements = content_div.find_all(['p', 'h3'])
        content_parts = []
        for el in text_elements:
            text = el.get_text(strip=True)
            if text:
                content_parts.append(text)
                
        full_content = "\n\n".join(content_parts)
        
        return {
            "baslik": title,
            "icerik": full_content,
            "url": url
        }
    except Exception as e:
        print(f"İçerik çekilemedi: {url} - Hata: {e}")
        return None

def main():
    if not os.path.exists('veri'):
        os.makedirs('veri')

    all_data = []

    for letter in LETTERS:
        print(f"'{letter}' harfi için linkler toplanıyor...")
        links = get_article_links(letter)
        print(f"'{letter}' harfi için {len(links)} adet link bulundu. İçerikler çekiliyor...")
        
        letter_data = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(scrape_article, set(links)))
            
        for res in results:
            if res:
                letter_data.append(res)
                all_data.append(res)
                
        file_path = os.path.join('veri', f"{letter}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(letter_data, f, ensure_ascii=False, indent=4)
            
        print(f"'{letter}' harfi tamamlandı. ({len(letter_data)} kayıt)")

    all_file_path = os.path.join('veri', "tumu.json")
    with open(all_file_path, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)
        
    print(f"Tüm işlemler tamamlandı! Toplam {len(all_data)} kayıt çekildi.")

if __name__ == "__main__":
    main()
