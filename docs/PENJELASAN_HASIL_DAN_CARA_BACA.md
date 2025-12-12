# 📊 Penjelasan Hasil dan Cara Membaca Output (Manual SVR)

Mode ini hanya perhitungan manual SVR dan gap `prediksi_svr` vs `X`. Tidak ada forecasting masa depan.

## 📁 File Excel

### 1) `result/dataset/dataset_bali_with_svr_*.xlsx` (dan lombok)
- Dataset asli + kolom `X` (hasil perhitungan manual SVR).
- Rumus: `X = w1 * rooms_sold + w2 * rooms_available + b` (default w1=0.01152, w2=-0.000843, b=0.02091).
- Bisa dibandingkan dengan kolom `occupancy_rate` atau metrik lain untuk evaluasi internal.

### 2) `result/dataset/gap_prediksi_svr_vs_X_*.xlsx`
- Gap antara `prediksi_svr` (dari Excel) dan `X` (hasil program).
- Kolom:
  - `prediksi_svr`
  - `X`
  - `Gap` = X - prediksi_svr
  - `Gap_Absolute` = |Gap|
  - `Gap_Percentage` = (Gap / prediksi_svr) × 100 (jika prediksi_svr ≠ 0)
- Toleransi kecil di-0-kan untuk menghilangkan noise float.
- Interpretasi:
  - Gap > 0: nilai program lebih besar.
  - Gap < 0: nilai program lebih kecil.
  - Persentase membantu melihat skala relatif (waspada bila denominator kecil).

## 🖼️ File Gambar (opsional)
Jika pipeline pelatihan/visualisasi historis diaktifkan:
- `result/img/SVR_Manual_Bali_results.png`
- `result/img/SVR_Manual_Lombok_results.png`

Isi grafik: actual vs predicted (train/test) dan scatter; berguna jika Anda melatih model historis (bukan forecasting masa depan).

## 🖥️ Console Output (utama)
- Preview dataset, info, dan deskriptif.
- Step-by-step 10 baris pertama perhitungan manual SVR.
- Ringkasan kolom X (min/max/mean/std).
- Ringkasan gap (min/max/mean/std) dan preview 5 baris.

## Cara Membaca & Interpretasi Singkat
- Kolom `X`: hasil prediksi manual berbasis dua fitur (rooms_sold, rooms_available) plus bias.
- Gap:
  - Positif → X lebih tinggi dari prediksi Excel.
  - Negatif → X lebih rendah dari prediksi Excel.
  - Persentase tinggi bisa terjadi jika `prediksi_svr` mendekati nol.
- Gunakan rounding/toleransi yang sudah disediakan untuk menghindari noise sangat kecil.

## Tips
- Pastikan kolom `prediksi_svr`, `rooms_sold`, `rooms_available` ada atau set manual di argumen fungsi.
- Tutup file Excel sebelum menyimpan untuk menghindari permission error (skrip sudah menyiapkan fallback nama timestamp).

