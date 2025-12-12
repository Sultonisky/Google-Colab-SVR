# 📓 Panduan Menjalankan Program Manual SVR di Google Colab

Mode: hanya perhitungan manual SVR (kolom `X`) dan gap `prediksi_svr` vs `X`. Tidak ada forecasting masa depan.

## Urutan Cell Disarankan

**Cell 1 — Install dependencies**
```python
!pip install pandas numpy scikit-learn matplotlib openpyxl
```

**Cell 2 — Ambil file dari Drive (contoh sederhana)**
```python
from google.colab import drive
import os, shutil

drive.mount('/content/drive')

# Ganti path sesuai lokasi Anda
SRC_PY = "/content/drive/MyDrive/path/to/SVR_Manual_Bali.py"
SRC_XLSX = "/content/drive/MyDrive/path/to/dataset_bali_2017_2025.xlsx"

for src, dst in [(SRC_PY, "SVR_Manual_Bali.py"), (SRC_XLSX, "dataset_bali_2017_2025.xlsx")]:
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"[SUCCESS] Copied {src} -> {dst}")
    else:
        print(f"[ERROR] File tidak ditemukan: {src}")

print("\n[INFO] Files in /content:")
print(os.listdir("/content"))
```

**Cell 3 — Jalankan manual SVR & buat gap**
```python
from SVR_Manual_Bali import SVRManual
from datetime import datetime

file_path = "dataset_bali_2017_2025.xlsx"
forecaster = SVRManual(file_path)

if not forecaster.load_data(sheet_name=0):
    raise SystemExit("Gagal load data")

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
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"dataset_bali_with_svr_{ts}.xlsx"
    forecaster.data.to_excel(output_file, index=False)
    print(f"[SUCCESS] Saved {output_file}")

    forecaster.create_gap_prediksi_svr_vs_X(
        pred_col="prediksi_svr",
        x_col="X",
        output_file="gap_prediksi_svr_vs_X.xlsx"
    )
```

**Cell 4 — Download hasil**
```python
from google.colab import files
import os, glob

def safe_download(fn):
    if os.path.exists(fn):
        files.download(fn)
        print(f"[SUCCESS] Downloaded {fn}")
    else:
        print(f"[WARNING] {fn} not found")

dataset_files = glob.glob("dataset_bali_with_svr_*.xlsx")
if dataset_files:
    safe_download(dataset_files[0])
else:
    print("[WARNING] dataset_bali_with_svr_*.xlsx tidak ditemukan")

safe_download("gap_prediksi_svr_vs_X.xlsx")
```

## Catatan
- Untuk Lombok, gunakan `SVR_Manual_Lombok.py` dan `dataset_lombok_2017_2025.xlsx`.
- Jika ingin visualisasi historis, sesuaikan script untuk memanggil pipeline pelatihan lalu simpan gambar ke `/content/result/img/`.

