# 📝 Panduan Penulisan Jurnal (Mode Manual SVR)

Mode yang dipakai: perhitungan manual SVR (tanpa forecasting masa depan), plus gap `prediksi_svr` (Excel) vs `X` (program).

## Struktur Umum Jurnal
1. Abstract  
2. Introduction  
3. Methodology  
4. Results and Discussion  
5. Conclusion  
6. References  

## Poin yang Perlu Disertakan

### Abstract
- Tujuan: baseline manual SVR occupancy rate, rumus linear.  
- Data: sebut dataset (mis. 2017–2025, lokasi).  
- Metode: manual SVR dengan bobot w1, w2, b.  
- Hasil: deskriptif kolom X, gap ringkas (min/max/mean).  
- Kesimpulan singkat: konsistensi antara `prediksi_svr` Excel dan hasil program.

### Introduction
- Latar belakang: kebutuhan baseline perhitungan sederhana.  
- Tujuan: menghasilkan kolom X dan gap terhadap `prediksi_svr`.  
- Manfaat: validasi/cek konsistensi perhitungan manual.  

### Methodology
- Dataset: sumber, periode, ukuran, kolom utama (`rooms_sold`, `rooms_available`, `prediksi_svr`).  
- Rumus manual:  
  `y = w1 * rooms_sold + w2 * rooms_available + b` (w1=0.01152, w2=-0.000843, b=0.02091).  
- Langkah: muat data, auto-detect kolom, hitung X, simpan Excel, hitung gap `prediksi_svr` vs `X`.  
- (Opsional) jika melatih model historis: sebut pipeline `prepare_features → split_data → scale_data → train_model → evaluate_model → visualize_results` untuk analisis internal (bukan forecasting future).  

### Results and Discussion
- Deskriptif kolom X: min, max, mean, std.  
- Gap `prediksi_svr` vs `X`: min, max, mean, std; contoh 5 baris.  
- Interpretasi: gap ≈ 0 berarti konsisten; gap besar → beda input atau pembulatan.  
- Jika ada visualisasi historis (opsional): jelaskan grafik actual vs predicted (train/test).  

### Conclusion
- Ringkasan: baseline manual SVR berjalan, file X + gap tersedia.  
- Keterbatasan: hanya dua fitur utama; sensitivitas ke skala; tidak melakukan forecasting masa depan.  
- Saran: perluasan fitur atau model lain untuk studi lebih lanjut.  

### References
- Sertakan referensi SVR/SVM umum (mis. Vapnik, Smola & Schölkopf) sesuai gaya jurnal.  

## Checklist Singkat
- [ ] Deskripsi dataset dan kolom kunci (`rooms_sold`, `rooms_available`, `prediksi_svr`).  
- [ ] Rumus manual SVR dan parameter (w1, w2, b).  
- [ ] Hasil X (statistik ringkas) dan contoh baris.  
- [ ] Hasil gap (statistik ringkas) dan contoh baris.  
- [ ] Interpretasi gap (positif/negatif) dan catatan toleransi.  
- [ ] (Opsional) Visualisasi historis jika pipeline model diaktifkan.  

## Catatan
- Mode ini tidak melakukan forecasting masa depan.  
- Pastikan file hasil yang dirujuk: `result/dataset/dataset_*with_svr_*.xlsx` dan `gap_prediksi_svr_vs_X_*.xlsx`.  

