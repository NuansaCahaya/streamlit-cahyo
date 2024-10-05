import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


all_df = pd.read_csv("all_data.csv")

datetime_columns = ["date"]
all_df.sort_values(by="date", inplace=True)
all_df.reset_index(inplace=True)
    
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["date"].min()
max_date = all_df["date"].max()
    
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://lh5.googleusercontent.com/Y9uzg5V3GHX0hs3GvxNeM10uIDwHxxJ8a_FvOl3rm69swh1PY4p3xsIRaqBBIwe7h2tkPBx9uukbRJOdtF2JAOh5yG3iGN7-NaGNnDVWDyyRbwXNxxUr1yCgtC4avM8NoQ=w1280")
    
    st.write("""
Proyek Analisis Data: Air Quality Dataset (Changping District)
- Nama: Nuansa Cahaya Muhammad
- Email: m004b4ky3407@bangkit.academy
- ID Dicoding: nuansacahayamuhammad
             
Jika anda ingin mengetahui jumlah konsentrasi polusi di udara di distrik Changping, silahkan pilih tanggal dibawah
""")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Date Filter',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

st.title('Air Quality in Changping :sparkles:')

main_df = all_df[(all_df["date"] >= str(start_date)) & 
                (all_df["date"] <= str(end_date))]

st.write("""
Proyek Analisis Data: Air Quality Dataset (Changping District)
- Nama: Nuansa Cahaya Muhammad
- Email: m004b4ky3407@bangkit.academy
- ID Dicoding: nuansacahayamuhammad
""")

st.header("Pertanyaan 1: Bagaimana hubungan antara suhu (TEMP) dan konsentrasi ozon (O3) di Distrik Changping?")
st.subheader("Perbandingan Konsentrasi O3 dan TEMP")
# Memilih kolom 'date', 'O3', dan 'TEMP', kemudian menjadikan 'date' sebagai indeks
# Resampling data menjadi rata-rata bulanan (M untuk bulanan) dan menghitung nilai rata-rata per bulan
data_time_series = all_df[['date', 'O3', 'TEMP']].set_index('date').resample('M').mean()
# Membuat figur/kanvas untuk plot dengan ukuran 15x6 inci
fig = plt.figure(figsize=(10,6))
# Membuat plot garis untuk konsentrasi O3 (Ozon) dengan warna merah
plt.plot(data_time_series.index, data_time_series['O3'], label='O3', color='red')
# Membuat plot garis untuk suhu (TEMP) dengan warna biru
plt.plot(data_time_series.index, data_time_series['TEMP'], label='TEMP', color='blue')
plt.xlabel("Date")
plt.ylabel("Concentration")
plt.legend()
st.pyplot(fig) 

st.write("""Berikut analisisnya:
- Baik O3 maupun suhu menunjukkan pola musiman yang kuat. Terlihat bahwa konsentrasi O3 (garis merah) meningkat pada musim panas (sekitar pertengahan tahun, yaitu Juli-Agustus), dan menurun pada musim dingin (sekitar Desember-Januari). Pola yang sama berlaku untuk suhu (garis biru), yang juga mencapai puncak selama bulan-bulan musim panas dan turun ke titik terendah di musim dingin.
- Dari grafik ini, tampak adanya korelasi positif antara suhu dan konsentrasi O3. Ketika suhu meningkat (musim panas), konsentrasi O3 juga meningkat, dan sebaliknya, ketika suhu menurun (musim dingin), konsentrasi O3 juga menurun.
""")

st.subheader("Scatter Plot of TEMP vs O3")
# Membuat figur/kanvas dengan satu subplot dan ukuran 20x10 inci
fig, ax = plt.subplots(1, 1, figsize=(20, 10))
# Membuat scatter plot untuk hubungan antara suhu (TEMP) dan Ozon (O3)
sns.scatterplot(ax=ax, x='TEMP', y='O3', data=all_df, label='O3', legend='full')
# Menambahkan label sumbu X dan Y
ax.set_xlabel('Temperature (TEMP)')
ax.set_ylabel('Ozone (O3)')
# Menampilkan plot
st.pyplot(fig) 

