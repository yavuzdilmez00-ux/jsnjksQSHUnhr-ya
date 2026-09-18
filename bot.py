import os
import json
import random
from typing import List

class MessageEngine:
    def __init__(self, output_dir: str = "veriler"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # =================================================================
        # 1. ORTAK HAVUZLAR (Tüm mesajlara rastgele serpiştirilecek parçalar)
        # =================================================================
        self.GENEL_HITAP = [
            "", "", "", # Bazen hitapsız başlasın diye boşluklar eklendi
            "Kıymetli dostlar,", "Sevgili kardeşim,", "Değerli müminler,",
            "Gönül dostlarım,", "Kıymetli ailem ve sevdiklerim,",
            "Değerli kardeşlerim,", "Güzel insanlar,"
        ]
        
        self.GENEL_DUA = [
            "Rabbim ömrümüzü ve amelimizi hayırlı kılsın.",
            "Evimizden huzur, kalbimizden iman, soframızdan bereket eksik olmasın.",
            "Yüce Allah yaptığımız ve yapacağımız tüm ibadetleri kabul eylesin.",
            "Rabbim bizleri sırat-ı müstakimden, doğru yoldan ayırmasın.",
            "Gönlünüzden geçen, hakkınızda hayırlı olan tüm dualarınız kabul görsün.",
            "Allah'ın rahmeti, bereketi ve mağfireti daima sizinle olsun.",
            "Rabbim sıkıntılarınızı gidersin, yüzünüzü güldürsün.",
            "Yüreklerimize inşirah, hastalarımıza şifa, dertlilerimize deva ihsan eyle Ya Rabbim.",
            "Allah bizleri sevdiklerimizle beraber cennetinde de buluştursun.",
            "Rabbim nefsimizin şerrinden ve şeytanın vesvesesinden bizleri muhafaza eylesin.",
            "Dünyaya barış, hanelerimize huzur ve kalplerimize tam bir teslimiyet nasip olsun."
        ]

        # =================================================================
        # 2. ÖZEL GÜN HAVUZLARI (Giriş ve Kapanışlar o güne özeldir)
        # =================================================================
        self.KATEGORILER = {
            "cuma": {
                "giris": [
                    "Huzurun, bereketin ve rahmetin yeryüzüne indiği bu Cuma vaktinde,",
                    "Haftanın en nurlu, en bereketli sabahına uyanmanın şükrüyle,",
                    "Rahmet kapılarının sonuna kadar açıldığı bu eşsiz Cuma gününde,"
                ],
                "kapanis": ["Hayırlı Cumalar.", "Cumanız mübarek olsun.", "Selam ve dua ile, bereketli Cumalar."]
            },
            "ramazan_ayi": {
                "giris": [
                    "On bir ayın sultanı, rahmet ve mağfiret ayı Ramazan-ı Şerif'te,",
                    "Oruçlarımızla nefsimizi terbiye ettiğimiz bu kutlu mevsimde,",
                    "İftar sofralarının bereketiyle hanelerimizin şenlendiği bu günlerde,"
                ],
                "kapanis": ["Hayırlı Ramazanlar.", "Ramazan-ı Şerifiniz mübarek olsun.", "Bereketli iftarlar ve sahurlar dilerim."]
            },
            "ramazan_bayrami": {
                "giris": [
                    "Oruçla arındığımız bir ayın ardından kavuştuğumuz bu şükür bayramında,",
                    "Şeker tadında, küslerin barıştığı, sevgilerin tazelendiği bu mübarek Ramazan Bayramı'nda,",
                    "Gönül köprülerinin kurulduğu, sevincin paylaşıldığı bu bayram sabahında,"
                ],
                "kapanis": ["Ramazan Bayramınız mübarek olsun.", "Huzur dolu, hayırlı bayramlar dilerim.", "İyi bayramlar."]
            },
            "kurban_bayrami": {
                "giris": [
                    "Teslimiyetin ve paylaşmanın simgesi olan bu mübarek Kurban Bayramı'nda,",
                    "Hz. İbrahim'in sadakati ve Hz. İsmail'in teslimiyetiyle idrak ettiğimiz bu bayramda,",
                    "Kurban ibadetimizle Allah'a yakınlaşmayı dilediğimiz bu müstesna günde,"
                ],
                "kapanis": ["Kurban Bayramınız mübarek olsun.", "Kestiğiniz kurbanlar, ettiğiniz dualar kabul olsun, iyi bayramlar.", "Hayırlı ve bereketli bayramlar."]
            },
            "mevlid_kandili": {
                "giris": [
                    "Alemlere rahmet olarak gönderilen Peygamber Efendimizin (s.a.v) dünyaya teşrif ettiği bu gecede,",
                    "Gönüllerimizin O'nun (s.a.v) nuruyla aydınlandığı mübarek Mevlid Kandili'nde,",
                    "Salat ve selamın en güzeli O'nun üzerine olsun dediğimiz bu kutlu gecede,"
                ],
                "kapanis": ["Mevlid Kandiliniz mübarek olsun.", "Hayırlı kandiller.", "Peygamber efendimizin şefaatine nail olmak duasıyla, kandiliniz mübarek olsun."]
            },
            "regaip_kandili": {
                "giris": [
                    "Rahmet, bereket ve mağfiret mevsimi üç ayların müjdecisi Regaip Kandili'nde,",
                    "Rabbimizin rahmetinin sağanak sağanak yağdığı bu kutlu Regaip gecesinde,",
                    "Gönüllerin dualarla yıkandığı bu feyizli gecede,"
                ],
                "kapanis": ["Regaip Kandiliniz mübarek olsun.", "Üç aylarımız ve Regaip Kandilimiz hayırlara vesile olsun.", "Dualarda buluşmak ümidiyle, hayırlı kandiller."]
            },
            "mirac_kandili": {
                "giris": [
                    "Peygamber Efendimizin (s.a.v) Mescid-i Haram'dan Mescid-i Aksa'ya, oradan da göklere yükseldiği bu mucizevi Miraç gecesinde,",
                    "Namazın müminlere hediye edildiği bu kutlu Miraç Kandili'nde,",
                    "Sırların ve hikmetlerin tecelli ettiği bu müstesna gecede,"
                ],
                "kapanis": ["Miraç Kandiliniz mübarek olsun.", "Miracın feyzi ve bereketi üzerinize olsun, hayırlı kandiller.", "Mirac Kandilimiz mübarek, dualarımız makbul olsun."]
            },
            "berat_kandili": {
                "giris": [
                    "Günahların affı, borçların edası ve kalplerin temize çıkması için vesile olan Berat gecesinde,",
                    "İlahi rahmetin yeryüzüne tecelli ettiği, kaderlerin yazıldığı bu feyizli gecede,",
                    "Rabbimizin sonsuz mağfiretine sığındığımız mübarek Berat Kandili'nde,"
                ],
                "kapanis": ["Berat Kandiliniz mübarek olsun.", "Rabbim bizleri beratını alanlardan eylesin, hayırlı kandiller.", "Berat gecemiz mübarek olsun."]
            },
            "kadir_gecesi": {
                "giris": [
                    "Kur'an-ı Kerim'in inmeye başladığı, bin aydan daha hayırlı olan Kadir Gecesi hürmetine,",
                    "Semadan meleklerin indiği, duaların geri çevrilmediği bu kutlu Kadir gecesinde,",
                    "Af kapılarının ardına kadar açık olduğu, huzur dolu bu mübarek gecede,"
                ],
                "kapanis": ["Kadir Geceniz mübarek olsun.", "Rabbim Kadir gecesinin nurundan nasiplenmeyi nasip etsin.", "Kadir gecemiz mübarek, dualarımız kabul olsun."]
            },
            "hicri_yilbasi": {
                "giris": [
                    "Yeni bir Hicri yıla, Muharrem ayına kavuşmanın manevi huzuru içerisinde,",
                    "Peygamberimizin hicretini ve İslam'ın yayılışını hatırladığımız bu yeni yılda,",
                    "Geçmişin muhasebesini yapıp yeni bir sayfa açtığımız Hicri Yılbaşında,"
                ],
                "kapanis": ["Hicri Yeni Yılınız mübarek olsun.", "Yeni Hicri yılımız İslam alemine hayırlar getirsin.", "Muharrem ayınız ve Hicri yılbaşınız mübarek olsun."]
            },
            "asure_gunu": {
                "giris": [
                    "Paylaşmanın, birliğin ve bereketin simgesi olan Muharrem ayı ve Aşure Günü'nde,",
                    "Pek çok peygamberin mucizesine şahitlik eden, güzelliklerin habercisi bu mübarek günde,",
                    "Kerbela'nın hüznünü yüreğimizde taşıyıp, kardeşlik bağlarımızı pekiştirdiğimiz Aşure gününde,"
                ],
                "kapanis": ["Aşure Gününüz mübarek olsun.", "Aşureniz bereketli, yuvanız huzurlu olsun.", "Rabbim birliğimizi ve beraberliğimizi daim kılsın, Aşure gününüz mübarek olsun."]
            }
        }

    def _generate_single_message(self, category: str) -> str:
        """Kombinasyon motoru ile 1 adet rastgele mesaj oluşturur."""
        hitap = random.choice(self.GENEL_HITAP)
        giris = random.choice(self.KATEGORILER[category]["giris"])
        
        # Rastgele 1 veya 2 farklı dua seç (daha zengin mesajlar için)
        secilen_dualar = random.sample(self.GENEL_DUA, k=random.choice([1, 2]))
        dua_kismi = " ".join(secilen_dualar)
        
        kapanis = random.choice(self.KATEGORILER[category]["kapanis"])
        
        # Parçaları birleştir ve gereksiz boşlukları temizle
        mesaj = f"{hitap} {giris} {dua_kismi} {kapanis}"
        return " ".join(mesaj.split())

    def generate_unique_batch(self, category: str, count: int = 50) -> List[str]:
        """İstenen sayıda tamamen benzersiz mesajlar kümesi üretir."""
        if category not in self.KATEGORILER:
            print(f"Uyarı: {category} bulunamadı, atlanıyor.")
            return []

        generated = set()
        deneme = 0
        maks_deneme = count * 20 # Sonsuz döngü koruması

        while len(generated) < count and deneme < maks_deneme:
            yeni_mesaj = self._generate_single_message(category)
            generated.add(yeni_mesaj)
            deneme += 1

        return list(generated)

    def save_to_json(self, category: str, new_messages: List[str]):
        """Oluşturulan mesajları dosyaya yazar, önceki tekrarları temizler."""
        if not new_messages:
            return

        filepath = os.path.join(self.output_dir, f"{category}.json")
        existing_data = []

        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []

        # Listeyi birleştir ve kopyaları set ile yok et
        total_data = list(set(existing_data + new_messages))

        # JSON'u oluştur (Türkçe karakter sorunu olmaması için ensure_ascii=False)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(total_data, f, ensure_ascii=False, indent=4)

        print(f"✅ [{category}.json] dosyasına {len(new_messages)} mesaj eklendi. (Toplam limit: ∞, Şu anki: {len(total_data)})")


if __name__ == "__main__":
    engine = MessageEngine(output_dir="veriler")
    
    # Motorun çalışacağı tüm günlerin listesi
    # Bunlar KATEGORILER sözlüğündeki isimlerle birebir aynı olmalıdır
    dini_gunler = [
        "cuma", "ramazan_ayi", "ramazan_bayrami", "kurban_bayrami", 
        "mevlid_kandili", "regaip_kandili", "mirac_kandili", 
        "berat_kandili", "kadir_gecesi", "hicri_yilbasi", "asure_gunu"
    ]

    for gun in dini_gunler:
        # Her tetiklemede her biri için 50 tane taptaze mesaj üretilir
        yeni_mesajlar = engine.generate_unique_batch(category=gun, count=50)
        engine.save_to_json(category=gun, new_messages=yeni_mesajlar)
