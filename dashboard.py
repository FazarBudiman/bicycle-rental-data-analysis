import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load dataset
bike_in_day_df = pd.read_csv('dataset/bike_in_day.csv')
bike_in_hour_df = pd.read_csv('dataset/bike_in_hour.csv')


st.title("Dashboard Analisis Penyewaan Sepeda")

colors = ['#3867d6', '#fa8231']

st.subheader("Pengaruh Kondisi Hari Terhadap Penyewaan Sepeda")
pivot_day_condition = bike_in_day_df.pivot_table(
    values='cnt',
    index='day_condition',
    aggfunc='mean'
)
plt.figure(figsize=(14, 8))
bars = plt.bar(pivot_day_condition.index, pivot_day_condition['cnt'], color=colors, width=0.6, 
              edgecolor='black', linewidth=0.5)
plt.title('Pengaruh Kondisi Hari terhadap Penyewaan Sepeda', fontsize=16, fontweight='bold')
plt.xlabel('Kondisi Hari', fontsize=14)
plt.ylabel('Rata-rata Penyewaan Sepeda', fontsize=14)
plt.xticks(rotation=45)
st.pyplot(plt)


# Sidebar
st.sidebar.header("Pengaturan Visualisasi Tren Penyewaan Per Jam")
selected_hours = st.sidebar.slider("Pilih Rentang Jam:", 0, 23, (0, 23))

# Subheader
st.subheader('Tren Penyewaan Sepeda per Jam di Hari Kerja dan Hari Libur')

# Filter data sesuai rentang jam yang dipilih
filtered_df = bike_in_hour_df[
    (bike_in_hour_df['hr'] >= selected_hours[0]) & 
    (bike_in_hour_df['hr'] <= selected_hours[1])
]

# Hitung rata-rata penyewaan per jam
work_day = filtered_df[filtered_df['day_condition'] == 'Hari Kerja'].groupby('hr')['cnt'].mean()
holiday = filtered_df[filtered_df['day_condition'] == 'Hari Libur'].groupby('hr')['cnt'].mean()

# Plotting
plt.figure(figsize=(10, 5))
colors = sns.color_palette("Set2", 2)  # Warna default jika belum didefinisikan
sns.lineplot(x=work_day.index, y=work_day.values, label='Hari Kerja', color='#3867d6')
sns.lineplot(x=holiday.index, y=holiday.values, label='Hari Libur', color='#fa8231')
plt.xlabel('Waktu/Jam dalam Sehari')
plt.ylabel('Rata-rata Penyewaan Sepeda')
plt.title('Tren Penyewaan Sepeda per Jam di Hari Kerja dan Hari Libur')
plt.legend()
plt.xticks(range(selected_hours[0], selected_hours[1] + 1))
st.pyplot(plt)
