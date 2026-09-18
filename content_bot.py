import json
import re
import g4f

kulliyat_icerikleri = {
    "peygamberler_tarihi": ["Hz. Adem", "Hz. Nuh"], 
    "ashabi_kiram": ["Hz. Ebubekir", "Hz. Ömer"],
    "islam_alimleri": ["İmam Rabbani", "İmam Gazali"]
}

nihai_json = []

def json_temizle(metin):
    try:
        match = re.search(r'\{.*\}', metin, re.DOTALL)
        if match:
            return match.group(0)
        return metin.strip()
    except Exception:
        return metin

for kategori, isimler in kulliyat_icerikleri.items():
    kategori_verisi = {"kategori_id": kategori, "kisiler": []}
    
    for isim in isimler:
        prompt = f"""
        {isim} isimli kişinin hayatını sadece JSON formatında yaz. Başka hiçbir kelime kullanma:
        {{
            "isim": "{isim}",
            "kisa_bilgi": "Kısa bir özet",
            "detayli_hayat_hikayesi": "Detaylı biyografi...",
            "onemli_olaylar": ["Olay 1", "Olay 2"]
        }}
        """
        
        yanit = ""
        try:
            # GitHub sunucularını engellemeyen PollinationsAI sağlayıcısını kullanmaya zorluyoruz
            yanit = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4o,
                provider=g4f.Provider.PollinationsAI,
                messages=[{"role": "user", "content": prompt}]
            )
            
            temiz_json = json_temizle(yanit)
            kisi_json = json.loads(temiz_json)
            kategori_verisi["kisiler"].append(kisi_json)
            
        except Exception as e:
            # EĞER SİSTEM YİNE ENGELLENİRSE, DOSYAYI BOŞ BIRAKMAK YERİNE HATAYI JSON'A EKLİYORUZ
            kategori_verisi["kisiler"].append({
                "isim": isim,
                "durum": "HATA",
                "hata_detayi": str(e),
                "gelen_yanit": yanit[:200] if yanit else "Hiç yanıt alınamadı, bağlantı koptu."
            })
            
    nihai_json.append(kategori_verisi)

with open("kulliyat.json", "w", encoding="utf-8") as f:
    json.dump(nihai_json, f, ensure_ascii=False, indent=4)