st.write("Secara keseluruhan, ada hubungan positif antara suhu (TEMP) dan konsentrasi ozon (O3). Ini berarti ketika suhu meningkat, konsentrasi ozon cenderung meningkat juga. Hubungan ini terlihat jelas pada bagian kanan grafik, di mana titik-titik naik tajam setelah suhu mencapai sekitar 10°C.")

st.header("Pertanyaan 2: Bagaimana perbandingan kualitas udara di Distrik Changping antara waktu AM dan waktu PM berdasarkan konsentrasi polutan di udara?")
#Bar Plot
st.subheader("Rata-rata Konsentrasi Polutan Berdasarkan AM/PM dengan Bar Plot")
# Membuat dataframe hasil agregasi hanya dengan rata-rata
mean_data = all_df.groupby(by="AM/PM").agg({
    "PM2.5": "mean",
    "PM10": "mean",
    "SO2": "mean",
    "NO2": "mean",
    "CO": "mean",
    "O3": "mean"
})
# Melakukan transpose data agar lebih mudah divisualisasikan
mean_data = mean_data.T
# Menentukan jumlah polutan
pollutants = mean_data.index
n_pollutants = len(pollutants)
# Membuat subplots dalam format 2x3
fig, axs = plt.subplots(2, 3, figsize=(15, 8), sharex=True)
# Rata-rata posisi untuk subplot
axs = axs.flatten()  # Mengubah array 2D menjadi 1D
# Membuat plot untuk setiap polutan
for i, polutan in enumerate(pollutants):
    bars = axs[i].bar(mean_data.columns, mean_data.loc[polutan], color='b', alpha=0.7)
    axs[i].set_title(f'Rata-rata Konsentrasi {polutan}', fontsize=10)
    axs[i].set_ylabel('Nilai Konsentrasi', fontsize=8)
    axs[i].set_ylim(0, mean_data.loc[polutan].max() + 10)  # Set batas y   
    # Menambahkan nilai di atas batang
    for bar in bars:
        yval = bar.get_height()
        axs[i].text(bar.get_x() + bar.get_width() / 2, yval + 1, round(yval, 1), 
                     ha='center', va='bottom', fontsize=8)
# Menambahkan label x pada subplot paling bawah
axs[3].set_xlabel('AM/PM', fontsize=10)
axs[4].set_xlabel('AM/PM', fontsize=10)
axs[5].set_xlabel('AM/PM', fontsize=10)
# Menambahkan judul keseluruhan
plt.suptitle('Rata-rata Konsentrasi Polutan Berdasarkan AM/PM', fontsize=14)
# Menampilkan plot
plt.tight_layout(rect=[0, 0, 1, 0.96])  # Untuk memberi ruang bagi judul
st.pyplot(fig)


st.subheader("Heatmap Rata-rata Konsentrasi Polutan Berdasarkan AM/PM")
# Membuat heatmap dari data mean
fig = plt.figure(figsize=(10, 6))
sns.heatmap(mean_data, annot=True, fmt=".1f", cmap='YlGnBu', cbar=True)
# Menambahkan detail ke heatmap
plt.title('Heatmap Rata-rata Konsentrasi Polutan Berdasarkan AM/PM', fontsize=14)
plt.ylabel('Polutan')
plt.xlabel('AM/PM')
plt.tight_layout()
st.pyplot(fig)

st.write("""
- Kualitas udara pada waktu PM (tengah hari (12:00 PM) hingga sebelum tengah malam (11:59 PM)) umumnya lebih buruk untuk beberapa polutan seperti PM2.5, PM10, SO2, dan terutama Ozon (O3). Ozon adalah polutan yang meningkat secara signifikan pada sore hari karena reaksi fotokimia yang dipicu oleh sinar matahari.
- Pada waktu AM (tengah malam (12:00 AM) hingga sebelum tengah hari (11:59 AM)), kualitas udara lebih buruk untuk CO (Karbon Monoksida), yang kemungkinan disebabkan oleh peningkatan aktivitas kendaraan pada jam sibuk pagi hari. Ini dapat berdampak pada kesehatan manusia, terutama bagi orang-orang yang berada di luar ruangan selama jam-jam tersebut.
- NO2 menunjukkan konsentrasi yang hampir sama antara AM dan PM, yang menunjukkan sumber emisi konstan, seperti dari kendaraan dan industri.
""")

