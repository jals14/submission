import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Dashboard Tren Polusi dan Cuaca di Stasiun Dongsi")

dongsi = pd.read_csv("dongsi.csv")
dongsi["date"] = pd.to_datetime(dongsi["date"], errors='coerce')
dongsi = dongsi.dropna(subset=["date"])

start_date = st.sidebar.date_input("Pilih Tanggal Mulai", dongsi["date"].min().date())
end_date = st.sidebar.date_input("Pilih Tanggal Akhir", dongsi["date"].max().date())

# Pilih kategori data
category = st.sidebar.radio("Pilih Kategori Data", ["Polusi", "Cuaca"])

if start_date > end_date:
    st.error("Masukkan tanggal mulai dan akhir dengan benar")
else:
    filtered_data = dongsi[(dongsi["date"] >= pd.to_datetime(start_date)) & 
                           (dongsi["date"] <= pd.to_datetime(end_date))]
    
    if filtered_data.empty:
        st.warning("Tidak ada data untuk rentang tanggal yang dipilih.")
    else:
        polution = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
        weather = ["TEMP", "PRES", "DEWP", "RAIN", "WSPM"]

        filtered_data["date_group"] = filtered_data["date"].dt.to_period("M")

        if category == "Polusi":
            selected_data = filtered_data.groupby("date_group")[polution].mean().reset_index()
        else:
            selected_data = filtered_data.groupby("date_group")[weather].mean().reset_index()
        
        selected_data["date_group"] = pd.to_datetime(selected_data["date_group"].astype(str))
        
        # Plot data sesuai kategori
        for col in (polution if category == "Polusi" else weather):
            if col in selected_data.columns:
                plt.figure(figsize=(10, 5))
                plt.plot(selected_data["date_group"], 
                         selected_data[col], 
                         marker='o', 
                         linestyle='-',
                         label=col)
                plt.title(f"Tren {col}", fontsize=14)
                plt.xlabel("Tanggal", fontsize=12)
                plt.ylabel(col, fontsize=12)
                plt.xticks(rotation=45)
                plt.legend()
                plt.grid(True)
                st.pyplot(plt)
