import os
import json
import time
import concurrent.futures
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# Site üzerindeki harf URL yapıları (Ç->cc, Ş->ss vb.)
LETTERS = [
    'a', 'b', 'c', 'cc', 'd', 'e', 'f', 'g', 'h', 'i', 'ii', 'j', 'k', 
    'l', 'm', 'n', 'o', 'oo', 'p', 'r', 's', 'ss', 't', 'u', 'uu', 'v', 'y', 'z'
]

BASE_URL = "https://www.ruyatabirleri.com"

def get_article_links(letter):
    """Bir harfe ait tüm sayfalardaki rüya linklerini toplar."""
    links = []
    page_num = 1
    
    # Arka planda gerçek bir Chrome başlatıyoruz
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        while True:
            if page_num == 1:
                url = f"{BASE_URL}/yorum/harf/{letter}"
            else:
                url = f"{BASE_URL}/yorum/harf/{letter}/page/{page_num}"
                
            try:
                # Sayfaya gidip DOM'un yüklenmesini bekliyoruz
                page.goto(url, timeout=45000)
                
                # Cloudflare'in "Just a moment" testini geçmesi ve JavaScript'in çalışması için 5 saniye süre tanıyoruz
                time.sleep(5)
                
                # Test geçildikten sonra oluşan GÜNCEL saf HTML'i alıyoruz
                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')
                
                if soup.title and ("Just a moment" in soup.title.text or "Cloudflare" in soup.title.text):
                    print(f"UYARI: Playwright bile güvenlik duvarına takıldı: {url}")
                    break

                articles = soup.select('.singlebox-wrapper a')
                
                # Eskisi gibi hiçbir şeyi silmeden alternatif seçici mantığı devam ediyor
                if not articles:
                    articles = soup.select('.singlebox h2')
                    if not articles:
                        print(f"BİLGİ: '{letter}' harfi {page_num}. sayfada içerik bitti veya bulunamadı.")
                        break
                    else:
                        articles = [h2.find_parent('a') for h2 in articles if h2.find_parent('a')]
                    
                for a in articles:
                    if a:
                        href = a.get('href')
                        if href:
                            if href.startswith('/'):
                                href = BASE_URL + href
                            elif not href.startswith('http'):
                                continue
                            links.append(href)
                
                page_num += 1
            except Exception as e:
                print(f"SİSTEM HATASI ({letter} - Sayfa {page_num}): {e}")
                break
                
        browser.close()
        
    return links

def scrape_article(url):
    """Tek bir rüya tabiri sayfasından başlık ve içeriği çeker."""
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            page.goto(url, timeout=45000)
            # Sayfa içeriğinin tam oturması için kısa bekleme
            time.sleep(2) 
            
            html = page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            content_div = soup.select_one('.entery')
            
            if not content_div:
                browser.close()
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
            
            browser.close()
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
        
        # Gerçek Chrome tarayıcılar arka planda RAM tüketeceği için aynı anda açılacak tarayıcı sınırını (worker) 3'e ayarladık
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
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
