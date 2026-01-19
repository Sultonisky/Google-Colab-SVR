## 📊 Penjelasan Hasil dan Cara Membaca Output (Manual SVR)

Mode ini **hanya menghitung manual SVR linear** untuk menghasilkan kolom output `X`.

## 📁 File Excel (Output Dataset)

### 1) `result/dataset/dataset_bali_with_svr_YYYYMMDD_HHMMSS.xlsx` (dan Lombok)
- Dataset asli + kolom `X` (hasil perhitungan manual SVR).
- Rumus:
  - `X = w1 * rooms_sold + w2 * rooms_available + b`
  - Default: `w1=0.01152`, `w2=-0.000843`, `b=0.02091`
- Kegunaan:
  - `X` bisa dipakai sebagai **indikator/kalkulasi internal** dan bisa dibandingkan dengan kolom lain (mis. `occupancy_rate`) jika tersedia.

## 🖼️ File Gambar (Opsional, jika visualisasi dijalankan)

### 1) `result/img/SVR_Manual_Bali_visualization.png` (dan Lombok)
Gambar berisi 4 plot untuk membantu membaca hasil `X`:
- Time series nilai `X` (dengan garis mean dan ±1 std dev)
- Histogram/distribusi nilai `X` (mean & median)
- Scatter `rooms_sold` vs `X` (dengan trend line)
- Scatter `rooms_available` vs `X` (dengan trend line)

Di bawah ini penjelasan yang lebih lengkap untuk tiap plot (versi awam).

---

## 📈 Plot 1 — Time Series (Nilai `X` dari waktu ke waktu)
**Tujuan:** melihat **tren** dan **perubahan** nilai `X` dari periode ke periode (misal: per hari/bulan sesuai data Anda).

**Yang biasanya terlihat di plot:**
- **Garis utama**: nilai `X` pada setiap baris/periode data.
- **Garis mean (rata-rata)**: patokan “nilai `X` normal/umum” di dataset.
- **Area ±1 standar deviasi (±1 std dev)**: rentang “variasi wajar” di sekitar rata-rata.

**Cara membaca cepat:**
- Jika garis `X` **cenderung naik** dari kiri ke kanan → performa indikator `X` **meningkat** seiring waktu.
- Jika garis `X` **cenderung turun** → performa indikator `X` **menurun**.
- Jika `X` **sering keluar** dari area ±1 std dev → dataset punya fluktuasi tinggi / ada kejadian tidak biasa.

**Hal yang perlu dicermati:**
- **Lonjakan tajam**: bisa menandakan event khusus, data input ekstrem, atau data salah input.
- **Pola musiman** (naik turun berulang): bisa menandakan seasonality (misal high season vs low season).

---

## 📊 Plot 2 — Histogram / Distribusi `X`
**Tujuan:** melihat nilai `X` **paling sering muncul** di rentang berapa, serta apakah data `X` “rapat” atau “menyebar”.

**Yang biasanya terlihat di plot:**
- **Batang histogram**: jumlah data (frekuensi) di rentang nilai `X`.
- **Garis mean (rata-rata)**: rata-rata `X`.
- **Garis median**: titik tengah data `X` (50% di bawah, 50% di atas).

**Cara membaca cepat:**
- Jika histogram **mengumpul rapat** → nilai `X` stabil (variasi kecil).
- Jika histogram **lebar/menyebar** → nilai `X` bervariasi besar.
- Jika **mean jauh dari median** → distribusi cenderung “miring” (ada banyak nilai ekstrem di satu sisi).

**Hal yang perlu dicermati:**
- **Dua puncak (bimodal)**: bisa berarti ada dua kondisi berbeda (misal: low season vs high season).
- **Ekor panjang**: menandakan ada outlier (nilai sangat tinggi/rendah).

---

## 🟠 Plot 3 — Scatter `rooms_sold` vs `X` (Scatter 1)
**Tujuan:** melihat hubungan antara **kamar terjual** (`rooms_sold`) dan nilai indikator `X`.

