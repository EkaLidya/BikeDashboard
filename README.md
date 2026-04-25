# 🚲 Bike Sharing Analysis Dashboard
Proyek ini adalah aplikasi dashboard interaktif yang menyajikan hasil analisis data dari dataset *Bike Sharing*. Dashboard ini dikembangkan menggunakan **Streamlit** untuk memvisualisasikan tren penggunaan sepeda berdasarkan faktor cuaca, waktu, dan kategori penggunaan.
## 📊 Deskripsi Proyek
Dashboard ini menampilkan temuan kunci dari tiga pertanyaan bisnis utama:
1. **Dampak Suhu**: Analisis hubungan antara suhu dengan total penyewaan pada hari kerja di tahun 2012.
2. **Pola Fluktuasi**: Perbandingan pola rata-rata penyewa *Casual* vs *Registered* setiap jamnya selama masa liburan.
3. **Kondisi Cuaca**: Analisis jumlah penyewaan berdasarkan berbagai kondisi cuaca (Cerah, Mendung, Hujan Ringan).

## 🛠️ Persiapan Lingkungan & Cara Menjalankan
Ikuti langkah-langkah di bawah ini untuk menjalankan dashboard di komputer lokal Anda:


### 1. Membuat & Mengaktifkan Virtual Environment
Pastikan Anda menggunakan terminal atau command prompt:
```bash
# Membuat environment baru dengan Python 3.9
conda create --name main-ds python=3.9
# Mengaktifkan environment
conda activate main-ds

### 2. Menginstall library yang dibutuhkan
pip install streamlit pandas seaborn altair matplotlib

### 3. Menjalankan dashboard streamlit
# Masuk ke direktori dashboard
cd dashboard
# Menjalankan aplikasi
streamlit run dashboard.py



Local URL: http://localhost:8501
Network URL: http://192.168.1.8:8501