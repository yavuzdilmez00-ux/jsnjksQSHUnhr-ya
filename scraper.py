import os
import json
import requests
from bs4 import BeautifulSoup
import concurrent.futures

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
    session = requests.Session()
    
    while True:
        if page == 1:
            url = f"{BASE_URL}/yorum/harf/{letter}"
        else:
            url = f"{BASE_URL}/yorum/harf/{letter}/page/{page}"
            
        try:
            response = session.get(url, timeout=10)
            if response.status_code != 200:
                break # Sayfa bitti veya bulunamadı
                
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.select('.singlebox-wrapper a')
            
            if not articles:
                break
                
            for a in articles:
                href = a.get('href')
                if href:
                    links.append(href)
            
            page += 1
        except Exception as e:
            print(f"Hata ({letter} - Sayfa {page}): {e}")
            break
            
    return links

def scrape_article(url):
    """Tek bir rüya tabiri sayfasından başlık ve içeriği çeker."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.select_one('.entery')
        
        if not content_div:
            return None
            
        # Başlığı al
        title_tag = content_div.select_one('h2')
        title = title_tag.get_text(strip=True) if title_tag else "Başlıksız"
        
        # Gereksiz kısımları DOM'dan temizle (Reklamlar, yorumlar, sosyal medya vs.)
        unwanted_selectors = ['.ads', '.ads2', '.ads3', '.ads-bottom', '.socials', 'script', 'style', 'h2']
        for selector in unwanted_selectors:
            for el in content_div.select(selector):
                el.decompose()
                
        # Sadece paragrafları ve alt başlıkları (h3) al
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
        
        # Hızlı çekim için ThreadPool kullanıyoruz
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(scrape_article, set(links)))
            
        for res in results:
            if res:
                letter_data.append(res)
                all_data.append(res)
                
        # Harfe özel JSON dosyasını kaydet
        file_path = os.path.join('veri', f"{letter}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(letter_data, f, ensure_ascii=False, indent=4)
            
        print(f"'{letter}' harfi tamamlandı. ({len(letter_data)} kayıt)")

    # Tüm verileri tek bir JSON dosyasında kaydet
    all_file_path = os.path.join('veri', "tumu.json")
    with open(all_file_path, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)
        
    print(f"Tüm işlemler tamamlandı! Toplam {len(all_data)} kayıt çekildi.")

if __name__ == "__main__":
    main()
