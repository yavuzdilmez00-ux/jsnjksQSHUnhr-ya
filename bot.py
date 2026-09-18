import os
import json
import random
from typing import List

class MessageEngine:
    def __init__(self, output_dir: str = "veriler"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 1. HİTAPLAR (Kısa ve öz)
        self.HITAP = [
            "", "", "", "", "", 
            "Canım dostum,", "Değerli kardeşim,", "Kıymetli ailem,", 
            "Gönül dostlarım,", "Sevdiklerim,", "Canım kardeşim,", 
            "Kıymetli büyüğüm,", "Güzel insan,"
        ]

        # 2. KISA DUALAR (Genişletilmiş Havuz)
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
            "Yüzünüzden gülümseme hiç eksik olmasın.", "Dualarınız makbul, gününüz güzel geçsin."
        ]

        # 3. KATEGORİLER (Genişletilmiş)
        self.KATEGORILER = {
            "cuma": {
                "ozel": [
                    "Mübarek Cuma gününün rahmeti üzerinize olsun.",
                    "Haftanın en güzel gününde dualarda buluşalım.",
                    "Cuma vaktinin feyzi hanenize dolsun.",
                    "Af kapılarının açıldığı bu mübarek günde dualarımız bir olsun."
                ],
                "kapanis": ["Hayırlı Cumalar.", "Cumanız mübarek olsun.", "Nurlu Cumalar.", "Bereketli Cumalar dilerim.", "Selam ve dua ile hayırlı Cumalar."]
            },
            "ramazan_ayi": {
                "ozel": [
                    "On bir ayın sultanının bereketi üzerinize olsun.",
                    "Rahmet ayında kalplerimiz imanla, sofralarımız bereketle dolsun.",
                    "Oruçlarınız ve ibadetleriniz makbul olsun.",
                    "Ramazan'ın huzuru tüm hanenizi sarsın."
                ],
                "kapanis": ["Hayırlı Ramazanlar.", "Ramazan ayınız mübarek olsun.", "Bereketli iftarlar.", "Hayırlı sahurlar.", "Ramazan-ı Şerifiniz mübarek olsun."]
            },
            "ramazan_bayrami": {
                "ozel": [
                    "Küslerin barıştığı, sevginin çoğaldığı bu mübarek günde mutluluk sizinle olsun.",
                    "Şeker tadında, neşe dolu bir bayram geçirmeniz dileğiyle.",
                    "Bayram sabahının neşesi kalbinize dolsun."
                ],
                "kapanis": ["İyi bayramlar.", "Hayırlı bayramlar.", "Ramazan Bayramınız mübarek olsun.", "Mutlu bayramlar dilerim."]
            },
            "kurban_bayrami": {
                "ozel": [
                    "Paylaşmanın ve teslimiyetin bayramında tüm dualarınız kabul olsun.",
                    "Kestiğiniz kurbanlar, ettiğiniz niyetler makbul olsun.",
                    "Kardeşliğin pekiştiği bu bayramda yüzünüz hep gülsün."
                ],
                "kapanis": ["Kurban Bayramınız mübarek olsun.", "İyi bayramlar.", "Hayırlı ve bereketli bayramlar.", "Bayramınız mübarek olsun."]
            },
            "mevlid_kandili": {
                "ozel": [
                    "Peygamber Efendimizin (s.a.v) şefaati üzerinize olsun.",
                    "Bu kutlu gecede O'nun (s.a.v) nuru kalbinizi aydınlatsın."
                ],
                "kapanis": ["Hayırlı kandiller.", "Mevlid Kandiliniz mübarek olsun.", "Dualarda buluşmak dileğiyle, hayırlı kandiller."]
            },
            "regaip_kandili": {
                "ozel": [
                    "Üç ayların müjdecisi olan bu gecede rahmet sağanak sağanak yağsın.",
                    "Regaip gecesinin feyzi ve bereketi hanenizi kuşatsın."
                ],
                "kapanis": ["Hayırlı kandiller.", "Regaip Kandiliniz mübarek olsun.", "Üç aylarımız mübarek olsun."]
            },
            "mirac_kandili": {
                "ozel": [
                    "Mucizelerle dolu bu gecede dualarınız gökyüzüne ulaşsın.",
                    "Miracın manevi huzuru yüreklerinize dolsun."
                ],
                "kapanis": ["Hayırlı kandiller.", "Miraç Kandiliniz mübarek olsun.", "Dualarla, hayırlı kandiller."]
            },
            "berat_kandili": {
                "ozel": [
                    "Günahların affedildiği bu gecede beratını alanlardan olmanız dileğiyle.",
                    "İlahi rahmetin tecelli ettiği bu mübarek vakitte dualarınız kabul olsun."
                ],
                "kapanis": ["Hayırlı kandiller.", "Berat Kandiliniz mübarek olsun.", "Berat geceniz hayırlara vesile olsun."]
            },
            "kadir_gecesi": {
                "ozel": [
                    "Bin aydan hayırlı olan bu gecede melekler dualarınıza amin desin.",
                    "Kadir Gecesi'nin nuru tüm hayatınızı aydınlatsın."
                ],
                "kapanis": ["Kadir Geceniz mübarek olsun.", "Hayırlı kandiller.", "Dualarınız kabul, geceniz mübarek olsun."]
            },
            "hicri_yilbasi": {
                "ozel": [
                    "Yeni Hicri yılın İslam alemine huzur ve barış getirmesini dilerim.",
                    "Yeni yılda yeni umutlar sizinle olsun."
                ],
                "kapanis": ["Hicri Yılbaşınız mübarek olsun.", "Yeni yılınız hayırlı olsun.", "Muharrem ayınız mübarek olsun."]
            },
            "asure_gunu": {
                "ozel": [
                    "Aşurenin bereketi sofranızdan, ağzınızın tadı yuvanızdan eksik olmasın.",
                    "Birlik ve beraberliğimizin simgesi olan bu günde kardeşliğimiz daim olsun."
                ],
                "kapanis": ["Aşure Gününüz mübarek olsun.", "Aşureniz bereketli olsun.", "Hayırlı günler dilerim."]
            }
        }

    def _generate_single_message(self, category: str) -> str:
        cat_data = self.KATEGORILER[category]
        yapi = random.choice([1, 2, 3, 4])
        
        hitap = random.choice(self.HITAP)
        ozel = random.choice(cat_data["ozel"])
        kapanis = random.choice(cat_data["kapanis"])
        
        # MUCİZE FORMÜL: Bazen 1 dua, bazen 2 duayı birleştirir (İhtimali 15.000'e katlar)
        secilen_dualar = random.sample(self.KISA_DUALAR, k=random.choice([1, 2]))
        dua = " ".join(secilen_dualar)
        
        if yapi == 1:
            mesaj = f"{dua} {kapanis}"
        elif yapi == 2:
            mesaj = f"{ozel} {kapanis}"
        elif yapi == 3:
            mesaj = f"{dua} {ozel} {kapanis}"
        else:
            mesaj = f"{hitap} {ozel} {dua} {kapanis}"
            
        return " ".join(mesaj.split())

    def generate_unique_batch(self, category: str, count: int) -> List[str]:
        if category not in self.KATEGORILER:
            return []

        generated = set()
        deneme = 0
        maks_deneme = count * 20 # Sonsuz döngüden korur
        onceki_uzunluk = 0
        tekrara_dusme_sayaci = 0

        while len(generated) < count and deneme < maks_deneme:
            yeni_mesaj = self._generate_single_message(category)
            generated.add(yeni_mesaj)
            
            # Eğer yeni mesaj bulamayıp takılırsa güvenli çıkış yapar
            if len(generated) == onceki_uzunluk:
                tekrara_dusme_sayaci += 1
            else:
                tekrara_dusme_sayaci = 0
                onceki_uzunluk = len(generated)
                
            if tekrara_dusme_sayaci > 1000:
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

    # HER ÇALIŞTIĞINDA 11 KATEGORİNİN HER BİRİ İÇİN 1000'ER MESAJ ÜRETİR! (Toplam 11.000)
    for gun in dini_gunler:
        yeni_mesajlar = engine.generate_unique_batch(category=gun, count=1000)
        engine.save_to_json(category=gun, new_messages=yeni_mesajlar)
