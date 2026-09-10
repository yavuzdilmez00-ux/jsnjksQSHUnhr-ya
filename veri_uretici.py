import json
import random
import os

print("Android uygulaması için dev JSON veri tabanı oluşturuluyor...")

# --- 1. CUMA MESAJI MATRİSİ (Milyonlarca kombinasyon için listeleri uzatabilirsin) ---
giris_cumleleri = [
    "Gönüllerin huzur bulduğu bu mübarek günde,",
    "Rabbimizin rahmet kapılarını sonuna kadar açtığı Cuma gününde,",
    "Haftanın en nurlu sabahına kavuştuk,",
    "İslam aleminin bayramı olan bu güzel günde,",
    "Kalplerimizin imanla dolduğu bu bereketli vakitte,"
]

dua_cumleleri = [
    "Rabbim gönlünüzden geçen duaları hakkınızda hayırlı eylesin.",
    "Allah kazancınıza bereket, ömrünüze afiyet ihsan eylesin.",
    "Mevlam bizleri doğru yoldan, Kur'an'ın nurundan ayırmasın.",
    "Rabbim hanenize huzur, bedeninize şifa versin.",
    "Allah sevdiklerinizi size bağışlasın, dertlerinize deva göndersin."
]

kapanis_cumleleri = [
    "Hayırlı Cumalar dilerim.",
    "Cumanız mübarek olsun.",
    "Selam ve dua ile kalın.",
    "Gününüz aydın, Cumanız bereketli olsun.",
    "Rabbime emanet olun, hayırlı Cumalar."
]

# Uygulaman için 10.000 adet benzersiz mesaj üretelim (sınırı sen belirle)
URETILECEK_CUMA_MESAJI_SAYISI = 10000
uretilen_mesajlar = set()
cuma_json_listesi = []

while len(uretilen_mesajlar) < URETILECEK_CUMA_MESAJI_SAYISI:
    # Cümleleri rastgele seçip birleştiriyoruz
    mesaj = f"{random.choice(giris_cumleleri)} {random.choice(dua_cumleleri)} {random.choice(kapanis_cumleleri)}"
    
    # Set (küme) kullandığımız için aynı mesaj 2 kez eklenemez, hepsi benzersiz olur!
    if mesaj not in uretilen_mesajlar:
        uretilen_mesajlar.add(mesaj)
        cuma_json_listesi.append({
            "id": len(uretilen_mesajlar),
            "mesaj": mesaj,
            "kategori": "Cuma Mesajı"
        })

print(f"✅ {len(cuma_json_listesi)} adet benzersiz Cuma Mesajı üretildi.")

# --- 2. HİKAYELER İÇİN ŞABLON YAKLAŞIMI ---
# Hikayeler karmaşık olduğu için "Boşluk Doldurma" (Mad Libs) mantığı kullanıyoruz.
sahabeler = ["Hz. Ali (r.a)", "Hz. Ömer (r.a)", "Hz. Ebubekir (r.a)", "Hz. Osman (r.a)"]
konular = ["adalet", "cömertlik", "tevazu", "cesaret"]
ogutler = ["kimsenin hakkını yemememiz gerektiğini", "Allah için vermenin bereketini", "gururdan uzak durmayı"]

hikaye_json_listesi = []
for i in range(1, 51): # Uygulama için şimdilik 50 hikaye örneği
    secilen_sahabe = random.choice(sahabeler)
    secilen_konu = random.choice(konular)
    secilen_ogut = random.choice(ogutler)
    
    metin = f"Bir gün {secilen_sahabe}, {secilen_konu} konusunda çevresindekilere büyük bir örnek oldu. Olayın sonunda herkes {secilen_ogut} bir kez daha anladı. Bu eşsiz olay, İslam tarihine altın harflerle geçti."
    
    hikaye_json_listesi.append({
        "id": i,
        "baslik": f"{secilen_sahabe} ve {secilen_konu.capitalize()}",
        "icerik": metin,
        "kategori": "İbretlik Hikayeler"
    })

print(f"✅ {len(hikaye_json_listesi)} adet Hikaye şablonu üretildi.")

# --- 3. JSON OLARAK BİRLEŞTİR VE KAYDET ---
# Android uygulamanın okuyacağı nihai veri tabanı yapısı
uygulama_veritabani = {
    "uygulama_adi": "Islami Rehber App",
    "guncellenme_tarihi": "2026-09-10",
    "cuma_mesajlari": cuma_json_listesi,
    "hikayeler": hikaye_json_listesi
}

# json dosyasını oluştur (Türkçe karakterleri bozmadan)
os.makedirs('android_api', exist_ok=True)
dosya_yolu = 'android_api/uygulama_verileri.json'

with open(dosya_yolu, 'w', encoding='utf-8') as f:
    json.dump(uygulama_veritabani, f, ensure_ascii=False, indent=4)

print(f"🎉 BÜYÜK BAŞARI! Tüm veriler '{dosya_yolu}' dosyasına kaydedildi.")
