# 📓 Panduan Menjalankan Program Manual SVR di Google Colab

Mode: hanya perhitungan manual SVR (kolom `X`) dan visualisasi hasil SVR.

## Urutan Cell Disarankan

**Cell 1 — Install dependencies (import)**
```python
!pip install -r requirements.txt
```

**Cell 2 — Ambil file dari Drive (contoh sederhana)**
```python
import os
import sys

sys.path.append("/content")

required_py = "SVR_Manual_Bali.py"

print("[INFO] Checking for SVR_Manual_Bali.py...")

# Check if main file exists
if os.path.exists(required_py):
    print("[SUCCESS] SVR_Manual_Bali.py found.")
else:
    print("[WARNING] SVR_Manual_Bali.py not found. Searching for similar filenames...")

    # Find alternative files such as SVR_Manual_Bali (1).py or similar
    for f in os.listdir("/content"):
        if f.startswith("SVR_Manual_Bali") and f.endswith(".py") and f != required_py:
            os.rename(f, required_py)
            print("[INFO] Similar Python file found and renamed to SVR_Manual_Bali.py")
            break
    else:
        print("[ERROR] No matching Python file found. Please ensure the file has been uploaded to Colab.")

```

**Cell 3 — Jalankan manual SVR**
```python
import importlib.util

spec = importlib.util.spec_from_file_location("SVR_Manual_Bali", "SVR_Manual_Bali.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

SVRForecasting = mod.SVRForecasting

file_path = "dataset_bali_2017_2025.xlsx"
forecaster = SVRForecasting(file_path)

# Load data sheet pertama
if not forecaster.load_data(sheet_name=0):
    raise SystemExit("Failed to load data")

# Parameter manual
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

**Cell 4 — Download hasil Visualisasi**
```python
from google.colab import files
if calculation_ok:
    forecaster.explain_svr_calculation()

    # Simpan visualisasi manual SVR
    forecaster.visualize_manual_svr_results(
        x_col="X",
        rooms_sold_col=None,
        rooms_available_col=None
    )

    # Auto-download hasil visualisasi
    # Correcting the file path to match where the visualization was actually saved.
    files.download("/result/img/SVR_Manual_Bali_visualization.png")
```

## Catatan
- Untuk Lombok, gunakan `SVR_Manual_Lombok.py` dan `dataset_lombok_2017_2025.xlsx`.
- Jika ingin visualisasi historis, sesuaikan script untuk memanggil pipeline pelatihan lalu simpan gambar ke `/content/result/img/`.

