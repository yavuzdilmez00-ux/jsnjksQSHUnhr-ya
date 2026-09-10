import json
import random
import os

print("Test için 10 adetlik JSON verisi oluşturuluyor...")

# --- CUMA MESAJI HAVUZU ---
girisler = [
    "Gönüllerin huzur bulduğu bu mübarek günde,",
    "Haftanın en nurlu sabahına kavuştuk,",
    "Kalplerimizin imanla dolduğu bu bereketli vakitte,"
]
dualar = [
    "Rabbim gönlünüzden geçen duaları hakkınızda hayırlı eylesin.",
    "Allah kazancınıza bereket, ömrünüze afiyet ihsan eylesin.",
    "Mevlam bizleri doğru yoldan, Kur'an'ın nurundan ayırmasın."
]
kapanislar = [
    "Hayırlı Cumalar dilerim.",
    "Cumanız mübarek olsun.",
    "Selam ve dua ile kalın."
]

uretilen_mesajlar = set()
cuma_json_listesi = []

# Sadece 10 adet üret
while len(uretilen_mesajlar) < 10:
    mesaj = f"{random.choice(girisler)} {random.choice(dualar)} {random.choice(kapanislar)}"
    if mesaj not in uretilen_mesajlar:
        uretilen_mesajlar.add(mesaj)
        cuma_json_listesi.append({
            "id": len(uretilen_mesajlar),
            "mesaj": mesaj,
            "kategori": "Cuma Mesajı"
        })

# --- HİKAYE HAVUZU (Sadece 10 adet) ---
sahabeler = ["Hz. Ali (r.a)", "Hz. Ömer (r.a)", "Hz. Ebubekir (r.a)", "Hz. Osman (r.a)"]
konular = ["adalet", "cömertlik", "tevazu", "cesaret"]
ogutler = ["hakkı gözetmemiz gerektiğini", "yardımlaşmanın önemini", "alçakgönüllü olmayı"]

hikaye_json_listesi = []
for i in range(1, 11): 
    metin = f"Bir gün {random.choice(sahabeler)}, {random.choice(konular)} konusunda büyük bir örnek oldu. Olayın sonunda herkes {random.choice(ogutler)} anladı."
    hikaye_json_listesi.append({
        "id": i,
        "baslik": f"Örnek Olay {i}",
        "icerik": metin,
        "kategori": "Kısa Hikayeler"
    })

# --- JSON OLARAK KAYDET ---
uygulama_veritabani = {
    "test_surumu": True,
    "toplam_cuma_mesaji": len(cuma_json_listesi),
    "toplam_hikaye": len(hikaye_json_listesi),
    "cuma_mesajlari": cuma_json_listesi,
    "hikayeler": hikaye_json_listesi
}

# Klasörü oluştur ve kaydet
os.makedirs('android_api', exist_ok=True)
dosya_yolu = 'android_api/ornek_veri.json'

with open(dosya_yolu, 'w', encoding='utf-8') as f:
    json.dump(uygulama_veritabani, f, ensure_ascii=False, indent=4)

print(f"✅ Test tamamlandı! {dosya_yolu} dosyası başarıyla oluşturuldu.")
