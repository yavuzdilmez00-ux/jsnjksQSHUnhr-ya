name: Yapay Zeka Kutsal Mekan Botu

on:
  schedule:
    - cron: '0 7 * * *' # Her sabah Türkiye saati ile 10:00 civarı (UTC 07:00) çalışır
  workflow_dispatch: # Senin elle istediğin zaman çalıştırman için buton

jobs:
  ai-cizim-ve-kaydet:
    runs-on: ubuntu-latest
    permissions:
      contents: write # Botun depoya resim yükleyebilmesi için zorunlu izin

    steps:
      - name: Depoyu Çek
        uses: actions/checkout@v3

      - name: Python Kur
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Gerekli Kütüphaneyi Yükle
        run: pip install requests

      - name: Yapay Zeka Çizim Kodunu Çalıştır
        # Uyarı: Depondaki python dosyasının adının 'yapay_zeka_cizer.py' olduğundan emin ol
        run: python yapay_zeka_cizer.py

      - name: Çizilen Görseli Github'a Pushla
        run: |
          git config --global user.name 'github-actions[bot]'
          git config --global user.email 'github-actions[bot]@users.noreply.github.com'
          git add .
          git commit -m "🕌 AI Bot: Yepyeni bir kutsal mekan görseli çizildi ve eklendi" || exit 0
          git pull --rebase origin main
          git push
