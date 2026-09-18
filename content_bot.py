import json
import re
from duckduckgo_search import DDGS

# Uygulamadaki kategorilerine uygun veri yapısı
kulliyat_icerikleri = {
    "peygamberler_tarihi": ["Hz. Adem", "Hz. Nuh"], 
    "ashabi_kiram": ["Hz. Ebubekir", "Hz. Ömer"],
    "islam_alimleri": ["İmam Rabbani", "İmam Gazali"]
}

nihai_json = []

def json_temizle(metin):
    # Yapay zeka bazen ```json ... ``` tagları arasında yanıt verebilir, bunu temizliyoruz.
    metin = re.sub(r"```json", "", metin)
    metin = re.sub(r"```", "", metin)
    return metin.strip()

# DuckDuckGo'nun ücretsiz yapay zeka chat servisini başlatıyoruz
with DDGS() as ddgs:
    for kategori, isimler in kulliyat_icerikleri.items():
        kategori_verisi = {"kategori_id": kategori, "kisiler": []}
        
        for isim in isimler:
            print(f"{isim} için içerik üretiliyor...")
            
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
                # API key olmadan tamamen ücretsiz sorgu atıyoruz
                yanit = ddgs.chat(prompt, model="gpt-4o-mini") 
                temiz_json = json_temizle(yanit)
                
                kisi_json = json.loads(temiz_json)
                kategori_verisi["kisiler"].append(kisi_json)
            except Exception as e:
                print(f"Hata oluştu ({isim}): {e}")
                
        nihai_json.append(kategori_verisi)

with open("kulliyat.json", "w", encoding="utf-8") as f:
    json.dump(nihai_json, f, ensure_ascii=False, indent=4)

print("kulliyat.json dosyası bedava sistemle başarıyla oluşturuldu!")
