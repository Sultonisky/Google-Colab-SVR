# Program Perhitungan Manual SVR (Occupancy Rate)

Program Python untuk menghitung nilai SVR linear secara manual dan menyimpan hasilnya ke file Excel (kolom `X`) serta gap vs `prediksi_svr`. Opsional: bisa latihan model & visualisasi historis bila diperlukan.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r programs/require/requirements.txt
```

### 2. Jalankan Program (Manual SVR)

```bash
cd C:\PY\forecasting
# Bali
python programs\SVR_Manual_Bali.py
# Lombok
python programs\SVR_Manual_Lombok.py
```

### 3. Output yang Dihasilkan (default manual-only)

- ✅ `result/dataset/dataset_bali_with_svr_*.xlsx`
- ✅ `result/dataset/dataset_lombok_with_svr_*.xlsx`
- ✅ `result/dataset/gap_prediksi_svr_vs_X_bali.xlsx`
- ✅ `result/dataset/gap_prediksi_svr_vs_X_lombok.xlsx`
- ✅ (Opsional, jika mengaktifkan pelatihan + visualisasi) `result/img/SVR_Manual_Bali_results.png`, `result/img/SVR_Manual_Lombok_results.png`

## 📚 Dokumentasi
Dokumen terdahulu tentang forecasting masa depan sudah tidak digunakan. Mode saat ini adalah perhitungan manual SVR + gap. Jika butuh panduan Colab atau jurnal, silakan ditambahkan kembali sesuai kebutuhan.

## ✨ Fitur Utama

- ✅ Perhitungan manual SVR: `y = w1 × rooms_sold + w2 × rooms_available + b`
- ✅ Gap `prediksi_svr` (Excel) vs `X` (program) dengan toleransi noise
- ✅ Auto-detect kolom (rooms_sold / rooms_available) dengan fallback manual
- ✅ Output rapi ke `result/dataset`; gambar ke `result/img` (jika visualisasi diaktifkan)

## 📋 Requirements

- Python 3.7+
- pandas
- numpy
- scikit-learn
- matplotlib
- openpyxl

## 🔧 Konfigurasi

Parameter SVR manual (default):
```python
w1 = 0.01152      # Bobot untuk rooms_sold
w2 = -0.000843    # Bobot untuk rooms_available
b = 0.02091       # Bias/intercept
```
Jika ingin melatih model dan membuat grafik, aktifkan sendiri pipeline pelatihan (prepare_features → split_data → scale_data → train_model → evaluate_model → visualize_results).

## 📖 Referensi

Formula SVR Linear yang digunakan:

```
y = w1 × rooms_sold + w2 × rooms_available + b
```

**Kernel:** Linear  
**Konfigurasi:** Sesuai referensi

## 🆘 Troubleshooting

- Kolom tidak ditemukan: pastikan ada kolom `rooms_sold` / `rooms_available` (atau sinonim). Bisa set manual di argumen fungsi.
- Permission denied: tutup file Excel tujuan; skrip akan mencoba nama baru bertimestamp.
- ModuleNotFoundError: pastikan `pip install -r programs/require/requirements.txt`.

---

**Catatan:** Mode ini tidak melakukan forecasting masa depan; hanya perhitungan manual SVR + gap. Jika butuh forecasting, tambahkan kembali pipeline terkait secara eksplisit.
