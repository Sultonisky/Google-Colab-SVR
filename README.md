# Program Manual SVR — Panduan Lengkap Project (Python + Notebook/Colab)

Project ini dibuat supaya Anda bisa **menghitung kolom indikator `X`** dari dataset hotel (Bali/Lombok) menggunakan rumus SVR linear **secara manual** (tanpa forecasting masa depan).

Kalau Anda orang awam, cukup ikuti bagian **Quick Start** dan **Cara Menjalankan (Langkah demi Langkah)**.

---

## 🎯 Yang dilakukan program (bahasa sederhana)
Program akan membaca file Excel (dataset), lalu menghitung kolom baru bernama `X` memakai rumus:

```
X = (w1 × rooms_sold) + (w2 × rooms_available) + b
```

Secara intuisi:
- Jika **kamar terjual** (`rooms_sold`) naik → `X` cenderung **naik**
- Jika **kamar kosong/tersedia** (`rooms_available`) naik → `X` cenderung **turun**

**Catatan penting:** mode utama project ini adalah **perhitungan manual** + **visualisasi hasil `X`**. Ini **bukan** “prediksi bulan depan”.

---

## ✨ Fitur utama
- **Perhitungan manual SVR** dan menambahkan kolom `X` ke dataset.
- **Auto-detect kolom** `rooms_sold` dan `rooms_available` (nama kolom boleh berbeda).
- **Step-by-step** contoh perhitungan untuk beberapa baris pertama (membantu verifikasi).
- **Visualisasi otomatis** (time series, distribusi, scatter) dan disimpan sebagai gambar.
- **Output rapi**: Excel hasil di `result/dataset/`, gambar di `result/img/`.

---

## 🧱 Struktur folder project (wajib tahu)
Struktur ringkas:

```
forecasting/
├─ dataset/
│  ├─ dataset_bali_2017_2025.xlsx
│  ├─ dataset_lombok_2017_2025.xlsx
│  └─ backup/                     # salinan cadangan dataset
├─ programs/
│  ├─ SVR_Manual_Bali.py           # script utama Bali
│  ├─ SVR_Manual_Lombok.py         # script utama Lombok
│  └─ require/requirements.txt     # daftar library Python yang dibutuhkan
├─ result/
│  ├─ dataset/                    # output Excel (hasil)
│  └─ img/                        # output gambar (visualisasi)
├─ docs/                          # dokumentasi (panduan lengkap & singkat)
├─ Manual_SVR_Bali.ipynb          # notebook (bisa dipakai di Colab/Jupyter)
├─ Manual_SVR_Lombok.ipynb
└─ README.md
```

**Penjelasan fungsi folder:**
- **`dataset/`**: tempat file Excel input (data sumber).
- **`programs/`**: tempat script Python yang dijalankan.
- **`result/`**: tempat hasil output otomatis (Excel + gambar).
- **`docs/`**: panduan penggunaan (termasuk Colab).
- **`*.ipynb`**: notebook untuk menjalankan langkah-langkah lewat Jupyter/Google Colab.

---

## 📦 File penting (yang biasanya Anda sentuh)
- **`programs/SVR_Manual_Bali.py`**: jalankan untuk dataset Bali.
- **`programs/SVR_Manual_Lombok.py`**: jalankan untuk dataset Lombok.
- **`dataset/dataset_bali_2017_2025.xlsx`**: input Bali.
- **`dataset/dataset_lombok_2017_2025.xlsx`**: input Lombok.
- **`result/dataset/`**: hasil Excel (ada kolom `X`).
- **`result/img/`**: gambar visualisasi.

---

## ⚙️ Requirements
- Python 3.7+ (disarankan Python 3.10+)
- Library (akan diinstall via requirements): pandas, numpy, scikit-learn, matplotlib, openpyxl

---

## 🚀 Quick Start (Windows)
### 1) Masuk ke folder project
```bash
cd C:\PY\forecasting
```

### 2) Install dependency (sekali saja)
```bash
pip install -r programs/require/requirements.txt
```

### 3) Jalankan program
```bash
# Bali
python programs\SVR_Manual_Bali.py

# Lombok
python programs\SVR_Manual_Lombok.py
```

---

## 🧭 Cara menjalankan program (lebih detail, langkah demi langkah)
### Step A — Pastikan file input ada
Cek file berikut harus ada:
- `dataset/dataset_bali_2017_2025.xlsx` (untuk Bali)
- `dataset/dataset_lombok_2017_2025.xlsx` (untuk Lombok)

### Step B — Pastikan kolom data sesuai
Program membutuhkan dua “angka utama”:
- **`rooms_sold`** = jumlah kamar terjual/terisi
- **`rooms_available`** = jumlah kamar tersedia/kosong

Kalau nama kolom Anda berbeda (misal bahasa Indonesia), program akan coba deteksi otomatis (misal: `jumlah_kamar_terjual`, `kamar_tersedia`, dll).

### Step C — Jalankan script
Contoh untuk Bali:
```bash
python programs\SVR_Manual_Bali.py
```

Saat jalan, Anda akan melihat output di terminal seperti:
- info dataset (preview)
- konfirmasi kolom yang dipakai
- rumus + parameter yang dipakai
- contoh perhitungan baris awal
- ringkasan statistik `X`
- info file output yang tersimpan

---

## 🔑 Parameter SVR manual (default)
Program memakai parameter default:
```python
w1 = 0.01152      # bobot rooms_sold
w2 = -0.000843    # bobot rooms_available
b  = 0.02091      # bias/intercept
```

Rumusnya:
```
X = (w1 × rooms_sold) + (w2 × rooms_available) + b
```

