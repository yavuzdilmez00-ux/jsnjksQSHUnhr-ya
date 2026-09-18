import os
import json
import random
from typing import List

class MessageEngine:
    def __init__(self, output_dir: str = "veriler"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 1. MANEVİ VE UHREVİ DUALAR
        self.MANEVI_DUALAR = [
            "Allah dualarınızı kabul etsin.",
            "Yüce Mevla dualarınızı dergahında makbul eylesin.",
            "Rabbim ibadetlerinizi kabul etsin, günahlarınızı affeylesin.",
            "Allah sizi darlıktan ve sıkıntıdan muhafaza eylesin.",
            "Rabbim inayetini ve rahmetini üzerinizden eksik etmesin.",
            "Rabbim her işinizi rast getirsin, yolunuzu açık etsin.",
            "Allah dünya ve ahiret saadeti nasip eylesin.",
            "Mevla görelim neyler, neylerse güzel eyler.",
            "Rabbim bizleri doğru yoldan, sırat-ı müstakimden ayırmasın.",
            "Allah kalbinizden imanı, dilinizden duayı eksik etmesin.",
            "Yüce Rabbim bizleri bağışlanan kullarından eylesin."
        ]

        # 2. HAYAT VE HUZUR DUALARI
        self.HAYAT_DUALARI = [
            "Gününüz aydın, kalbiniz huzur dolsun.",
            "Rabbim dert verip derman aratmasın.",
            "Evinizden bereket, yüzünüzden tebessüm hiç eksik olmasın.",
            "Sağlık, mutluluk ve huzur yakanızı hiç bırakmasın.",
            "Rabbim sevdiklerinizi size bağışlasın.",
            "İşleriniz rast gitsin, kazancınız bereketli olsun.",
            "Yuvanıza huzur, kalbinize nur dolsun.",
            "Ömrünüz bereketli, yuvanız şen olsun.",
            "Gönlünüzden geçen tüm güzellikler sizi bulsun.",
            "Rabbim görünür görünmez kazalardan muhafaza eylesin.",
            "Allah dertlilere deva, hastalara şifa ihsan eylesin."
        ]

        # 3. GENİŞLETİLMİŞ VE HER KATEGORİ İÇİN ZENGİNLEŞTİRİLMİŞ ÖZEL GÜN CÜMLELERİ
        self.KATEGORILER = {
            "cuma": {
                "ozel": [
                    "Mübarek Cuma gününün rahmeti ve bereketi üzerinize olsun.",
                    "Haftanın en nurlu gününde dualarda buluşalım.",
                    "Cuma vaktinin feyzi hanenize dolsun.",
                    "Af kapılarının açıldığı bu mübarek günde dualarınız kabul olsun.",
                    "Gönüllerin duada birleştiği bu mübarek Cuma vaktinde,",
                    "Meleklerin duaya durduğu bu eşsiz günde,",
                    "Huzurun ve bereketin yeryüzüne indiği bu Cuma gününde,",
                    "Cumanın manevi iklimi yüreklerinizi ferahlatsın.",
                    "Haftanın en bereketli sabahına uyanmanın şükrüyle,",
                    "Gönül kapılarının Rabb'e açıldığı bu müstesna vakitte,",
                    "Duaların geri çevrilmediği bu feyizli Cuma saatinde,"
                ],
                "kapanis": ["Hayırlı Cumalar.", "Cumanız mübarek olsun.", "Nurlu Cumalar.", "Bereketli Cumalar dilerim.", "Selam ve dua ile hayırlı Cumalar."]
            },
            "ramazan_ayi": {
                "ozel": [
                    "On bir ayın sultanının bereketi hanenize dolsun.",
                    "Rahmet ayında kalbiniz imanla, sofranız bereketle dolsun.",
                    "Oruçlarınız ve ibadetleriniz makbul olsun.",
                    "Ramazan'ın manevi huzuru tüm hanenizi sarsın.",
                    "Mağfiret kapılarının ardına kadar açıldığı bu mübarek ayda,",
                    "Gönüllerin arındığı, sabrın pekiştiği Ramazan-ı Şerif'te,",
                    "Kur'an ayının feyzi ve bereketi yüreğinizi aydınlatsın.",
                    "İftar sofralarının bereketiyle hanelerinizin şenlendiği bu günlerde,",
                    "Başı rahmet, ortası mağfiret olan bu bereketli günlerde,",
                    "Cehennemden azat olunan bu kutlu mevsimde,"
                ],
                "kapanis": ["Hayırlı Ramazanlar.", "Ramazan ayınız mübarek olsun.", "Bereketli iftarlar.", "Hayırlı sahurlar.", "Ramazan-ı Şerifiniz mübarek olsun."]
            },
            "ramazan_bayrami": {
                "ozel": [
                    "Küslerin barıştığı bu mübarek günde barış ve huzur sizinle olsun.",
                    "Şeker tadında, neşe dolu bir bayram geçirmeniz dileğiyle.",
                    "Bayram sabahının neşesi kalbinize dolsun.",
                    "Oruçla arındığımız bir ayın ardından kavuştuğumuz bu şükür bayramında,",
                    "Sevincin çoğaldığı, umutların yeşerdiği bu güzel bayram coşkusunda,",
                    "Gönül köprülerinin kurulduğu bu bayram sabahında,",
                    "Uzakların yakın olduğu, gönüllerin birleştiği bu anlamlı günde,",
                    "Ramazanın manevi ikliminden çıkıp kavuştuğumuz bu mübarek bayramda,"
                ],
                "kapanis": ["İyi bayramlar.", "Hayırlı bayramlar.", "Ramazan Bayramınız mübarek olsun.", "Mutlu bayramlar dilerim."]
            },
            "kurban_bayrami": {
                "ozel": [
                    "Paylaşmanın ve teslimiyetin bayramında tüm dualarınız kabul olsun.",
                    "Kestiğiniz kurbanlar, ettiğiniz niyetler makbul olsun.",
                    "Kardeşliğin pekiştiği bu bayramda yüzünüz hep gülsün.",
                    "Hz. İbrahim'in sadakatiyle idrak ettiğimiz bu mübarek bayramda,",
                    "Allah'a yakınlaşmayı dilediğimiz bu müstesna günde,",
                    "Kurban ibadetinin getirdiği manevi huzur tüm hayatınıza yayılsın.",
                    "Yardımlaşmanın en güzel örneği olan bu bereketli bayramda,",
                    "Teslimiyetin sırrına erdiğimiz bu eşsiz Kurban Bayramı'nda,"
                ],
                "kapanis": ["Kurban Bayramınız mübarek olsun.", "İyi bayramlar.", "Hayırlı ve bereketli bayramlar.", "Bayramınız mübarek olsun."]
            },
            "mevlid_kandili": {
                "ozel": [
                    "Peygamber Efendimizin (s.a.v) şefaati üzerinize olsun.",
                    "Bu kutlu gecede O'nun (s.a.v) nuru kalbinizi aydınlatsın.",
                    "Alemlere rahmet olarak gönderilen Peygamberimizin dünyaya teşrif ettiği bu gecede,",
                    "Salat ve selamın en güzeli O'nun üzerine olsun dediğimiz bu vakitte,",
                    "Gönüllerimizin Peygamber sevgisiyle dolduğu bu feyizli gecede,",
                    "Kainatın efendisinin doğumuyla şereflenen bu mübarek gecede,",
                    "O'nun ahlakıyla ahlaklanmayı dilediğimiz bu kutlu kandil gecesinde,"
                ],
                "kapanis": ["Hayırlı kandiller.", "Mevlid Kandiliniz mübarek olsun.", "Dualarda buluşmak dileğiyle, hayırlı kandiller."]
            },
            "regaip_kandili": {
                "ozel": [
                    "Üç ayların müjdecisi olan bu gecede rahmet hanenize yağsın.",
                    "Regaip gecesinin feyzi ve bereketi ömrünüzü kuşatsın.",
                    "Rabbimizin rahmetinin sağanak sağanak yağdığı bu kutlu gecede,",
                    "Manevi mevsimin başlangıcı olan bu bereketli vakitte,",
                    "Gönüllerin dualarla yıkandığı bu feyizli gecede,",
                    "Regaip kandilinin nuruyla kalplerimizin arındığı bu anlarda,",
                    "İlahi lütufların bolca ihsan edildiği bu müstesna gecede,"
                ],
                "kapanis": ["Hayırlı kandiller.", "Regaip Kandiliniz mübarek olsun.", "Üç aylarınız mübarek olsun."]
            },
            "mirac_kandili": {
                "ozel": [
                    "Mucizelerle dolu bu gecede dualarınız gökyüzüne ulaşsın.",
                    "Miracın manevi huzuru yüreğinize dolsun.",
                    "Peygamber Efendimizin göklere yükseldiği bu mucizevi gecede,",
                    "Namazın müminlere hediye edildiği bu kutlu Miraç Kandili'nde,",
                    "Sırların ve hikmetlerin tecelli ettiği bu müstesna gecede,",
                    "İsra ve Miracın derin manasını idrak ettiğimiz bu mübarek gecede,",
                    "Yüce Yaratıcıya olan bağlılığımızın perçinlendiği bu anlarda,"
                ],
                "kapanis": ["Hayırlı kandiller.", "Miraç Kandiliniz mübarek olsun.", "Dualarla, hayırlı kandiller."]
            },
            "berat_kandili": {
                "ozel": [
                    "Günahların affedildiği bu gecede beratını alanlardan olmanız dileğiyle.",
                    "İlahi rahmetin tecelli ettiği bu mübarek vakitte dualarınız kabul olsun.",
                    "Borçların edası ve kalplerin temize çıkması için vesile olan bu gecede,",
                    "Rabbimizin sonsuz mağfiretine sığındığımız mübarek Berat Kandili'nde,",
                    "Kaderlerin hayırla yazıldığı bu feyizli gecede,",
                    "Kurtuluş ve af gecesi olan Berat kandilinin nuru hanenize dolsun,",
                    "Ellerin semaya af dilemek için açıldığı bu eşsiz gecede,"
                ],
                "kapanis": ["Hayırlı kandiller.", "Berat Kandiliniz mübarek olsun.", "Berat geceniz hayırlara vesile olsun."]
            },
            "kadir_gecesi": {
                "ozel": [
                    "Bin aydan hayırlı olan bu gecede melekler dualarınıza amin desin.",
                    "Kadir Gecesi'nin nuru tüm hayatınızı aydınlatsın.",
                    "Kur'an-ı Kerim'in yeryüzüne inmeye başladığı bu kutlu gecede,",
                    "Af kapılarının ardına kadar açık olduğu, huzur dolu bu anlarda,",
                    "Ellerin semaya, dillerin duaya yöneldiği bu eşsiz gecede,",
                    "Bin aydan daha bereketli bu müstesna zaman diliminde,",
                    "Cebrail'in (a.s) ve meleklerin yeryüzüne indiği bu nurani gecede,"
                ],
                "kapanis": ["Kadir Geceniz mübarek olsun.", "Hayırlı kandiller.", "Dualarınız kabul, geceniz mübarek olsun."]
            },
            "hicri_yilbasi": {
                "ozel": [
                    "Yeni Hicri yılın hanenize huzur ve barış getirmesini dilerim.",
                    "Yeni yılda yeni umutlar daima sizinle olsun.",
                    "Yeni bir Hicri yıla kavuşmanın manevi huzuru içerisinde,",
                    "Geçmişin muhasebesini yapıp yeni bir sayfa açtığımız bu günde,",
                    "Muharrem ayının feyzi ve bereketi ömrünüzü kuşatsın.",
                    "Hicri yeni yılımızın tüm İslam alemine hayırlar getirmesi duasıyla,",
                    "Hicretin derin manasını yüreğimizde hissettiğimiz bu yeni yılda,"
                ],
                "kapanis": ["Hicri Yılbaşınız mübarek olsun.", "Yeni yılınız hayırlı olsun.", "Muharrem ayınız mübarek olsun."]
            },
            "asure_gunu": {
                "ozel": [
                    "Aşurenin bereketi sofranızdan, ağzınızın tadı yuvanızdan eksik olmasın.",
                    "Birlik ve beraberliğin simgesi olan bu günde mutluluk yakanızı bırakmasın.",
                    "Paylaşmanın en güzel örneği olan bu bereketli günde,",
                    "Muharrem ayının incisi Aşure gününün feyzi hanenize dolsun.",
                    "Kardeşlik bağlarımızın daha da güçlendiği bu anlamlı günde,",
                    "Farklılıkların bir arada ahenk oluşturduğu bu güzel Aşure gününde,",
                    "Kerbela'nın hüznünü rahmete dönüştürmek ümidiyle dualarda buluşalım,"
                ],
                "kapanis": ["Aşure Gününüz mübarek olsun.", "Aşureniz bereketli olsun.", "Hayırlı günler dilerim."]
            }
        }

    def _generate_single_message(self, category: str) -> str:
        cat_data = self.KATEGORILER[category]
        yapi = random.choice([1, 2, 3])
        
        ozel = random.choice(cat_data["ozel"])
        kapanis = random.choice(cat_data["kapanis"])
        
        secim = random.choice(["tek_manevi", "tek_hayat", "ikisi_birarada"])
        
        if secim == "tek_manevi":
            dua = random.choice(self.MANEVI_DUALAR)
        elif secim == "tek_hayat":
            dua = random.choice(self.HAYAT_DUALARI)
        else:
            dua1 = random.choice(self.MANEVI_DUALAR)
            dua2 = random.choice(self.HAYAT_DUALARI)
            dua = f"{dua1} {dua2}"
        
        if yapi == 1:
            mesaj = f"{ozel} {dua} {kapanis}"
        elif yapi == 2:
            mesaj = f"{dua} {ozel} {kapanis}"
        else:
            mesaj = f"{dua} {kapanis}"
            
        return " ".join(mesaj.split())

    def generate_unique_batch(self, category: str, count: int) -> List[str]:
        if category not in self.KATEGORILER:
            return []

        generated = set()
        deneme = 0
        maks_deneme = count * 20
        onceki_uzunluk = 0
        tekrara_dusme_sayaci = 0

        while len(generated) < count and deneme < maks_deneme:
            yeni_mesaj = self._generate_single_message(category)
            generated.add(yeni_mesaj)
            
            if len(generated) == onceki_uzunluk:
                tekrara_dusme_sayaci += 1
            else:
                tekrara_dusme_sayaci = 0
                onceki_uzunluk = len(generated)
                
            if tekrara_dusme_sayaci > 1500: 
                break
                
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

    for gun in dini_gunler:
        yeni_mesajlar = engine.generate_unique_batch(category=gun, count=1000)
        engine.save_to_json(category=gun, new_messages=yeni_mesajlar)
