import json
import re
from duckduckgo_search import DDGS

kulliyat_icerikleri = {
    "peygamberler_tarihi": ["Hz. Adem", "Hz. Nuh"], 
    "ashabi_kiram": ["Hz. Ebubekir", "Hz. Ömer"],
    "islam_alimleri": ["İmam Rabbani", "İmam Gazali"]
}

nihai_json = []

def json_temizle(metin):
    # Metnin içindeki { ve } işaretleri arasındaki JSON kısmını zorla çeker
    match = re.search(r'\{.*\}', metin, re.DOTALL)
    if match:
        return match.group(0)
    return metin.strip()

print("Sistem başlatılıyor...")

try:
    with DDGS() as ddgs:
        for kategori, isimler in kulliyat_icerikleri.items():
            kategori_verisi = {"kategori_id": kategori, "kisiler": []}
            
            for isim in isimler:
                print(f"\n--- {isim} için içerik isteniyor ---")
                
                prompt = f"""
                {isim} isimli kişinin hayatını sadece geçerli bir JSON formatında yaz. 
                Başka hiçbir açıklama, selamlama veya markdown kullanma. Sadece şu yapıyı ver:
                {{
                    "isim": "{isim}",
                    "kisa_bilgi": "Kısa bir özet",
                    "detayli_hayat_hikayesi": "Detaylı biyografi...",
                    "onemli_olaylar": ["Olay 1", "Olay 2"]
                }}
                """
                
                try:
                    # AI'dan yanıt al
                    yanit = ddgs.chat(prompt, model="gpt-4o-mini") 
                    print(f"Ham Yanıt: {yanit[:150]}...") # Yanıtın ilk kısmını GitHub loglarına yazdırır
                    
                    # JSON'ı temizle ve dönüştür
                    temiz_json = json_temizle(yanit)
                    kisi_json = json.loads(temiz_json)
                    kategori_verisi["kisiler"].append(kisi_json)
                    
                    print(f"BAŞARILI: {isim} eklendi.")
                    
                except json.JSONDecodeError as e:
                    print(f"HATA: {isim} için JSON çevirme başarısız. Hata: {e}")
                    print(f"Gelen Tam Metin: {yanit if 'yanit' in locals() else 'Yok'}")
                except Exception as e:
                    print(f"HATA: {isim} işlenirken bir sorun oluştu: {e}")
                    
            nihai_json.append(kategori_verisi)

except Exception as e:
    print(f"KRİTİK HATA: DuckDuckGo bağlantısı koptu veya engellendi: {e}")

# JSON dosyasına yazdır
with open("kulliyat.json", "w", encoding="utf-8") as f:
    json.dump(nihai_json, f, ensure_ascii=False, indent=4)

print("\nİşlem tamamlandı, kulliyat.json dosyası oluşturuldu.")
