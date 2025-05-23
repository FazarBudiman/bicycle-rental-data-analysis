import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load dataset
bike_in_day_df = pd.read_csv('dataset/bike_in_day.csv')
bike_in_hour_df = pd.read_csv('dataset/bike_in_hour.csv')


st.title("Dashboard Analisis Penyewaan Sepeda")

# Tambahkan pilihan untuk jenis visualisasi
st.sidebar.header("Pengaturan Visualisasi Tren Penyewaan Per Jam")
chart_type = st.sidebar.radio(
    "Pilih tampilan data:",
    ["Total Penyewaan Sepeda", "Proporsi dari Jenis Pengguna"],
    horizontal=True
)
 
st.subheader("Pengaruh Kondisi Hari Terhadap Penyewaan Sepeda")
# Hitung rata-rata untuk setiap kategori berdasarkan kondisi hari
avg_by_day_condition = bike_in_day_df.groupby('day_condition')[['casual', 'registered', 'cnt']].mean().reset_index()

# Buat grafik berdasarkan pilihan
plt.figure(figsize=(14, 8))
if chart_type == "Total Penyewaan Sepeda":
    bars = plt.bar(avg_by_day_condition['day_condition'], avg_by_day_condition['cnt'], 
                   color='darkblue', width=0.6, edgecolor='black', linewidth=0.5)
    
    for i, (condition, cnt) in enumerate(zip(avg_by_day_condition['day_condition'], avg_by_day_condition['cnt'])):
        plt.text(i, cnt + 50, f'{cnt:.0f}', ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    plt.ylabel('Rata-rata Penyewaan Sepeda', fontsize=14)
    
else:
    # Stacked bar chart dengan breakdown casual + registered
    bar_width = 0.6
    x_pos = range(len(avg_by_day_condition['day_condition']))
    
    bars1 = plt.bar(x_pos, avg_by_day_condition['casual'], 
                    bar_width, label='Casual', color='lightblue', 
                    edgecolor='black', linewidth=0.5)
    
    bars2 = plt.bar(x_pos, avg_by_day_condition['registered'], 
                    bar_width, bottom=avg_by_day_condition['casual'], 
                    label='Registered', color='darkblue', 
                    edgecolor='black', linewidth=0.5)
    
    # Tambahkan nilai di atas setiap bar
    for i, (casual, registered, total) in enumerate(zip(avg_by_day_condition['casual'], 
                                                       avg_by_day_condition['registered'], 
                                                       avg_by_day_condition['cnt'])):
        plt.text(i, total + 50, f'{total:.0f}', ha='center', va='bottom', fontweight='bold', fontsize=12)
        plt.text(i, casual/2, f'{casual:.0f}', ha='center', va='center', fontweight='bold', color='white', fontsize=10)
        plt.text(i, casual + registered/2, f'{registered:.0f}', ha='center', va='center', fontweight='bold', color='white', fontsize=10)
    
    plt.ylabel('Rata-rata Penyewaan Sepeda', fontsize=14)

plt.xlabel('Kondisi Hari', fontsize=14)
plt.xticks(range(len(avg_by_day_condition['day_condition'])), avg_by_day_condition['day_condition'])

# Tampilkan legend hanya untuk breakdown chart
if chart_type == "Proporsi dari Jenis Pengguna":
    plt.legend(fontsize=12)

plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
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
sns.lineplot(x=work_day.index, y=work_day.values, label='Hari Kerja', color='darkblue')
sns.lineplot(x=holiday.index, y=holiday.values, label='Hari Libur', color='darkorange')
plt.xlabel('Waktu/Jam dalam Sehari')
plt.ylabel('Rata-rata Penyewaan Sepeda')
plt.title('Tren Penyewaan Sepeda per Jam di Hari Kerja dan Hari Libur')
plt.legend()
plt.xticks(range(selected_hours[0], selected_hours[1] + 1))
st.pyplot(plt)
