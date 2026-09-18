import os
import json
import random
from typing import List

class MessageEngine:
    def __init__(self, output_dir: str = "veriler"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 1. PARÇA: HİTAPLAR
        self.HITAP = [
            "", "", "", "", 
            "Kıymetli dostlar,", "Sevgili kardeşim,", "Değerli müminler,",
            "Gönül dostlarım,", "Kıymetli ailem,", "Canım sevdiklerim,",
            "Değerli kardeşlerim,", "Güzel insanlar,"
        ]

        # 2. PARÇA: ZAMAN VE DUYGU GİRİŞİ
        self.ZAMAN_GIRIS = [
            "Rahmet rüzgarlarının estiği bu kutlu vakitte,",
            "Gönüllerimizin sevgiyle dolduğu bu müstesna anlarda,",
            "Umutlarımızın yeşerdiği bu güzel günde,",
            "Duaların arşa yükseldiği bu bereketli zaman diliminde,",
            "Kardeşlik bağlarımızın en çok güçlendiği bu anlamlı vakitte,",
            "Yüreklerimizin aynı duada buluştuğu bu özel anlarda,",
            "Manevi iklimin her yanımızı sardığı bu feyizli günde,",
            "İyiliklerin ve güzelliklerin filizlendiği bu mutlu günde,",
            "Allah'ın rahmetinin yeryüzünü kuşattığı şu saatlerde,",
            "Ruhumuzun sükunet bulduğu bu mübarek vakitlerde,",
            "İçimizin huzurla dolup taştığı bu eşsiz günde,",
            "Dostlukların pekiştiği, kinin unutulduğu bu güzel zamanda,"
        ]
        
        # 3. PARÇA: DUALAR
        self.DUA = [
            "Rabbim ömrümüzü ve amelimizi hayırlı kılsın.",
            "Evimizden huzur, kalbimizden iman, soframızdan bereket eksik olmasın.",
            "Yüce Allah yaptığımız ve yapacağımız tüm ibadetleri dergahında kabul eylesin.",
            "Rabbim bizleri doğru yoldan, sırat-ı müstakimden ayırmasın.",
            "Gönlünüzden geçen, hakkınızda hayırlı olan tüm dualarınız kabul görsün.",
            "Allah'ın rahmeti, bereketi ve mağfireti daima sizinle olsun.",
            "Rabbim sıkıntılarınızı gidersin, yüzünüzü her daim güldürsün.",
            "Yüreklerimize inşirah, hastalarımıza şifa ihsan eyle Ya Rabbim.",
            "Allah bizleri sevdiklerimizle beraber cennetinde de buluştursun.",
            "Dünyaya barış, hanelerimize huzur ve kalplerimize tam bir teslimiyet nasip olsun.",
            "Allah bizleri darlıktan, yokluktan ve her türlü kötülükten muhafaza eylesin."
        ]

        # 4. PARÇA: ÖZEL GÜN ANLAMI VE KAPANIŞLARI
        self.KATEGORILER = {
            "cuma": {
                "ozel_anlam": [
                    "haftanın en nurlu gününe uyanmanın şükrüyle,",
                    "Cuma gününün bereketi ve feyzi üzerimize olsun diyerek,",
                    "af kapılarının açıldığı bu Cuma vaktinde,"
                ],
                "kapanis": ["Hayırlı Cumalar.", "Cumanız mübarek olsun.", "Bereketli Cumalar dilerim."]
            },
            "ramazan_ayi": {
                "ozel_anlam": [
                    "on bir ayın sultanı Ramazan-ı Şerif'in nuruyla aydınlanırken,",
                    "oruçlarımızla nefsimizi terbiye ettiğimiz bu kutlu ayda,",
                    "iftar sofralarının bereketiyle hanelerimiz şenlenirken,"
                ],
                "kapanis": ["Hayırlı Ramazanlar.", "Ramazan-ı Şerifiniz mübarek olsun.", "Bereketli iftarlar dilerim."]
            },
            "ramazan_bayrami": {
                "ozel_anlam": [
                    "oruçla arındığımız bir ayın ardından kavuştuğumuz bu şükür bayramında,",
                    "küslerin barıştığı, sevgilerin tazelendiği bu mübarek Ramazan Bayramı'nda,",
                    "gönül köprülerinin kurulduğu, sevincin paylaşıldığı bu bayram sabahında,",
                    "ellerin hasretle kenetlendiği bu güzel bayram coşkusunda,"
                ],
                "kapanis": ["Ramazan Bayramınız mübarek olsun.", "Huzur dolu, hayırlı bayramlar dilerim.", "İyi bayramlar."]
            },
            "kurban_bayrami": {
                "ozel_anlam": [
                    "teslimiyetin ve paylaşmanın simgesi olan bu mübarek Kurban Bayramı'nda,",
                    "Hz. İbrahim'in sadakatiyle idrak ettiğimiz bu bayramda,",
                    "kurban ibadetimizle Allah'a yakınlaşmayı dilediğimiz bu günde,"
                ],
                "kapanis": ["Kurban Bayramınız mübarek olsun.", "Kestiğiniz kurbanlar kabul olsun, iyi bayramlar.", "Hayırlı bayramlar."]
            },
            "mevlid_kandili": {
                "ozel_anlam": [
                    "Peygamber Efendimizin (s.a.v) dünyaya teşrif ettiği bu gecede,",
                    "gönüllerimizin O'nun (s.a.v) nuruyla aydınlandığı Mevlid Kandili'nde,",
                    "salat ve selamın en güzeli O'nun üzerine olsun dediğimiz bu vakitte,"
                ],
                "kapanis": ["Mevlid Kandiliniz mübarek olsun.", "Hayırlı kandiller.", "Peygamber efendimizin şefaatine nail olmak duasıyla."]
            },
            "regaip_kandili": {
                "ozel_anlam": [
                    "üç ayların müjdecisi olan mübarek Regaip Kandili'nde,",
                    "Rabbimizin rahmetinin sağanak yağdığı bu Regaip gecesinde,"
                ],
                "kapanis": ["Regaip Kandiliniz mübarek olsun.", "Üç aylarımız hayırlara vesile olsun.", "Hayırlı kandiller."]
            },
            "mirac_kandili": {
                "ozel_anlam": [
                    "Peygamber Efendimizin göklere yükseldiği bu mucizevi Miraç gecesinde,",
                    "namazın müminlere hediye edildiği bu kutlu Miraç Kandili'nde,"
                ],
                "kapanis": ["Miraç Kandiliniz mübarek olsun.", "Miracın bereketi üzerinize olsun, hayırlı kandiller."]
            },
            "berat_kandili": {
                "ozel_anlam": [
                    "günahların affı ve kalplerin temize çıkması için vesile olan Berat gecesinde,",
                    "ilahi rahmetin yeryüzüne tecelli ettiği bu feyizli vakitte,"
                ],
                "kapanis": ["Berat Kandiliniz mübarek olsun.", "Rabbim bizleri beratını alanlardan eylesin, hayırlı kandiller."]
            },
            "kadir_gecesi": {
                "ozel_anlam": [
                    "bin aydan daha hayırlı olan Kadir Gecesi hürmetine,",
                    "semadan meleklerin indiği, duaların geri çevrilmediği bu kutlu gecede,"
                ],
                "kapanis": ["Kadir Geceniz mübarek olsun.", "Rabbim Kadir gecesinin nurundan nasiplenmeyi nasip etsin."]
            },
            "hicri_yilbasi": {
                "ozel_anlam": [
                    "yeni bir Hicri yıla, Muharrem ayına kavuşmanın manevi huzuru içerisinde,",
                    "geçmişin muhasebesini yapıp yeni bir sayfa açtığımız Hicri Yılbaşında,"
                ],
                "kapanis": ["Hicri Yeni Yılınız mübarek olsun.", "Muharrem ayınız ve Hicri yılbaşınız mübarek olsun."]
            },
            "asure_gunu": {
                "ozel_anlam": [
                    "paylaşmanın, birliğin ve bereketin simgesi olan Aşure Günü'nde,",
                    "kardeşlik bağlarımızı pekiştirdiğimiz bu anlamlı günde,"
                ],
                "kapanis": ["Aşure Gününüz mübarek olsun.", "Aşureniz bereketli, yuvanız huzurlu olsun."]
            }
        }

    def _generate_single_message(self, category: str) -> str:
        hitap = random.choice(self.HITAP)
        zaman_giris = random.choice(self.ZAMAN_GIRIS)
        ozel_anlam = random.choice(self.KATEGORILER[category]["ozel_anlam"])
        dualar = random.sample(self.DUA, k=random.choice([1, 2]))
        dua_kismi = " ".join(dualar)
        kapanis = random.choice(self.KATEGORILER[category]["kapanis"])
        
        mesaj = f"{hitap} {zaman_giris} {ozel_anlam} {dua_kismi} {kapanis}"
        return " ".join(mesaj.split())

    def generate_unique_batch(self, category: str, count: int) -> List[str]:
        if category not in self.KATEGORILER:
            return []

        generated = set()
        deneme = 0
        maks_deneme = count * 30 

        while len(generated) < count and deneme < maks_deneme:
            yeni_mesaj = self._generate_single_message(category)
            generated.add(yeni_mesaj)
            deneme += 1

        sonuclar = list(generated)
        random.shuffle(sonuclar)
        return sonuclar

    def save_to_json(self, category: str, new_messages: List[str]):
        if not new_messages:
            return

        filepath = os.path.join(self.output_dir, f"{category}.json")
        existing_data = []

        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
            except json.JSONDecodeError:
                pass

        total_data = list(set(existing_data + new_messages))

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(total_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    engine = MessageEngine(output_dir="veriler")
    
    dini_gunler = [
        "cuma", "ramazan_ayi", "ramazan_bayrami", "kurban_bayrami", 
        "mevlid_kandili", "regaip_kandili", "mirac_kandili", 
        "berat_kandili", "kadir_gecesi", "hicri_yilbasi", "asure_gunu"
    ]

    # HER ÇALIŞTIRILDIĞINDA ARTIK 200 MESAJ ÜRETİR
    for gun in dini_gunler:
        yeni_mesajlar = engine.generate_unique_batch(category=gun, count=200)
        engine.save_to_json(category=gun, new_messages=yeni_mesajlar)
