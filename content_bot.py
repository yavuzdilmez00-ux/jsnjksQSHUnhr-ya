import json
import re
import g4f
from g4f.client import Client

kulliyat_icerikleri = {
    "peygamberler_tarihi": ["Hz. Adem", "Hz. Nuh"], 
    "ashabi_kiram": ["Hz. Ebubekir", "Hz. Ömer"],
    "islam_alimleri": ["İmam Rabbani", "İmam Gazali"]
}

nihai_json = []

def json_temizle(metin):
    try:
        # Sadece { } işaretleri arasındaki JSON verisini bulur
        match = re.search(r'\{.*\}', metin, re.DOTALL)
        if match:
            return match.group(0)
        return metin.strip()
    except Exception:
        return metin

print("GPT4Free (g4f) ile sistem başlatılıyor...")
client = Client()

for kategori, isimler in kulliyat_icerikleri.items():
    kategori_verisi = {"kategori_id": kategori, "kisiler": []}
    
    for isim in isimler:
        print(f"\n--- {isim} için içerik isteniyor ---")
        
        prompt = f"""
        {isim} isimli kişinin hayatını sadece geçerli bir JSON formatında yaz. 
        Hiçbir markdown kodu (```json vb.), selamlama veya ekstra açıklama kullanma. Sadece şu yapıyı ver:
        {{
            "isim": "{isim}",
            "kisa_bilgi": "Kısa bir özet",
            "detayli_hayat_hikayesi": "Detaylı biyografi...",
            "onemli_olaylar": ["Olay 1", "Olay 2"]
        }}
        """
        
        try:
            # g4f otomatik olarak çalışan ücretsiz bir sağlayıcı bulup yanıt alır
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                timeout=120 # Yanıt gecikmesine karşı süre tanıdık
            )
            yanit = response.choices[0].message.content
            print(f"Ham Yanıt: {yanit[:100]}...") 
            
            temiz_json = json_temizle(yanit)
            kisi_json = json.loads(temiz_json)
            kategori_verisi["kisiler"].append(kisi_json)
            print(f"BAŞARILI: {isim} sisteme eklendi.")
            
        except json.JSONDecodeError as e:
            print(f"HATA (JSON Çevirme): {isim} için veri bozuk geldi. Metin: {yanit[:50]}...")
        except Exception as e:
            print(f"HATA (Bağlantı): {isim} işlenemedi. Sorun: {e}")
            
    nihai_json.append(kategori_verisi)

with open("kulliyat.json", "w", encoding="utf-8") as f:
    json.dump(nihai_json, f, ensure_ascii=False, indent=4)

print("\nİşlem tamamlandı, kulliyat.json dosyası yazıldı.")