---

## 📤 Output yang dihasilkan (hasilnya ada di mana dan apa isinya?)
### 1) Output dataset (Excel)
File output akan dibuat otomatis di:
- **`result/dataset/`**

Nama file memakai timestamp agar tidak menimpa file lama:
- `result/dataset/dataset_bali_with_svr_YYYYMMDD_HHMMSS.xlsx`
- `result/dataset/dataset_lombok_with_svr_YYYYMMDD_HHMMSS.xlsx`

Isi Excel output:
- dataset asli (kolom-kolom awal tetap)
- **kolom baru `X`** (hasil perhitungan manual SVR)

### 2) Output visualisasi (gambar)
Gambar output dibuat di:
- **`result/img/`**

Nama file:
- `result/img/SVR_Manual_Bali_visualization.png`
- `result/img/SVR_Manual_Lombok_visualization.png`

Isi gambar (4 grafik):
- **Time series `X`**: tren nilai `X` dari waktu ke waktu
- **Histogram `X`**: sebaran nilai `X`
- **Scatter `rooms_sold` vs `X`**: biasanya cenderung naik
- **Scatter `rooms_available` vs `X`**: biasanya cenderung turun

---

## 📓 Menjalankan via Notebook / Google Colab
Kalau tidak ingin setup Python lokal, Anda bisa memakai Colab.

- Panduan lengkap Colab ada di: `docs/PANDUAN_GOOGLE_COLAB.md`
- Notebook siap pakai:
  - `Manual_SVR_Bali.ipynb`
  - `Manual_SVR_Lombok.ipynb`

Ringkas alurnya di Colab:
1. Upload notebook + dataset + `requirements.txt`
2. Install dependency
3. Jalankan cell sampai selesai
4. Download hasil Excel dan gambar dari folder output Colab

---

## 🧠 (Opsional) Melatih model SVR (training/testing split, scaling, dll)
Di dalam script ada pipeline pelatihan yang bisa Anda pakai jika ingin eksperimen:

`prepare_features → split_data → scale_data → train_model → evaluate_model → visualize_results`

Penjelasan dan contoh potongan kode sudah disediakan di:
- `docs/PANDUAN_SINGKAT_SVR.md` (bagian training/testing split, epsilon, C, scaling)
- `docs/PANDUAN_LENGKAP_SVR.md` (versi lebih detail)

---

## 🆘 Troubleshooting (yang paling sering)
### 1) Error: kolom tidak ditemukan
Gejala: `[ERROR] Column 'rooms_sold' not found!` atau `'rooms_available' not found!`

Solusi:
- Pastikan dataset memang punya kolom setara `rooms_sold` dan `rooms_available`
- Kalau namanya jauh berbeda, ubah nama kolom di Excel, atau set manual di kode (lihat komentar di `programs/SVR_Manual_*.py` pada pemanggilan `calculate_manual_svr(...)`)

### 2) Gagal simpan Excel (Permission denied)
Penyebab paling umum: file Excel output sedang terbuka.

Solusi:
- tutup file Excel yang sedang dibuka
- jalankan ulang program (nama file output pakai timestamp)

### 3) `ModuleNotFoundError`
Solusi:
```bash
pip install -r programs/require/requirements.txt
```

---

## ❓ FAQ Singkat (Super Awam)
- **Output Excel tidak muncul?**  
  Pastikan program selesai tanpa error dan folder `result/dataset/` bisa ditulis. Tutup Excel yang sedang terbuka, lalu jalankan ulang.
- **Nama kolom saya beda (bahasa Indonesia), gimana?**  
  Program coba auto-detect. Jika gagal, ubah nama kolom di Excel agar mirip (`rooms_sold`, `rooms_available`) atau set manual di argumen `calculate_manual_svr(...)`.
- **Sheet Excel saya bukan sheet pertama.**  
  Ubah argumen `sheet_name` saat `load_data(...)` di script (misal `sheet_name=1` atau nama sheet).
- **Mau ganti parameter `w1`, `w2`, `b` sendiri.**  
  Bisa langsung isi di `calculate_manual_svr(w1=..., w2=..., b=...)` atau ikuti bagian training di `docs/PANDUAN_SINGKAT_SVR.md`.
- **Bisa jalan di Google Colab?**  
  Bisa. Ikuti `docs/PANDUAN_GOOGLE_COLAB.md` dan gunakan notebook `Manual_SVR_*.ipynb`.
- **Apakah ini memprediksi masa depan?**  
  Tidak. Hanya menghitung kolom indikator `X` dari data yang sudah ada.
- **Gambar tidak muncul?**  
  Cek `result/img/`. Jika kosong, pastikan script jalan sampai bagian visualisasi dan tidak ada error Matplotlib.

---

## 📚 Dokumentasi tambahan
- **Panduan singkat (mudah)**: `docs/PANDUAN_SINGKAT_SVR.md`
- **Panduan lengkap**: `docs/PANDUAN_LENGKAP_SVR.md`
- **Panduan Google Colab**: `docs/PANDUAN_GOOGLE_COLAB.md`
- **Cara baca hasil**: `docs/PENJELASAN_HASIL_DAN_CARA_BACA.md`

---

## 👥 Credits
Kelompok 2 - PT Pembangun Negeri BSI Slipi

1. AMMAD RAIHAN NAFIS (19230222)
2. RIFQI HISYAM FADHILAH (19231794)
3. RAFI AKBAR SULISTYO (19231411)
4. MOHAMMAD SULTONI (19230759)
5. NIHAT HASANNANTO (19231487)
6. RIZKI ERLANGGA (19231987)