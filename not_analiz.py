#!/usr/bin/env python
# not_analiz.py

import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import pathlib
import sys

# ---------- 1. Ayarlar (burayı değiştirin) ---------- #
EXCEL_FILE = "sample_grades.xlsx"  # Projeye koyduğun Excel dosyasının adı
SHEET_NAME = 0              # Sayfa adı veya indeksi
WEIGHTS = {                 # Yüzde cinsinden ağırlıklar (toplamı 100 olsun)
    "Quiz": 20,
    "Odev": 30,
    "Final": 50
}
OUT_FILE = "results.xlsx"   # Oluşacak sonuç dosyası

# ---------- 2. Yardımcı Fonksiyonlar ---------- #
def assign_letter_percentile(scores: pd.Series) -> pd.Series:
    """
    Yüzdelik dilimlere göre atama:
      AA: üst %10
      BA: sonraki %15  → toplam %25
      BB: sonraki %20  → toplam %45
      CB: sonraki %15  → toplam %60
      CC: sonraki %15  → toplam %75
      DC: sonraki %10  → toplam %85
      DD: sonraki %10  → toplam %95
      F : alt %5      → toplam %100
    """
    # Kesme noktaları (kümülatif)
    bins = [0, .10, .25, .45, .60, .75, .85, .95, 1.0]
    labels = ["AA","BA","BB","CB","CC","DC","DD","F"]
    # Negatif skorlarla en yüksek puanlar ilk dilimi (AA) alır
    return pd.qcut(-scores, q=bins, labels=labels, duplicates="drop")


def draw_plots(scores: pd.Series, prefix: str):
    plt.figure(figsize=(6,4))
    plt.hist(scores, bins=10, edgecolor="black")
    plt.title("Ağırlıklı Ortalama Dağılımı")
    plt.xlabel("Puan")
    plt.ylabel("Frekans")
    plt.tight_layout()
    plt.savefig(f"{prefix}_hist.png")
    plt.close()

    plt.figure(figsize=(4,6))
    plt.boxplot(scores, vert=True, showfliers=False)
    plt.ylabel("Puan")
    plt.title("Not Boxplot")
    plt.tight_layout()
    plt.savefig(f"{prefix}_box.png")
    plt.close()

# ---------- 3. Ana Akış ---------- #
def main():
    # Excel’i oku
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
    except Exception as e:
        sys.exit(f"Excel okunamadı: {e}")

    # Ağırlıkları normalize et (oran yap)
    w = {col: pct/100 for col, pct in WEIGHTS.items()}
    missing = set(w) - set(df.columns)
    if missing:
        sys.exit(f"Excel'de eksik sütun(lar): {', '.join(missing)}")

    # Ağırlıklı ortalama
    df["Ortalama"] = sum(df[col] * wt for col, wt in w.items())

    # Z-skor (isteğe bağlı)
    df["z"] = stats.zscore(df["Ortalama"])

    # Harf notu
    df["Harf"] = assign_letter_percentile(df["Ortalama"])

    # Sıralama
    df.sort_values("Ortalama", ascending=False, inplace=True, ignore_index=True)

    # Grafikler
    prefix = pathlib.Path(OUT_FILE).stem
    draw_plots(df["Ortalama"], prefix)

    # Sonucu yaz
    df.to_excel(OUT_FILE, index=False)
    print(f"✅ Sonuç: {OUT_FILE}")
    print(f"📊 Grafikler: {prefix}_hist.png, {prefix}_box.png")

if __name__ == "__main__":
    main()
