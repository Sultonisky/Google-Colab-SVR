# 📘 Panduan Singkat (Versi Mudah) — Program Manual SVR

Dokumen ini adalah versi **lebih sederhana** dari `docs/PANDUAN_LENGKAP_SVR.md`. Targetnya: **orang awam pun bisa mengikuti** tanpa perlu paham machine learning.

---

## 🎯 Program ini buat apa?
Program ini menghitung **nilai indikator** bernama kolom `X` memakai rumus:

\[
X = (w1 \times rooms\_sold) + (w2 \times rooms\_available) + b
\]

Nilai `X` ini membantu melihat **“kinerja”** berdasarkan:
- berapa kamar yang **terjual** (`rooms_sold`)
- berapa kamar yang **masih tersedia/kosong** (`rooms_available`)

**Penting:** program ini **bukan** “forecast masa depan”. Program ini hanya menghitung `X` dari data yang sudah ada di Excel.

---

## ✅ Yang Anda butuhkan
- Python terinstal (disarankan Python 3.10+)
- File dataset Excel:
  - `dataset/dataset_bali_2017_2025.xlsx` (untuk Bali)
  - `dataset/dataset_lombok_2017_2025.xlsx` (untuk Lombok)

Kolom minimal yang harus ada (nama boleh berbeda, program akan coba deteksi):
- `rooms_sold` (kamar terjual)
- `rooms_available` (kamar tersedia / belum terjual)

---

## 💻 Instalasi (sekali saja)
Buka PowerShell / CMD, lalu jalankan:

```bash
cd C:\PY\forecasting
pip install -r programs/require/requirements.txt
```

Kalau Anda tidak pakai `requirements.txt`, bisa install manual:

```bash
pip install pandas numpy scikit-learn matplotlib openpyxl
```

---

## 🚀 Cara menjalankan program
Masih di folder project:

```bash
cd C:\PY\forecasting
# Bali
python programs\SVR_Manual_Bali.py
# Lombok
python programs\SVR_Manual_Lombok.py
```

Setelah jalan, program akan:
- membaca file Excel
- mendeteksi kolom `rooms_sold` dan `rooms_available`
- menghitung kolom baru `X` menggunakan rumus: `X = w1 × rooms_sold + w2 × rooms_available + b`
  - Parameter default: `w1=0.01152`, `w2=-0.000843`, `b=0.02091`
- menampilkan contoh perhitungan (beberapa baris pertama)
- membuat gambar visualisasi
- menyimpan hasil Excel baru

