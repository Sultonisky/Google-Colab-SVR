# 📓 Panduan Lengkap Google Colab untuk Menjalankan Program Manual SVR

Panduan ini dibuat supaya **orang awam sekalipun** bisa:
- Mengerti **apa itu Google Colab**
- Bisa **membuat notebook baru**
- **Upload file** (script Python & Excel)
- **Menulis kode di cell**
- **Menjalankan cell** dan
- **Membaca output** program manual SVR (kolom `X` dan visualisasi).

Mode program: **hanya perhitungan manual SVR (kolom `X`) dan visualisasi hasil SVR**, tanpa forecasting masa depan.

---

## 1. Apa Itu Google Colab?

- **Google Colab (Colaboratory)** adalah layanan gratis dari Google untuk:
  - Menjalankan **kode Python langsung di browser**
  - Tanpa perlu install Python di laptop
  - Notebook tersimpan di **Google Drive**
- Cocok untuk:
  - Data analysis
  - Machine learning
  - Menjalankan script seperti **program manual SVR** di project ini

Cara mengakses:
- Buka browser (Chrome/Edge/Firefox)
- Kunjungi `https://colab.research.google.com`
- Login pakai akun Google Anda

---

## 2. Cara Membuat Notebook Baru

1. Buka `https://colab.research.google.com`
2. Di pojok kiri atas, pilih **File → New notebook**  
   (atau klik tombol **New Notebook** jika ada)
3. Akan muncul tampilan notebook dengan:
   - Judul default, misalnya `Untitled0.ipynb`
   - Satu cell kosong pertama (tipe: Code)

Opsional:
- Klik judul di kiri atas untuk mengganti nama, misalnya:  
  `SVR_Manual_Bali_Colab.ipynb`

---

## 3. Mengenal Cell: Code vs Text

Di Colab, notebook terdiri dari beberapa **cell**:

- **Code cell**: berisi kode Python yang bisa dijalankan.
- **Text/Markdown cell**: berisi penjelasan, judul, catatan (tidak dieksekusi).

Cara menambah cell:
- Klik ikon **+ Code** untuk menambah cell kode.
- Klik ikon **+ Text** untuk menambah cell teks.

Cara mengubah jenis cell:
- Klik cell → di toolbar atas, pilih **Code** atau **Text**.

---

## 4. Upload File Program & Dataset ke Colab

Agar program SVR bisa berjalan, Anda perlu meng-upload:
- File Python: `SVR_Manual_Bali.py` (dan/atau `SVR_Manual_Lombok.py`)
- File Excel: `dataset_bali_2017_2025.xlsx` (dan/atau `dataset_lombok_2017_2025.xlsx`)

### 4.1. Upload Manual via Sidebar

1. Di sisi kiri Colab, klik ikon **folder** (Files).
2. Klik tombol **Upload** (ikon panah ke atas).
3. Pilih file dari komputer Anda:
   - `SVR_Manual_Bali.py`
   - `dataset_bali_2017_2025.xlsx`
4. Pastikan setelah upload:
   - File muncul di panel kiri di folder `/content`

> Catatan: Jika Anda menutup runtime Colab, file bisa hilang dan perlu di-upload ulang.

---

## 5. Menulis Kode di Cell dan Menjalankannya

### 5.1. Cara Menulis Kode di Cell

1. Klik **+ Code** untuk membuat cell baru.
2. Ketik kode Python di dalam cell, misalnya:

```python
print("Halo dari Colab!")
```

### 5.2. Cara Menjalankan Cell

Ada beberapa cara:
- Klik tombol **▶** (Run) di sisi kiri cell.
- Atau tekan **Shift + Enter** di keyboard.

Jika berhasil:
- Di bawah cell akan muncul **output**:
  - Misalnya: `Halo dari Colab!`

---

## 6. Install Dependency yang Dibutuhkan Program

Program manual SVR membutuhkan beberapa library Python (pandas, numpy, scikit-learn, dll).  
Cara termudah di Colab: jalankan perintah install di **cell pertama**.

**Cell 1 — Install dependencies**

```python
!pip install -r requirements.txt
```

Jika Anda tidak punya `requirements.txt` di Colab:

```python
!pip install pandas numpy scikit-learn matplotlib openpyxl
```

Tunggu sampai proses selesai (tulisan `Successfully installed ...` muncul).

---

## 7. Memastikan File Program SVR Tersedia

Buat satu **code cell** lagi, lalu isi dengan kode berikut untuk mengecek file `SVR_Manual_Bali.py`:

```python
import os
import sys

sys.path.append("/content")  # pastikan /content ada di sys.path

required_py = "SVR_Manual_Bali.py"

print("[INFO] Checking for SVR_Manual_Bali.py...")

if os.path.exists(required_py):
    print("[SUCCESS] SVR_Manual_Bali.py found.")
else:
    print("[WARNING] SVR_Manual_Bali.py not found. Please upload it to Colab (folder /content).")
```

Jalankan cell tersebut:
- Jika file ditemukan, akan muncul pesan **SUCCESS**.
- Jika tidak, ulangi langkah **Upload File** di bagian sebelumnya.

---

## 8. Menjalankan Program Manual SVR (Bali)