**Cara membaca cepat:**
- Secara logika (dengan parameter default), hubungan yang “normal” adalah **semakin tinggi `rooms_sold`, `X` cenderung naik**.
- **Trend line** membantu melihat arah umum hubungan:
  - trend line naik → hubungan positif (sesuai harapan)
  - trend line datar → `rooms_sold` tidak terlalu menjelaskan `X` (atau data bervariasi karena faktor lain)
  - trend line turun → tidak sesuai intuisi; perlu cek data/kolom/parameter

**Yang perlu diperhatikan:**
- **Titik yang jauh sekali** dari kumpulan utama = outlier (bisa karena data ekstrem atau error input).
- Kalau titik-titik **tersebar sangat acak**, artinya `X` tidak hanya dipengaruhi `rooms_sold` saja (wajar, karena juga ada `rooms_available` dan bias).

---

## 🔴 Plot 4 — Scatter `rooms_available` vs `X` (Scatter 2)
**Tujuan:** melihat hubungan antara **kamar tersedia/kosong** (`rooms_available`) dan nilai indikator `X`.

**Cara membaca cepat:**
- Secara logika (dengan parameter default), hubungan yang “normal” adalah **semakin tinggi `rooms_available`, `X` cenderung turun** (karena `w2` negatif).
- **Trend line**:
  - trend line turun → hubungan negatif (sesuai harapan)
  - trend line datar → pengaruh `rooms_available` kecil / data bervariasi
  - trend line naik → tidak sesuai intuisi; cek data/kolom/parameter

**Catatan penting (supaya tidak bingung):**
- Nilai `w2` (default) relatif kecil dibanding `w1`, jadi pengaruh `rooms_available` bisa tampak “lebih lemah” dibanding `rooms_sold` pada scatter.

---

## ✅ Cara menyimpulkan cepat dari 4 plot (1 menit)
- **Time series**: cari tren naik/turun dan lonjakan.
- **Histogram**: cari rentang nilai `X` yang paling sering, apakah stabil atau menyebar.
- **Scatter sold**: harusnya “cenderung naik”.
- **Scatter available**: harusnya “cenderung turun”.

Kalau hasil scatter berlawanan arah (sold turun, available naik), biasanya penyebabnya:
- kolom yang terbaca bukan kolom yang Anda maksud (auto-detect salah), atau
- data terbalik (misal: rooms_available sebenarnya total kamar, bukan kamar kosong), atau
- parameter `w1`, `w2`, `b` tidak cocok untuk dataset tersebut.

---

## 🧩 Contoh Kasus (Real Life) + Cara Membacanya
Bagian ini berisi contoh “kejadian umum” yang sering muncul di plot, supaya Anda gampang menyimpulkan.

### Kasus 1 — Time series naik perlahan (stabil)
**Yang terlihat:**
- Garis `X` naik pelan dari waktu ke waktu, dan banyak titik masih berada di sekitar area ±1 std dev.

**Makna sederhana:**
- Indikator `X` membaik secara bertahap.
- Biasanya terjadi karena `rooms_sold` makin bagus atau `rooms_available` makin kecil.

**Aksi cepat:**
- Bandingkan dengan periode sebelumnya: apakah memang `rooms_sold` naik?
- Cek apakah ada perubahan strategi (promo, event, musim liburan).

### Kasus 2 — Ada 1–2 lonjakan sangat tinggi/rendah
**Yang terlihat:**
- Beberapa titik `X` melonjak jauh di atas/di bawah titik lainnya (keluar dari area ±1 std dev).

**Kemungkinan penyebab:**
- **Event khusus** (peak season, libur panjang, konser, dll).
- **Data input ekstrem** (misal salah ketik: 1500 bukan 150).
- **Perubahan kapasitas** (jumlah kamar berubah drastis).

**Checklist cepat (paling berguna):**
- Cek baris data pada periode itu: nilai `rooms_sold` / `rooms_available` wajar atau tidak?
- Kalau ada kolom tanggal/periode, cocokkan dengan kejadian eksternal.

### Kasus 3 — Histogram sempit vs histogram lebar
**Yang terlihat:**
- Histogram **sempit**: batang berkumpul di rentang kecil.
- Histogram **lebar**: batang menyebar ke banyak rentang nilai.

