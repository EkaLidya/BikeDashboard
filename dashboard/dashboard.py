import streamlit as st
import pandas as pd
import altair as alt
import os

# --- CONFIG DASHBOARD --- 
st.set_page_config(
    page_title="Dashboard Analisis Bike Sharing",
    page_icon="🚲",
    layout="wide"
)

@st.cache_data
def load_data():
    # Mendapatkan path absolut dari folder tempat dashboard.py berada
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Menentukan path file secara otomatis
    # Kita cek dulu apakah ada di folder 'data' atau langsung di folder utama
    main_path = os.path.join(base_dir, "main_data.csv")
    if not os.path.exists(main_path):
        main_path = os.path.join(base_dir, "data", "main_data.csv")
        
    hour_path = os.path.join(base_dir, "hour.csv")
    if not os.path.exists(hour_path):
        hour_path = os.path.join(base_dir, "data", "hour.csv")

    # Load data dengan error handling agar dashboard tidak crash total
    try:
        df = pd.read_csv(main_path)
        df['dteday'] = pd.to_datetime(df['dteday'])
        
        hour_df = pd.read_csv(hour_path)
        hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
        
        return df, hour_df
    except FileNotFoundError as e:
        st.error(f"⚠️ Waduh! File tidak ketemu. Pastikan 'main_data.csv' dan 'hour.csv' ada di folder: {base_dir}")
        st.stop() # Hentikan aplikasi agar tidak traceback panjang

df, hour_df = load_data()

# --- SIDEBAR FILTER ---
st.sidebar.image("https://img.icons8.com/clouds/100/000000/bicycle.png")
st.sidebar.header("Filter Eksplorasi")

# 1. Ambil input dari user
date_range = st.sidebar.date_input(
    "Rentang Waktu",
    min_value=df["dteday"].min(),
    max_value=df["dteday"].max(),
    value=[df["dteday"].min(), df["dteday"].max()]
)

# 2. Cek apakah user sudah memilih rentang lengkap (start dan end)
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    # Jika baru pilih satu tanggal, samakan start dan end agar tidak error
    start_date = end_date = date_range[0]

# 3. Filter dataframe berdasarkan hasil seleksi
main_df_filtered = df[
    (df["dteday"] >= pd.to_datetime(start_date)) & 
    (df["dteday"] <= pd.to_datetime(end_date))
]

hour_df_filtered = hour_df[
    (hour_df["dteday"] >= pd.to_datetime(start_date)) & 
    (hour_df["dteday"] <= pd.to_datetime(end_date))
]

# --- MAIN PAGE ---
st.title("🚲 Dashboard Interaktif Bike Sharing")

# --- METRICS ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", value=f"{main_df_filtered['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Suhu", value=f"{main_df_filtered['temp'].mean():.2f}")
with col3:
    st.metric("Hari Kerja Terpantau", value=f"{main_df_filtered['workingday'].sum()} Hari")

st.markdown("---")

# --- VISUALISASI 1: SUHU VS PENYEWAAN ---
st.subheader("1. Pengaruh Suhu terhadap Jumlah Penyewaan")
points = alt.Chart(main_df_filtered).mark_point(filled=True, size=60, opacity=0.5).encode(
    x=alt.X('temp:Q', title='Suhu (Normalized)'),
    y=alt.Y('cnt:Q', title='Total Penyewaan'),
    color=alt.value('#3182bd'),
    tooltip=['dteday', 'temp', 'cnt']
)
line = points.transform_regression('temp', 'cnt').mark_line(size=3).encode(
    color=alt.value('red')
)
st.altair_chart((points + line).interactive(), use_container_width=True)

# --- VISUALISASI 2: TREN JAM (Sesuai Filter Sidebar) ---
st.subheader("2. Pola Fluktuasi Penyewa: Casual vs Registered")
# Menghapus filter 'yr==0' dan 'holiday==1' agar grafik mengikuti pilihan user di sidebar
if not hour_df_filtered.empty:
    h_grouped = hour_df_filtered.groupby('hr')[['casual', 'registered']].mean().reset_index()
    h_melted = h_grouped.melt('hr', var_name='Tipe Pengguna', value_name='Rata-rata')

    line_chart = alt.Chart(h_melted).mark_line(point=True).encode(
        x=alt.X('hr:O', title='Jam (0-23)'),
        y=alt.Y('Rata-rata:Q', title='Rata-rata Jumlah Penyewa'),
        color=alt.Color('Tipe Pengguna:N', scale=alt.Scale(range=['#f39c12', '#2980b9'])),
        tooltip=['hr', 'Tipe Pengguna', 'Rata-rata']
    ).interactive()

    st.altair_chart(line_chart, use_container_width=True)
else:
    st.warning("Tidak ada data tersedia pada rentang waktu yang dipilih.")

# --- VISUALISASI 3: DAMPAK CUACA ---
st.subheader("3. Performa Berdasarkan Kondisi Cuaca")
weather_map = {1: 'Cerah', 2: 'Mendung', 3: 'Hujan/Salju Ringan', 4: 'Ekstrem'}
viz3_df = main_df_filtered.copy()
viz3_df['Cuaca'] = viz3_df['weathersit'].map(weather_map)

bar_chart = alt.Chart(viz3_df).mark_bar().encode(
    x=alt.X('Cuaca:N', sort='-y'),
    y=alt.Y('mean(cnt):Q', title='Rata-rata Penyewaan'),
    color=alt.Color('Cuaca:N', legend=None, scale=alt.Scale(scheme='viridis')),
    tooltip=['Cuaca', 'mean(cnt)']
).properties(height=400)

st.altair_chart(bar_chart, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.caption("Eka Lidya Rahmadini 2026")