Setelah:
- Library ter-install
- File `SVR_Manual_Bali.py` dan `dataset_bali_2017_2025.xlsx` sudah ter-upload

Buat **code cell** baru dan isi:

```python
import importlib.util

spec = importlib.util.spec_from_file_location("SVR_Manual_Bali", "SVR_Manual_Bali.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

SVRForecasting = mod.SVRForecasting

file_path = "dataset_bali_2017_2025.xlsx"  # nama file Excel yang sudah di-upload
forecaster = SVRForecasting(file_path)

# Load data sheet pertama
if not forecaster.load_data(sheet_name=0):
    raise SystemExit("Failed to load data")

# Parameter manual (default dari project)
w1, w2, b = 0.01152, -0.000843, 0.02091

calculation_ok = forecaster.calculate_manual_svr(
    rooms_sold_col=None,
    rooms_available_col=None,
    w1=w1, w2=w2, b=b,
    output_col="X",
    n_rows=10
)

if calculation_ok:
    forecaster.explain_svr_calculation()

    # Simpan dataset dengan kolom X
    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"dataset_bali_with_svr_{ts}.xlsx"
    forecaster.data.to_excel(output_file, index=False)
    print(f"[SUCCESS] Saved {output_file}")
```

### Apa yang Akan Keluar di Output?

Jika berhasil:
- Di console bawah cell, Anda akan melihat:
  - Info loading data (jumlah baris/kolom, preview head)
  - Step-by-step perhitungan manual SVR untuk beberapa baris
  - Ringkasan statistik nilai `X`
  - Penjelasan tertulis tentang rumus SVR
  - Pesan `[SUCCESS] Saved dataset_bali_with_svr_YYYYMMDD_HHMMSS.xlsx`

File Excel hasil (dengan kolom `X`) akan tersimpan di:
- Folder `/content`
- Dengan nama mirip: `dataset_bali_with_svr_20260119_153000.xlsx`

---

## 9. Membuat dan Mendownload Visualisasi Hasil SVR

Untuk membuat gambar visualisasi `X`:

```python
from google.colab import files

if calculation_ok:
    # Buat dan simpan visualisasi manual SVR
    forecaster.visualize_manual_svr_results(
        x_col="X",
        rooms_sold_col=None,
        rooms_available_col=None
    )

    # Lokasi default penyimpanan (di script, biasanya di folder result/img).
    # Jika script menyimpan ke 'result/img/SVR_Manual_Bali_visualization.png',
    # pastikan folder tersebut ada dan file sudah dibuat.

    files.download("result/img/SVR_Manual_Bali_visualization.png")
```

Jika path berbeda (misal Anda ubah di script), sesuaikan nama file di `files.download(...)`.

Setelah cell dijalankan:
- Colab akan memunculkan dialog **download** file PNG ke komputer Anda.

---

## 10. Cara Membaca Output Excel & Gambar

- **File Excel `dataset_bali_with_svr_*.xlsx`**
  - Buka di Excel / LibreOffice / Google Sheets.
  - Akan ada kolom baru `X` yang berisi hasil perhitungan manual SVR.
  - Kolom ini bisa Anda bandingkan dengan kolom lain (misal `occupancy_rate`) jika ada.

- **File Gambar `SVR_Manual_Bali_visualization.png`**
  - Berisi 4 plot:
    - Time series nilai `X`
    - Distribusi nilai `X`
    - Scatter `rooms_sold` vs `X`
    - Scatter `rooms_available` vs `X`
  - Cocok dipakai untuk melihat pola dan hubungan antar variabel secara visual.

---

## 11. Menjalankan untuk Lombok

Jika Anda juga ingin menjalankan manual SVR untuk Lombok:

- Upload:
  - `SVR_Manual_Lombok.py`
  - `dataset_lombok_2017_2025.xlsx`
- Langkahnya sama seperti Bali, hanya ubah:
  - Nama file Python → `SVR_Manual_Lombok.py`
  - Nama file Excel → `dataset_lombok_2017_2025.xlsx`
  - Nama output/gambar jika ingin dibedakan.

---

## 12. Ringkasan Singkat (Checklist untuk Orang Awam)

- **[ ]** Buka `https://colab.research.google.com` dan buat **notebook baru**
- **[ ]** Install library di cell pertama (`pip install ...`)
- **[ ]** Upload file:
  - `SVR_Manual_Bali.py`
  - `dataset_bali_2017_2025.xlsx`
- **[ ]** Cek file sudah ada di `/content`
- **[ ]** Jalankan cell kode untuk:
  - Import dan menjalankan `SVR_Manual_Bali.py`
  - Menghitung kolom `X`
  - Menyimpan Excel hasil
- **[ ]** (Opsional) Jalankan cell untuk membuat dan download visualisasi
- **[ ]** Download Excel & gambar ke komputer, lalu buka dan analisis hasilnya.

Dengan mengikuti langkah-langkah di atas secara berurutan, pengguna awam sekalipun seharusnya bisa:
- Menjalankan program manual SVR di Colab
- Melihat output di console
- Mendapatkan file Excel hasil dan gambar visualisasi untuk dianalisis lebih lanjut.