st.subheader("Conclusion")
st.write("""
- Conclusion pertanyaan 1: Terdapat korelasi positif antara suhu dengan konsentrasi ozon. Ini menunjukkan bahwa ketika suhu meningkat, konsentrasi O3 atau ozon cenderung meningkat juga.
- Conclusion pertanyaan 2: Secara keseluruhan, kualitas udara pada sore hari (PM) cenderung lebih buruk karena tingginya konsentrasi polutan seperti PM10, SO2, dan terutama ozon, yang merupakan ancaman besar bagi kesehatan pernapasan. Pagi hari (AM) lebih baik dari segi beberapa polutan, tetapi masih menghadapi masalah dengan konsentrasi karbon monoksida yang lebih tinggi.
""")

st.header("Jumlah Konsentrasi Polusi di Udara Berdasarkan Tanggal yang Anda Pilih")
st.write("""
Jika anda ingin mengetahui jumlah konsentrasi polusi di udara, silahkan pilih tanggal yang anda inginkan di sidebar sebelah kiri
""")
st.subheader("PM2.5 Polution")
groupByYear = main_df.groupby("date").mean(numeric_only=True)


fig = plt.figure(figsize=(10,6))
plt.plot(groupByYear.index, groupByYear["PM2.5"], label="PM2.5")
plt.xlabel("Date")
plt.ylabel("Concentration")
plt.legend()
st.pyplot(fig)


st.subheader("PM10 Polution")
groupByYear = main_df.groupby("date").mean(numeric_only=True)


fig = plt.figure(figsize=(10,6))
plt.plot(groupByYear.index, groupByYear["PM10"], label="PM10")
plt.xlabel("Date")
plt.ylabel("Concentration")
plt.legend()
st.pyplot(fig)

st.subheader("SO2 Polution")
groupByYear = main_df.groupby("date").mean(numeric_only=True)


fig = plt.figure(figsize=(10,6))
plt.plot(groupByYear.index, groupByYear["SO2"], label="SO2")
plt.xlabel("Date")
plt.ylabel("Concentration")
plt.legend()
st.pyplot(fig)

st.subheader("NO2 Polution")
groupByYear = main_df.groupby("date").mean(numeric_only=True)


fig = plt.figure(figsize=(10,6))
plt.plot(groupByYear.index, groupByYear["NO2"], label="NO2")
plt.xlabel("Date")
plt.ylabel("Concentration")
plt.legend()
st.pyplot(fig)

st.subheader("CO Polution")
groupByYear = main_df.groupby("date").mean(numeric_only=True)


fig = plt.figure(figsize=(10,6))
plt.plot(groupByYear.index, groupByYear["CO"], label="CO")
plt.xlabel("Date")
plt.ylabel("Concentration")
plt.legend()
st.pyplot(fig)

st.subheader("O3 Polution")
groupByYear = main_df.groupby("date").mean(numeric_only=True)


fig = plt.figure(figsize=(10,6))
plt.plot(groupByYear.index, groupByYear["O3"], label="O3")
plt.xlabel("Date")
plt.ylabel("Concentration")
plt.legend()
st.pyplot(fig)


st.subheader("Temperatur")
groupByYear = main_df.groupby("date").mean(numeric_only=True)


fig = plt.figure(figsize=(10,6))
plt.plot(groupByYear.index, groupByYear["TEMP"], label="TEMP")
plt.xlabel("Date")
plt.ylabel("Concentration")
plt.legend()
st.pyplot(fig)


st.caption("by: Nuansa Cahaya Muhammad")
