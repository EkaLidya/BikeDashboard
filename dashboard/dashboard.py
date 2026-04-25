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

# --- LOAD DATA ---
@st.cache_data
def load_data():
    # Mengambil direktori tempat file dashboard.py berada
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path untuk data utama
    main_path = os.path.join(base_dir, "main_data.csv")
    
    # Path untuk data jam (Cek di folder yang sama dulu, baru cek folder data)
    hour_path = os.path.join(base_dir, "hour.csv")
    if not os.path.exists(hour_path):
        hour_path = os.path.join(base_dir, "..", "data", "hour.csv")
    
    # Proses Loading
    df = pd.read_csv(main_path)
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    hour_df = None
    if os.path.exists(hour_path):
        hour_df = pd.read_csv(hour_path)
        hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
        
    return df, hour_df
# PENTING: Panggil fungsi ini agar variabel df dan hour_df tersedia
df, hour_df = load_data()

# --- SIDEBAR FILTER (Definisikan Variabel di Sini) ---
st.sidebar.image("https://img.icons8.com/clouds/100/000000/bicycle.png")
st.sidebar.header("Filter Eksplorasi")

# Membuat variabel start_date dan end_date agar bisa dipakai di bawah
start_date, end_date = st.sidebar.date_input(
    "Rentang Waktu",
    min_value=df["dteday"].min(),
    max_value=df["dteday"].max(),
    value=[df["dteday"].min(), df["dteday"].max()]
)

# Membuat variabel filtered_df berdasarkan input user
filtered_df = df[
    (df["dteday"] >= pd.to_datetime(start_date)) & 
    (df["dteday"] <= pd.to_datetime(end_date))
]

# --- MAIN PAGE ---
st.title("🚲 Dashboard Interaktif Bike Sharing")

# --- METRICS ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", value=f"{filtered_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Suhu", value=f"{filtered_df['temp'].mean():.2f}")
with col3:
    st.metric("Hari Kerja Terpantau", value=f"{filtered_df['workingday'].sum()} Hari")

st.markdown("---")

# --- VISUALISASI 1: SUHU VS PENYEWAAN (Regresi Merah) ---
st.subheader("1. Pengaruh Suhu terhadap Jumlah Penyewaan")
points = alt.Chart(filtered_df).mark_point(filled=True, size=60, opacity=0.5).encode(
    x=alt.X('temp:Q', title='Suhu (Normalized)'),
    y=alt.Y('cnt:Q', title='Total Penyewaan'),
    color=alt.value('#3182bd'),
    tooltip=['dteday', 'temp', 'cnt']
)
line = points.transform_regression('temp', 'cnt').mark_line(size=3).encode(
    color=alt.value('red')
)

st.altair_chart((points + line).interactive(), use_container_width=True)

# --- VISUALISASI 2: TREN JAM (Casual vs Registered) ---
st.subheader("2. Pola Fluktuasi Penyewa: Casual vs Registered (Holiday 2011)")
if hour_df is not None:
    # PERBAIKAN: Menambahkan filter 'holiday == 1' dan 'yr == 0' (tahun 2011)
    # Ini akan membuat angka rata-rata sesuai dengan hasil di Colab Anda
    h_filtered = hour_df[
        (hour_df["yr"] == 0) & 
        (hour_df["holiday"] == 1) &
        (hour_df["dteday"] >= pd.to_datetime(start_date)) & 
        (hour_df["dteday"] <= pd.to_datetime(end_date))
    ]
    
    if not h_filtered.empty:
        h_grouped = h_filtered.groupby('hr')[['casual', 'registered']].mean().reset_index()
        h_melted = h_grouped.melt('hr', var_name='Tipe Pengguna', value_name='Rata-rata')

        line_chart = alt.Chart(h_melted).mark_line(point=True).encode(
            x=alt.X('hr:O', title='Jam (0-23)'),
            y=alt.Y('Rata-rata:Q', title='Rata-rata Jumlah Penyewa'),
            color=alt.Color('Tipe Pengguna:N', scale=alt.Scale(range=['#f39c12', '#2980b9'])),
            tooltip=['hr', 'Tipe Pengguna', 'Rata-rata']
        ).interactive()

        st.altair_chart(line_chart, use_container_width=True)
    else:
        st.warning("Tidak ada data hari libur tahun 2011 pada rentang waktu yang dipilih.")
else:
    st.error("File 'hour.csv' tidak ditemukan.")

# --- VISUALISASI 3: DAMPAK CUACA ---
st.subheader("3. Performa Berdasarkan Kondisi Cuaca")
weather_map = {1: 'Cerah', 2: 'Mendung', 3: 'Hujan/Salju Ringan', 4: 'Ekstrem'}
# Gunakan .copy() untuk menghindari SettingWithCopyWarning
viz3_df = filtered_df.copy()
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