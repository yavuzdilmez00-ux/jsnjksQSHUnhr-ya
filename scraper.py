import os
import json
import concurrent.futures
from bs4 import BeautifulSoup
import cloudscraper

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
    
    # GitHub Actions IP'lerini engelleyen güvenlik duvarlarını (Cloudflare vb.) aşmak için cloudscraper
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    
    while True:
        if page == 1:
            url = f"{BASE_URL}/yorum/harf/{letter}"
        else:
            url = f"{BASE_URL}/yorum/harf/{letter}/page/{page}"
            
        try:
            response = scraper.get(url, timeout=20)
            
            # DEBUG 1: HTTP Durum Kodunu kontrol edelim
            if response.status_code != 200:
                if response.status_code != 404:
                    print(f"HATA: Durum Kodu ({letter} - Sayfa {page}): {response.status_code}")
                    print(f"HATA DETAYI: {response.text[:300]}") # Sitenin verdiği hatanın ilk 300 karakteri
                break 
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Sayfanın başlığını kontrol ederek doğrulama (captcha/challenge) sayfasına düşüp düşmediğimizi görelim
            if soup.title and ("Just a moment" in soup.title.text or "Cloudflare" in soup.title.text or "Attention Required" in soup.title.text):
                print(f"UYARI: Bot korumasına takıldı (Cloudflare): {url}")
                break

            articles = soup.select('.singlebox-wrapper a')
            
            # Ana seçici çalışmazsa, hiçbir şeyi silmeden alternatif bir HTML arama yöntemi uyguluyoruz
            if not articles:
                articles = soup.select('.singlebox h2')
                if not articles:
                    # DEBUG 2: Etiketler yoksa site bize ne döndürdü? İlk 500 karakteri ekrana yazdırıyoruz.
                    print(f"DEBUG: '{letter}' harfi {page}. sayfada içerik etiketi bulunamadı!")
                    print(f"SİTENİN DÖNDÜRDÜĞÜ HTML (İlk 500 Karakter):\n{response.text[:500]}\n{'-'*50}")
                    break
                else:
                    # Sadece h2 bulunduysa bir üstündeki a etiketini (linki) yakala
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
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})
    try:
        response = scraper.get(url, timeout=20)
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
        
        # İstek limiti (Rate limit) yememek için eşzamanlı işlemi biraz düşürüyoruz (10'dan 5'e)
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
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
