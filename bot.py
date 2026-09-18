import os
import json
import random
from typing import List

class MessageEngine:
    def __init__(self, output_dir: str = "veriler"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 1. KISA VE GENEL DUALAR (Hitaplar tamamen kaldırıldı, dualar genişletildi)
        self.KISA_DUALAR = [
            "Allah dualarınızı kabul etsin.", "Gününüz aydın, kalbiniz huzur dolsun.",
            "Rabbim dert verip derman aratmasın.", "Gönlünüzden geçenler hayırlısıyla ömrünüze nasip olsun.",
            "Evinizden bereket, yüzünüzden tebessüm eksik olmasın.", "Sağlık, mutluluk ve huzur yakanızı hiç bırakmasın.",
            "Rabbim sevdiklerinizi size bağışlasın.", "Ne muradınız varsa Rabbim nasip etsin.",
            "Allah sizi darlıktan ve sıkıntıdan muhafaza eylesin.", "İşleriniz rast gitsin, kazancınız bereketli olsun.",
            "Rabbim gönlünüze göre versin.", "Dünya ve ahiret saadetiniz daim olsun.",
            "Yuvanıza huzur, kalbinize nur dolsun.", "Allah dertlilere deva, hastalara şifa versin.",
            "Rabbim her işinizi rast getirsin.", "Allah sağlığınızı daim etsin.",
            "Ömrünüz bereketli, yuvanız şen olsun.", "Rabbim sizi kötülüklerden korusun.",
            "Gönlünüzden geçen tüm güzellikler sizi bulsun.", "Allah yolunuzu açık etsin.",
            "Yüzünüzden gülümseme hiç eksik olmasın.", "Dualarınız makbul, gününüz güzel geçsin.",
            "Mevla görelim neyler, neylerse güzel eyler.", "Rabbim inayetini ve rahmetini üzerimizden eksik etmesin."
        ]

        # 2. KATEGORİLER VE GENEL DURUMLAR
        self.KATEGORILER = {
            "cuma": {
                "ozel": [
                    "Mübarek Cuma gününün rahmeti üzerimize olsun.",
                    "Haftanın en nurlu gününde dualarda buluşalım.",
                    "Cuma vaktinin feyzi hanelerimize dolsun.",
                    "Af kapılarının açıldığı bu mübarek günde dualarımız bir olsun."
                ],
                "kapanis": ["Hayırlı Cumalar.", "Cumanız mübarek olsun.", "Nurlu Cumalar.", "Bereketli Cumalar dilerim.", "Selam ve dua ile hayırlı Cumalar."]
            },
            "ramazan_ayi": {
                "ozel": [
                    "On bir ayın sultanının bereketi üzerimize olsun.",
                    "Rahmet ayında kalplerimiz imanla, sofralarımız bereketle dolsun.",
                    "Oruçlarımız ve ibadetlerimiz makbul olsun.",
                    "Ramazan'ın huzuru tüm İslam alemini sarsın."
                ],
                "kapanis": ["Hayırlı Ramazanlar.", "Ramazan ayınız mübarek olsun.", "Bereketli iftarlar.", "Hayırlı sahurlar.", "Ramazan-ı Şerifiniz mübarek olsun."]
            },
            "ramazan_bayrami": {
                "ozel": [
                    "Küslerin barıştığı, sevginin çoğaldığı bu mübarek günde barış ve huzur hakim olsun.",
                    "Şeker tadında, neşe dolu bir bayram geçirmemiz dileğiyle.",
                    "Bayram sabahının neşesi kalplerimize dolsun."
                ],
                "kapanis": ["İyi bayramlar.", "Hayırlı bayramlar.", "Ramazan Bayramımız mübarek olsun.", "Mutlu bayramlar dilerim."]
            },
            "kurban_bayrami": {
                "ozel": [
                    "Paylaşmanın ve teslimiyetin bayramında tüm dualarımız kabul olsun.",
                    "Kestiğimiz kurbanlar, ettiğimiz niyetler makbul olsun.",
                    "Kardeşliğin pekiştiği bu bayramda yüzümüz hep gülsün."
                ],
                "kapanis": ["Kurban Bayramınız mübarek olsun.", "İyi bayramlar.", "Hayırlı ve bereketli bayramlar.", "Bayramımız mübarek olsun."]
            },
            "mevlid_kandili": {
                "ozel": [
                    "Peygamber Efendimizin (s.a.v) şefaati üzerimize olsun.",
                    "Bu kutlu gecede O'nun (s.a.v) nuru kalplerimizi aydınlatsın."
                ],
                "kapanis": ["Hayırlı kandiller.", "Mevlid Kandiliniz mübarek olsun.", "Dualarda buluşmak dileğiyle, hayırlı kandiller."]
            },
            "regaip_kandili": {
                "ozel": [
                    "Üç ayların müjdecisi olan bu gecede rahmet sağanak sağanak yağsın.",
                    "Regaip gecesinin feyzi ve bereketi hanelerimizi kuşatsın."
                ],
                "kapanis": ["Hayırlı kandiller.", "Regaip Kandiliniz mübarek olsun.", "Üç aylarımız mübarek olsun."]
            },
            "mirac_kandili": {
                "ozel": [
                    "Mucizelerle dolu bu gecede dualarımız gökyüzüne ulaşsın.",
                    "Miracın manevi huzuru yüreklerimize dolsun."
                ],
                "kapanis": ["Hayırlı kandiller.", "Miraç Kandiliniz mübarek olsun.", "Dualarla, hayırlı kandiller."]
            },
            "berat_kandili": {
                "ozel": [
                    "Günahların affedildiği bu gecede beratını alanlardan olmamız dileğiyle.",
                    "İlahi rahmetin tecelli ettiği bu mübarek vakitte dualarımız kabul olsun."
                ],
                "kapanis": ["Hayırlı kandiller.", "Berat Kandiliniz mübarek olsun.", "Berat gecemiz hayırlara vesile olsun."]
            },
            "kadir_gecesi": {
                "ozel": [
                    "Bin aydan hayırlı olan bu gecede melekler dualarımıza amin desin.",
                    "Kadir Gecesi'nin nuru tüm hayatımızı aydınlatsın."
                ],
                "kapanis": ["Kadir Geceniz mübarek olsun.", "Hayırlı kandiller.", "Dualarımız kabul, gecemiz mübarek olsun."]
            },
            "hicri_yilbasi": {
                "ozel": [
                    "Yeni Hicri yılın İslam alemine huzur ve barış getirmesini dilerim.",
                    "Yeni yılda yeni umutlar bizimle olsun."
                ],
                "kapanis": ["Hicri Yılbaşınız mübarek olsun.", "Yeni yılımız hayırlı olsun.", "Muharrem ayımız mübarek olsun."]
            },
            "asure_gunu": {
                "ozel": [
                    "Aşurenin bereketi sofralarımızdan, ağzımızın tadı yuvamızdan eksik olmasın.",
                    "Birlik ve beraberliğimizin simgesi olan bu günde kardeşliğimiz daim olsun."
                ],
                "kapanis": ["Aşure Gününüz mübarek olsun.", "Aşuremiz bereketli olsun.", "Hayırlı günler dilerim."]
            }
        }

    def _generate_single_message(self, category: str) -> str:
        cat_data = self.KATEGORILER[category]
        
        # 1: Sadece Dua + Kapanış (Çok genel ve kısa)
        # 2: Özel Anlam + Kapanış
        # 3: Dua + Özel Anlam + Kapanış
        # 4: Özel Anlam + Dua + Kapanış (Hitap yerine yerleri değişen dinamik yapı)
        yapi = random.choice([1, 2, 3, 4])
        
        ozel = random.choice(cat_data["ozel"])
        kapanis = random.choice(cat_data["kapanis"])
        
        # Bazen 1 dua, bazen 2 duayı birleştir (Hitap silindiği için ihtimali yüksek tutar)
        secilen_dualar = random.sample(self.KISA_DUALAR, k=random.choice([1, 2]))
        dua = " ".join(secilen_dualar)
        
        if yapi == 1:
            mesaj = f"{dua} {kapanis}"
        elif yapi == 2:
            mesaj = f"{ozel} {kapanis}"
        elif yapi == 3:
            mesaj = f"{dua} {ozel} {kapanis}"
        else:
            mesaj = f"{ozel} {dua} {kapanis}"
            
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
                
            if tekrara_dusme_sayaci > 1500: # Güvenli çıkış
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
