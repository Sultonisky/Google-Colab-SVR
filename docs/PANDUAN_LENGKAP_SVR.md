# 📘 Panduan Lengkap Program Manual SVR

## 📋 Daftar Isi
1. [Pengenalan](#pengenalan)
2. [Instalasi](#instalasi)
3. [Cara Menggunakan (Manual SVR)](#cara-menggunakan-manual-svr)
4. [Penjelasan Perhitungan SVR](#penjelasan-perhitungan-svr)
5. [Analisis Gap `prediksi_svr` vs `X`](#analisis-gap-prediksi_svr-vs-x)
6. [Output yang Dihasilkan](#output-yang-dihasilkan)
7. [Troubleshooting](#troubleshooting)
8. [Checklist](#checklist)

---

## 🎯 Pengenalan
Mode ini hanya menghitung SVR linear secara manual (kolom `X`) dan membuat file gap antara `prediksi_svr` (Excel) dan `X` (program). Tidak ada forecasting masa depan.

### Fitur Utama
- Perhitungan manual SVR: `y = w1 × rooms_sold + w2 × rooms_available + b`
- Gap `prediksi_svr` (Excel) vs `X` (program) dengan toleransi noise
- Auto-detect kolom (bisa override manual)
- Output rapi: dataset & gap di `result/dataset`, gambar (jika visualisasi diaktifkan) di `result/img`

---

## 💻 Instalasi
```bash
pip install -r programs/require/requirements.txt
```

Dataset:
- `dataset/dataset_bali_2017_2025.xlsx`
- `dataset/dataset_lombok_2017_2025.xlsx`

Kolom wajib/sinonim: `rooms_sold`, `rooms_available`; kolom `prediksi_svr` dibutuhkan untuk analisis gap.

---

## 🚀 Cara Menggunakan (Manual SVR)
```bash
cd C:\PY\forecasting
# Bali
python programs\SVR_Manual_Bali.py
# Lombok
python programs\SVR_Manual_Lombok.py
```

Alur:
1) Load dataset (sheet pertama).  
2) Auto-detect `rooms_sold` / `rooms_available` (bisa set manual).  
3) Hitung kolom `X` dengan rumus manual.  
4) Tampilkan step-by-step 10 baris pertama.  
5) Simpan dataset+X ke `result/dataset/dataset_...with_svr_*.xlsx`.  
6) Simpan gap `prediksi_svr` vs `X` ke `result/dataset/gap_prediksi_svr_vs_X_*.xlsx`.  

Opsional (jika mau visualisasi historis): aktifkan pipeline `prepare_features → split_data → scale_data → train_model → evaluate_model → visualize_results`. Gambar ke `result/img/`.

---

## 📊 Penjelasan Perhitungan SVR
Formula:
```
y = w1 × rooms_sold + w2 × rooms_available + b
```
Default: `w1=0.01152`, `w2=-0.000843`, `b=0.02091`.

Interpretasi:
- w1 positif: rooms_sold naik → prediksi naik.
- w2 negatif: rooms_available naik → prediksi turun.
- b: baseline saat fitur = 0.

Contoh (rooms_sold=2, rooms_available=43):
```
X = 0.01152*2 + (-0.000843)*43 + 0.02091
  = 0.02304 - 0.036249 + 0.02091
  = 0.007701
```

---

## 📈 Analisis Gap `prediksi_svr` vs `X`
```
Gap      = X - prediksi_svr
Gap_abs  = |Gap|
Gap_pct  = (Gap / prediksi_svr) × 100   (jika prediksi_svr ≠ 0)
```
Toleransi kecil di-0-kan untuk menghilangkan noise floating point.

Interpretasi:
- Gap > 0: nilai program (X) lebih besar dari prediksi Excel.
- Gap < 0: nilai program (X) lebih kecil.
- Gap_pct memberi konteks relatif; hati-hati jika denominator kecil.

---

## 📁 Output yang Dihasilkan
- `result/dataset/dataset_bali_with_svr_*.xlsx`  
- `result/dataset/dataset_lombok_with_svr_*.xlsx`  
- `result/dataset/gap_prediksi_svr_vs_X_bali.xlsx`  
- `result/dataset/gap_prediksi_svr_vs_X_lombok.xlsx`  
- (Opsional, jika visualisasi diaktifkan) `result/img/SVR_Manual_Bali_results.png`, `result/img/SVR_Manual_Lombok_results.png`

---

## 🔧 Troubleshooting
- Kolom tidak ditemukan: pastikan ada `rooms_sold` / `rooms_available`; bisa set manual di argumen.
- Permission denied saat simpan Excel: tutup file yang terbuka; fallback nama bertimestamp.
- ModuleNotFoundError: `pip install -r programs/require/requirements.txt`.

---

## ✅ Checklist
- [x] Perhitungan manual SVR (kolom `X`)
- [x] Auto-detect kolom / manual override
- [x] Step-by-step 10 baris pertama
- [x] Analisis gap `prediksi_svr` vs `X`
- [x] Simpan hasil ke `result/dataset`
- [x] Error handling kolom & permission
- [ ] (Opsional) Latih model & visualisasi historis → `result/img`