**Makna sederhana:**
- **Sempit** → performa relatif konsisten.
- **Lebar** → performa fluktuatif (kadang bagus, kadang buruk).

**Aksi cepat:**
- Kalau lebar: cek time series, cari periode penyebab fluktuasi.

### Kasus 4 — Histogram “dua puncak” (bimodal)
**Yang terlihat:**
- Ada dua kumpulan nilai `X` yang sering muncul (dua puncak).

**Makna sederhana:**
- Dataset kemungkinan berisi **dua kondisi berbeda**, misalnya:
  - low season vs high season
  - sebelum vs sesudah suatu event/perubahan kebijakan
  - weekday vs weekend (kalau datanya harian)

**Aksi cepat:**
- Pisahkan data jadi dua periode, lalu bandingkan rata-rata `rooms_sold` dan `rooms_available`.

### Kasus 5 — Scatter `rooms_sold` vs `X` terlihat “naik” (sesuai harapan)
**Yang terlihat:**
- Titik-titik cenderung naik ke kanan.
- Trend line naik.

**Makna sederhana:**
- `rooms_sold` memang mendorong `X` naik (sesuai rumus, karena `w1` positif).

**Aksi cepat:**
- Cari outlier: titik yang jauh sendiri biasanya data ekstrem atau salah input.

### Kasus 6 — Scatter `rooms_available` vs `X` terlihat “turun” (sesuai harapan)
**Yang terlihat:**
- Titik-titik cenderung turun ke kanan.
- Trend line turun.

**Makna sederhana:**
- Semakin banyak kamar kosong/tersedia, indikator `X` turun (sesuai rumus, karena `w2` negatif).

### Kasus 7 — Arah scatter “kebalik” (membingungkan)
**Yang terlihat:**
- Scatter `rooms_sold` vs `X` trend line malah turun, atau
- Scatter `rooms_available` vs `X` trend line malah naik.

**Penyebab paling umum (urut dari yang paling sering):**
1. **Kolom kebaca salah** karena nama kolom mirip (auto-detect memilih kolom yang bukan Anda maksud).
2. **Definisi kolom berbeda**:
   - `rooms_available` di dataset Anda ternyata “total kamar”, bukan “kamar kosong/tersedia”.
3. **Ada nilai kosong/NaN** atau data tidak konsisten di beberapa periode.
4. **Parameter `w1/w2/b`** tidak cocok untuk dataset tersebut (biasanya kalau dataset beda skala/beda definisi).

**Aksi cepat (paling efektif):**
- Pastikan kolom yang dipakai benar (lihat output console “Columns used”).
- Kalau perlu, set manual nama kolom di `calculate_manual_svr(rooms_sold_col='...', rooms_available_col='...')`.

## 🖥️ Console Output (Utama)
- Preview dataset (`head`), `info`, dan statistik deskriptif.
- Step-by-step perhitungan manual SVR untuk beberapa baris pertama (default 10 baris).
- Ringkasan kolom `X` (min/max/mean/std).
- Jika kolom `rooms_sold` / `rooms_available` tidak ditemukan, program akan menampilkan daftar kolom yang ada dan contoh cara set nama kolom secara manual.

## Cara Membaca & Interpretasi Singkat
- **Kolom `X`**: hasil perhitungan manual berbasis `rooms_sold`, `rooms_available`, dan bias `b`.
- **Arah pengaruh parameter (default)**:
  - `w1` positif → `rooms_sold` naik → `X` cenderung naik.
  - `w2` negatif → `rooms_available` naik → `X` cenderung turun.
- **Catatan penting**: `X` adalah output formula linear yang mengikuti skala data input; interpretasikan sebagai skor/indikator sesuai konteks dataset Anda.

## Tips
- Pastikan dataset memiliki kolom `rooms_sold` dan `rooms_available` (atau sinonimnya). Jika auto-detect gagal, isi `rooms_sold_col` dan `rooms_available_col` secara manual saat memanggil `calculate_manual_svr(...)`.
- Tutup file Excel output jika sedang terbuka sebelum menjalankan program lagi, untuk menghindari `PermissionError` saat menyimpan (skrip sudah memakai nama berbasis timestamp untuk mengurangi konflik).

