# Python Not Analiz Aracı

Bu proje, **Excel** formatındaki öğrenci notlarını alıp:
- Ağırlıklı ortalama hesaplar
- Z-skor ekler
- Artan ortalamaya göre sıralar
- AA–F arası yüzdelik dilimlere göre curve (percentile grading) uygular
- Histogram ve boxplot oluşturur
- Sonuçları yeni bir Excel dosyasına ve grafiklere kaydeder

---

## 📦 Kurulum

1. Depoyu klonla veya indir:
   git clone <repo-url>
   cd not-analiz-araci
2. (Opsiyonel) Sanal ortam oluştur ve aktif et:
   python -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate       # Windows
3. Gerekli paketleri yükle:
   pip install -r requirements.txt

---

## ⚙️ Kullanım

1. sample_grades.xlsx dosyasını proje köküne koy.
2. not_analiz.py içindeki AYARLAR bölümünü kendine göre düzenle:
   EXCEL_FILE = "sample_grades.xlsx"
   SHEET_NAME = 0
   WEIGHTS = {
     "Quiz": 20,
     "Odev": 30,
     "Final": 50
   }
   OUT_FILE = "results.xlsx"
3. Script’i çalıştır:
   python not_analiz.py

---

Oluşacak dosyalar:
- results.xlsx  – Ortalama, z-skor, harf notu ve sıralı tablo
- results_hist.png  – Dağılım histogramı
- results_box.png   – Boxplot

---

## 🛠️ Özelleştirme

- Ağırlıklar: WEIGHTS sözlüğünü % cinsinden güncelleyin.
- Kurve Dilimleri: assign_letter_percentile fonksiyonundaki bins / labels’ı değiştirin.
- Sheet Adı: Farklı sayfa için SHEET_NAME’i güncelleyin.
- Grafikleri özelleştirme: draw_plots fonksiyonundaki matplotlib ayarlarını düzenleyin.

---

## 📄 Lisans

MIT © [Serhat Memiş]
