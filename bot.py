import os
import json
import random
from typing import List

# ==========================================
# KÜTÜPHANE BÖLÜMÜ (MessageEngine Sınıfı)
# ==========================================
class MessageEngine:
    """Özel günler için dinamik, sınırsız ve benzersiz mesaj üreten motor."""

    TEMPLATES = {
        "cuma": {
            "giris": [
                "Gönüllerin dua ile birleştiği bu mübarek günde,",
                "Huzurun, bereketin ve rahmetin sağanak gibi yağdığı Cuma gününde,",
                "Ey Rabbimiz! Açılan elleri, yönelen kalpleri boş çevirme.",
                "Rabbim ömrümüzü ve amelimizi hayırlı kılsın.",
                "Bugün af kapılarının sonuna kadar açıldığı mübarek gündür."
            ],
            "govde": [
                "Cumanız mübarek, dualarınız ve ibadetleriniz kabul olsun.",
                "Evinizden huzur, kalbinizden sevgi, sofranızdan bereket eksik olmasın.",
                "Yüreklerimize inşirah, hastalarımıza şifa, dertlilerimize deva ihsan eyle.",
                "Tüm sevdiklerinizle birlikte esenlik dolu, feyizli bir gün dilerim.",
                "Bu mübarek vakit hürmetine gönlünüzden geçen tüm hayırlı dualar kabul görsün."
            ],
            "kapanis": [
                "Hayırlı Cumalar dilerim.",
                "Selam ve dua ile, bereketli Cumalar.",
                "Hayırlı, nurlu ve huzurlu Cumalar.",
                "Cumanız hayırlara vesile olsun.",
                "Dualarda buluşmak ümidiyle, Hayırlı Cumalar."
            ]
        },
        "ramazan": {
            "giris": [
                "On bir ayın sultanı Ramazan-ı Şerif'in gelişiyle,",
                "Başı rahmet, ortası mağfiret, sonu cehennemden kurtuluş olan bu ayda,",
                "Gönüllerin arındığı, sabrın ve şükrün pekiştiği mübarek Ramazan'da,",
                "Oruçlarımızla nefsimizi terbiye ettiğimiz bu kutlu mevsimde,"
            ],
            "govde": [
                "Tuttuğunuz oruçlar, ettiğiniz dualar dergâh-ı izzette kabul olsun.",
                "İftar sofralarınız bereketli, haneniz huzur ve afiyetle dolsun.",
                "Paylaşmanın, kardeşliğin ve birliğin bereketi üzerinize olsun.",
                "Yüce Allah bizleri bayrama günahlarından arınmış olarak ulaştırsın."
            ],
            "kapanis": [
                "Hayırlı Ramazanlar dilerim.",
                "Ramazan-ı Şerifiniz mübarek olsun.",
                "Huzurlu ve bereketli bir Ramazan ayı geçirmeniz dileğiyle.",
                "Dualarınız kabul, Ramazanınız nurlu olsun."
            ]
        },
        "bayram": {
            "giris": [
                "Küslerin barıştığı, sevgilerin tazelendiği bu mübarek bayramda,",
                "Birlik, beraberlik ve kardeşlik duygularının pekiştiği bayram gününde,",
                "Uzakların yakın olduğu, gönüllerin birleştiği bu güzel günde,"
            ],
            "govde": [
                "Sevdiklerinizle birlikte sağlıklı, mutlu ve neşe dolu bir bayram geçirmenizi dilerim.",
                "Hanenize huzur, kalbinize sevinç, ömrünüze bereket dolsun.",
                "Bayramın getirdiği manevi huzur tüm hayatınıza yayılsın."
            ],
            "kapanis": [
                "Bayramınız mübarek olsun.",
                "İyi bayramlar dilerim.",
                "Huzur dolu, hayırlı bayramlar.",
                "En kalbi duygularımla bayramınızı tebrik ederim."
            ]
        },
        "kadir_gecesi": {
            "giris": [
                "Bin aydan daha hayırlı olan Kadir Gecesi hürmetine,",
                "Semadan meleklerin indiği, duaların geri çevrilmediği bu kutlu gecede,",
                "Kur'an-ı Kerim'in nuruyla aydınlanan bu feyizli gecede,"
            ],
            "govde": [
                "Rabbim günahlarımızı affeylesin, kalplerimizi nurlu kılsın.",
                "Yaptığınız tüm ibadetleri ve döktüğünüz gözyaşlarını kabul eylesin.",
                "Dünyaya barış, hanelerimize huzur ve kalplerimize teslimiyet versin."
            ],
            "kapanis": [
                "Kadir Geceniz mübarek olsun.",
                "Bu gecenin hayırlara vesile olmasını dilerim.",
                "Dualarda buluşmak üzere, hayırlı kandiller."
            ]
        }
    }

    def __init__(self, output_dir: str = "veriler"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_unique_batch(self, category: str, count: int = 50) -> List[str]:
        """İstenen kategoride belirtilen sayıda tekrarsız mesaj üretir."""
        if category not in self.TEMPLATES:
            raise ValueError(f"Geçersiz kategori: {category}")

        pool = self.TEMPLATES[category]
        generated = set()

        # Maksimum üretilebilecek benzersiz kombinasyon sayısını hesapla
        max_possible = len(pool["giris"]) * len(pool["govde"]) * len(pool["kapanis"])
        
        # Eğer istenen sayı (50), havuzun kapasitesinden büyükse, hedefi kapasiteye düşür
        hedef_sayi = min(count, max_possible)
        
        # Sonsuz döngüye girmemesi için güvenlik limiti (fail-safe)
        deneme_sayisi = 0
        maksimum_deneme = hedef_sayi * 10 

        # Hedeflenen sayıya ulaşana kadar rastgele permütasyon üretir
        while len(generated) < hedef_sayi and deneme_sayisi < maksimum_deneme:
            giris = random.choice(pool["giris"])
            govde = random.choice(pool["govde"])
            kapanis = random.choice(pool["kapanis"])
            
            mesaj = f"{giris} {govde} {kapanis}"
            generated.add(mesaj)
            deneme_sayisi += 1

        return list(generated)

    def save_to_json(self, category: str, new_messages: List[str]):
        """Yeni mesajları mevcut JSON dosyasına ekler, kopyaları eler."""
        filepath = os.path.join(self.output_dir, f"{category}.json")
        existing_data = []

        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []

        # Listeyi birleştirip tekrarlananları set ile temizle
        total_data = list(set(existing_data + new_messages))

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(total_data, f, ensure_ascii=False, indent=4)

        print(f"[{category}.json] -> {len(new_messages)} yeni mesaj eklendi. (Toplam: {len(total_data)})")


# ==========================================
# ÇALIŞTIRICI BÖLÜMÜ (Main)
# ==========================================
if __name__ == "__main__":
    engine = MessageEngine(output_dir="veriler")
    
    # İstediğin kategoriler
    kategoriler = ["cuma", "ramazan", "bayram", "kadir_gecesi"]

    for kat in kategoriler:
        # Her biri için maksimum kapasiteye göre (en fazla 50) mesaj üret ve kaydet
        yeni_mesajlar = engine.generate_unique_batch(category=kat, count=50)
        engine.save_to_json(category=kat, new_messages=yeni_mesajlar)