**Catatan:** Program ini menggunakan parameter yang sudah dioptimasi sebelumnya. Jika Anda ingin mendapatkan parameter sendiri, lihat bagian [Bagaimana Cara Mendapatkan Parameter w1, w2, b Sendiri?](#-bagaimana-cara-mendapatkan-parameter-w1-w2-b-sendiri-opsional) di bawah.

---

## 📦 Output (hasilnya ada di mana?)
Program akan membuat folder (kalau belum ada) dan menyimpan:

- **Excel hasil**: `result/dataset/dataset_*_with_svr_YYYYMMDD_HHMMSS.xlsx`  
  (dataset asli + kolom baru `X`)
- **Gambar visualisasi**: `result/img/SVR_Manual_*_visualization.png`

---

## 🧾 Penjelasan kolom penting (bahasa sederhana)
- **`rooms_sold`**: jumlah kamar yang berhasil terjual/terisi.
- **`rooms_available`**: jumlah kamar yang masih tersedia/kosong.
- **`X`**: nilai indikator hasil rumus SVR manual.

Secara logika:
- kalau `rooms_sold` naik → biasanya `X` **naik** (karena `w1` positif)
- kalau `rooms_available` naik → biasanya `X` **turun** (karena `w2` negatif)

---

## 🔑 Angka w1, w2, b itu apa?
Program punya nilai default:
- `w1 = 0.01152`
- `w2 = -0.000843`
- `b  = 0.02091`

Artinya sederhana:
- **`w1` (positif)**: “seberapa kuat pengaruh kamar terjual” ke `X`.  
  Setiap 1 kamar terjual menambah `X` sekitar **0.01152**.
- **`w2` (negatif)**: “seberapa kuat pengaruh kamar kosong” ke `X`.  
  Setiap 1 kamar kosong mengurangi `X` sekitar **0.000843**.
- **`b` (konstan)**: “nilai dasar” yang selalu ditambahkan.

**Dari mana angka ini?**  
Angka ini berasal dari proses **training SVR linear** sebelumnya pada data historis (jadi sudah "disiapkan" untuk dipakai).

---

## 🔧 Bagaimana Cara Mendapatkan Parameter w1, w2, b Sendiri? (Opsional)

Jika Anda ingin mendapatkan parameter `w1`, `w2`, `b` sendiri dari data Anda, Anda bisa melakukan **training model SVR**. Berikut contoh kode yang sinkron dengan program:

### 1️⃣ Persiapan Data dan Split Training/Testing

Program membagi data menjadi dua bagian:
- **Data Training** (80%): untuk "belajar" pola
- **Data Testing** (20%): untuk "uji" apakah model sudah bagus

```python
from programs.SVR_Manual_Bali import SVRForecasting

# Load data
forecaster = SVRForecasting('dataset/dataset_bali_2017_2025.xlsx')
forecaster.load_data(sheet_name=0)

# Siapkan fitur dan target
# Misalnya: fitur = rooms_sold & rooms_available, target = occupancy_rate
forecaster.prepare_features(
    target_column='occupancy_rate',  # kolom yang ingin diprediksi
    feature_columns=['rooms_sold', 'rooms_available'],
    lag_periods=None  # tidak pakai lag, langsung pakai kolom
)

# Bagi data: 80% training, 20% testing
forecaster.split_data(test_size=0.2, random_state=42)
```

**Penjelasan sederhana:**
- `test_size=0.2` artinya 20% data dipakai untuk testing (sisanya 80% untuk training)
- `random_state=42` artinya hasilnya akan sama setiap kali dijalankan (untuk konsistensi)

### 2️⃣ Scaling/Normalisasi Data

Sebelum training, data biasanya di-scale agar semua kolom punya skala yang mirip:

```python
# Normalisasi data (scaling)
forecaster.scale_data()
```

**Kenapa perlu scaling?**
- Kolom `rooms_sold` mungkin punya nilai ratusan (misal: 150)
- Kolom `rooms_available` mungkin punya nilai puluhan (misal: 50)
- Scaling membuat keduanya punya skala yang mirip, sehingga model lebih mudah belajar

### 3️⃣ Training Model dengan Parameter Epsilon dan C

Setelah data siap, kita bisa training model SVR:

```python
# Training model SVR dengan kernel LINEAR
forecaster.train_model(
    kernel='linear',    # pakai kernel linear (agar dapat w1, w2, b yang jelas)
    C=100,             # parameter regularisasi (semakin besar, semakin "ketat")
    gamma='scale',     # parameter kernel (untuk linear tidak terlalu penting)
    epsilon=0.1        # toleransi error (semakin kecil, semakin teliti)
)
```

**Penjelasan parameter:**

| Parameter | Nilai Default | Arti Sederhana |
|-----------|---------------|----------------|
| **`kernel='linear'`** | `'linear'` | Pakai rumus linear (agar dapat w1, w2, b yang jelas) |
| **`C=100`** | `100` | Seberapa "ketat" model (semakin besar = semakin detail, tapi bisa overfit) |
| **`epsilon=0.1`** | `0.1` | Toleransi error (semakin kecil = semakin teliti, tapi lebih kompleks) |
| **`gamma='scale'`** | `'scale'` | Parameter kernel (untuk linear tidak terlalu penting) |

**Epsilon (`epsilon=0.1`):**
- Ini adalah "tabung toleransi" untuk error
- Jika prediksi beda dengan aktual kurang dari `0.1`, dianggap "tidak error"
- Semakin kecil epsilon → model lebih teliti tapi lebih kompleks
- Semakin besar epsilon → model lebih "toleran" tapi mungkin kurang akurat

**C (Regularization):**
- Mengontrol keseimbangan antara "akurasi" dan "kesederhanaan"
- C besar (misal: 1000) → model lebih detail, tapi bisa overfit
- C kecil (misal: 0.1) → model lebih sederhana, tapi mungkin kurang akurat
- Default `C=100` adalah nilai yang cukup seimbang

### 4️⃣ Ekstrak Parameter w1, w2, b dari Model

Setelah training selesai, kita bisa ambil parameter dari model:

```python
# Ekstrak parameter dari model yang sudah dilatih
model = forecaster.model

if hasattr(model, 'coef_') and hasattr(model, 'intercept_'):
    # Untuk SVR linear, koefisien tersimpan di coef_ dan intercept_
    w1_trained = model.coef_[0][0]  # koefisien untuk rooms_sold
    w2_trained = model.coef_[0][1]  # koefisien untuk rooms_available
    b_trained = model.intercept_[0]  # bias/intercept
    
    print(f"Parameter hasil training:")
    print(f"w1 (rooms_sold)     = {w1_trained:.6f}")
    print(f"w2 (rooms_available) = {w2_trained:.6f}")
    print(f"b (bias)             = {b_trained:.6f}")
```

**Catatan penting:**
- Parameter di atas adalah pada **data yang sudah di-scale**
- Untuk mendapatkan parameter pada data asli (unscaled), ada dua cara:
  1. **Training tanpa scaling** (lebih mudah untuk interpretasi)
  2. **Transformasi manual** dari scaled ke unscaled (lebih kompleks)

### 5️⃣ Evaluasi Model (Opsional)

Untuk melihat seberapa bagus model yang sudah dilatih:

```python
# Evaluasi model
eval_results = forecaster.evaluate_model()

# Hasil evaluasi akan menampilkan:
# - MSE (Mean Squared Error): semakin kecil semakin baik
# - RMSE (Root Mean Squared Error): akar dari MSE
# - MAE (Mean Absolute Error): rata-rata selisih absolut
# - R² Score: semakin mendekati 1 semakin baik (0-1)
```

### 📝 Contoh Lengkap: Training untuk Dapat Parameter Baru

Berikut contoh lengkap jika Anda ingin training sendiri:

```python
from programs.SVR_Manual_Bali import SVRForecasting
from pathlib import Path

# 1. Setup
base_dir = Path(__file__).resolve().parent
file_path = base_dir / 'dataset' / 'dataset_bali_2017_2025.xlsx'

# 2. Load data
forecaster = SVRForecasting(file_path)
forecaster.load_data(sheet_name=0)

# 3. Siapkan fitur dan target
# Asumsi: ada kolom 'occupancy_rate' sebagai target
forecaster.prepare_features(
    target_column='occupancy_rate',
    feature_columns=['rooms_sold', 'rooms_available'],
    lag_periods=None
)

# 4. Bagi data (80% training, 20% testing)
forecaster.split_data(test_size=0.2, random_state=42)

# 5. Scaling data
forecaster.scale_data()

# 6. Training dengan parameter default
forecaster.train_model(
    kernel='linear',
    C=100,
    epsilon=0.1,
    gamma='scale'
)

# 7. Evaluasi
eval_results = forecaster.evaluate_model()

# 8. Ambil parameter
model = forecaster.model
w1 = model.coef_[0][0]
w2 = model.coef_[0][1]
b = model.intercept_[0]

print(f"\nParameter baru:")
print(f"w1 = {w1:.6f}")
print(f"w2 = {w2:.6f}")
print(f"b  = {b:.6f}")

# 9. Gunakan parameter baru untuk perhitungan manual
forecaster.calculate_manual_svr(
    w1=w1, w2=w2, b=b,
    output_col='X',
    n_rows=10
)
```

### ⚠️ Catatan Penting

1. **Training membutuhkan kolom target**: Anda perlu punya kolom yang ingin diprediksi (misal: `occupancy_rate`)
2. **Parameter scaled vs unscaled**: Parameter dari training dengan scaling berbeda dengan yang tanpa scaling
3. **Default sudah cukup baik**: Parameter default (`w1=0.01152`, `w2=-0.000843`, `b=0.02091`) sudah dioptimasi sebelumnya, jadi biasanya tidak perlu retrain kecuali ada perubahan signifikan pada data

---

## 🧮 Contoh hitung (biar kebayang)
Misal:
- `rooms_sold = 156`
- `rooms_available = 44`

Maka:
- kontribusi sold = `0.01152 × 156 = 1.79712`
- kontribusi available = `-0.000843 × 44 = -0.037092`
- tambah bias = `+ 0.02091`

Hasil:
\[
X = 1.79712 - 0.037092 + 0.02091 = 1.780938
\]

---

## 📊 Cara membaca nilai X (interpretasi praktis)
Ini patokan sederhana agar mudah dipahami:

| Nilai X | Makna sederhana |
|--------:|------------------|
| **X > 1.5** | Performa **sangat baik** (banyak terjual, sedikit kosong) |
| **1.0 < X ≤ 1.5** | Performa **baik** |
| **0.5 < X ≤ 1.0** | Performa **cukup** (perlu evaluasi) |
| **0.1 < X ≤ 0.5** | Performa **kurang** (banyak kamar kosong) |
| **X ≤ 0.1** | Performa **sangat kurang** |

**Catatan:** ini interpretasi praktis untuk “membaca indikator”. Bukan standar baku industri.

---

## 🖼️ Apa isi gambar visualisasi?
Di `result/img/...png` umumnya ada:
- **Time series**: nilai `X` dari waktu ke waktu (lihat tren naik/turun).
- **Histogram**: sebaran nilai `X` (seringnya nilai ada di rentang berapa).
- **Scatter rooms_sold vs X**: harusnya cenderung naik.
- **Scatter rooms_available vs X**: harusnya cenderung turun.

---

## 🧯 Troubleshooting (masalah yang paling sering)

### 1) Kolom tidak ditemukan
Gejala: error seperti “Column 'rooms_sold' not found”.

Solusi:
- Pastikan di Excel ada kolom setara `rooms_sold` dan `rooms_available`
- Kalau nama kolom Anda berbeda jauh, Anda bisa:
  - ganti nama kolom di Excel agar mirip, atau
  - set manual di code (lihat `PANDUAN_LENGKAP_SVR.md` bagian troubleshooting)

### 2) Gagal menyimpan Excel (Permission denied / file sedang dibuka)
Solusi:
- tutup file Excel hasil sebelumnya yang sedang terbuka
- jalankan ulang program

### 3) `ModuleNotFoundError` (misal: pandas belum ada)
Solusi:

```bash
pip install -r programs/require/requirements.txt
```

---

## ❓ FAQ singkat

### Apakah ini memprediksi bulan depan?
Tidak. Ini hanya menghitung `X` dari data yang Anda berikan.

### Kenapa nilai X bisa lebih dari 1?
Karena `X` adalah hasil rumus linear, bukan persentase. Angkanya tergantung skala data dan parameter.

### Kalau dataset saya berbeda (kolom/daerah lain), bisa?
Bisa, tapi mungkin Anda perlu:
- memastikan kolom `rooms_sold` & `rooms_available` benar, dan/atau
- melakukan training ulang untuk dapat `w1`, `w2`, `b` yang lebih cocok.

---

## ✅ Ringkasan cepat (1 menit)
- Jalankan: `python programs\SVR_Manual_Bali.py` atau `SVR_Manual_Lombok.py`
- Lihat hasil: `result/dataset/...with_svr...xlsx` (kolom `X` bertambah)
- Lihat grafik: `result/img/...png`
- Makna `X`: indikator performa dari kombinasi kamar terjual & kamar kosong


