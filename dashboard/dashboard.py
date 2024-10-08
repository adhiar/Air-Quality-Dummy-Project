import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np 
import seaborn as sb
import scipy as sp 
import os
import geopandas as gpd
from shapely.geometry import Point
import folium
from folium.plugins import HeatMap
import streamlit as st
from streamlit_folium import st_folium

droped = pd.read_csv('main_data.csv')
st.header('AIR QUALITY DASHBOARD')
tab1, tab2 = st.tabs(["Data Mining", "Explanation"])

with tab1:
    st.header("Data Mining")
    st.write("Section ini akan memperlihatkan visualisasi data dari data yang telah digabung menjadi satu yang terdiri dari 12 data stasiun pengamatan kualitas udara")
    
    with st.container():
        st.subheader("Rata-rata indeks Polutansi tiap daerah")
        stasiun = sorted(droped['station'].unique())
        rataan_pm25 = droped.groupby('station')['PM2.5'].mean()
        rataan_pm10 = droped.groupby('station')['PM10'].mean()

        pollutant = st.selectbox('Pilih indeks yang ingin dilihat:', ('PM2.5', 'PM10'), key='pollutant_selectbox')
        
        plt.figure(figsize=(10, 6))
        
        if pollutant == 'PM2.5':
            plt.bar(stasiun, rataan_pm25)
            plt.axhline(y=min(rataan_pm25), color='r', linestyle='--', label='nilai min')
            plt.axhline(y=max(rataan_pm25), color='r', linestyle='--', label='nilai max')
            plt.title("Rataan Indeks PM2.5 Tiap Stasiun")
            plt.ylabel("Indeks PM2.5")
        else:
            plt.bar(stasiun, rataan_pm10)
            plt.axhline(y=min(rataan_pm10), color='r', linestyle='--', label='nilai min')
            plt.axhline(y=max(rataan_pm10), color='r', linestyle='--', label='nilai max')
            plt.title("Rataan Indeks PM10 Tiap Stasiun")
            plt.ylabel("Indeks PM10")

        plt.xticks(rotation=60)
        plt.xlabel("Stasiun")
        plt.legend()
        st.pyplot(plt)
        plt.close()  
    
    with st.container():
        st.subheader("Tampilan Geospasial Kualitas Udara")
        koor = {
            'Aotizhongxin': (39.988, 116.407),
            'Changping': (40.217, 116.231),
            'Dingling': (40.296, 116.181),
            'Dongsi': (39.928, 116.417),
            'Guanyuan': (39.933, 116.365),
            'Gucheng': (39.927, 116.202),
            'Huairou': (40.316, 116.637),
            'Nongzhanguan': (39.936, 116.454),
            'Shunyi': (40.126, 116.654),
            'Tiantan': (39.883, 116.412),
            'Wanliu': (39.974, 116.299),
            'Wanshouxigong': (39.886, 116.361)
        }

        pollutant_map = st.selectbox('Pilih indeks yang ingin dilihat (Map):', ('PM2.5', 'PM10'), key='pollutant_map_selectbox')
        rataan = droped.groupby('station')[pollutant_map].mean()
        rataan_df = rataan.reset_index()

        rataan_df['coordinates'] = rataan_df['station'].map(koor)
        rataan_df['geometry'] = rataan_df['coordinates'].apply(lambda x: Point(x[1], x[0]))

        gdf = gpd.GeoDataFrame(rataan_df, geometry='geometry')
        gdf.set_crs(epsg=4326, inplace=True)

        m = folium.Map(location=[39.9, 116.4], zoom_start=10, tiles='CartoDB positron', 
                        scrollWheelZoom=False, zoom_control=False)

        heat_data = [[point.y, point.x, pm] for point, pm in zip(gdf.geometry, gdf[pollutant_map]) if pm is not None]
        max_pm = gdf[pollutant_map].max() 

        HeatMap(
            heat_data, 
            gradient={0.0: 'blue', 0.4: 'green', 0.7: 'yellow', 1.0: 'red'}, 
            radius=25, 
            blur=15,
            max_val=max_pm
        ).add_to(m)

        for station, (lat, lon) in koor.items():
            pm_value = rataan_df.loc[rataan_df['station'] == station, pollutant_map].values[0]
            folium.Marker(
                location=[lat, lon],
                popup=f"{station}: {pm_value:.2f}",
                icon=folium.Icon(color='blue')
            ).add_to(m)
        
        st_folium(m, width=1000, height=600)
    
    with st.container():
        st.subheader("data pendukung spasial")
        stasiun = sorted(droped['station'].unique())
        rataan_temp = droped.groupby('station')['TEMP'].mean()
        rataan_pres = droped.groupby('station')['PRES'].mean()
        rataan_o3 = droped.groupby('station')['O3'].mean()

        plt.figure(figsize=(8, 12))
        plt.subplot(3, 1, 1)
        plt.bar(stasiun, rataan_temp, label='TEMPERATUR')
        plt.ylabel("Temperature")
        plt.axhline(y=min(rataan_temp), color='r', linestyle='--', label=f'nilai min')
        plt.xticks([])

        plt.subplot(3, 1, 2)
        plt.bar(stasiun, rataan_pres, label='TEKANAN')
        plt.ylabel("Tekanan")
        plt.axhline(y=min(rataan_pres), color='r', linestyle='--', label=f'nilai min')
        plt.xticks([])
        plt.ylim(min(rataan_pres)-50, max(rataan_pres)+10)

        plt.subplot(3, 1, 3)
        plt.bar(stasiun, rataan_o3, label='O3')
        plt.ylabel("O3")
        plt.xlabel("Stasiun")
        plt.axhline(y=min(rataan_o3), color='r', linestyle='--', label=f'nilai min')
        plt.xticks(rotation=60)

        plt.tight_layout()
        st.pyplot(plt)  
        plt.close()  
    
    with st.container():
        st.subheader("Hubungan Indeks PM10 dengan Unsur Kimia Berbahaya")
        x_pm10 = droped['PM10']
        par_pm10 = st.selectbox('Pilih partikel untuk PM10:', ('SO2', 'CO', 'O3', 'NO2'), key='particle_pm10')
        plt.figure(figsize=(10, 6))  
        sb.scatterplot(x=x_pm10, y=droped[par_pm10])
        sb.regplot(x=x_pm10, y=droped[par_pm10], scatter=False, color='r')
        plt.ylabel(f'Jumlah Partikel {par_pm10}')
        plt.xlabel('Indeks PM10')
        plt.legend()
        st.pyplot(plt)
        plt.close()

    with st.container():
        st.subheader("Hubungan Indeks PM2.5 dengan Unsur Kimia Berbahaya")
        x_pm25 = droped['PM2.5']
        par_pm25 = st.selectbox('Pilih partikel untuk PM2.5:', ('SO2', 'CO', 'O3', 'NO2'), key='particle_pm25')
        plt.figure(figsize=(10, 6))  
        sb.scatterplot(x=x_pm25, y=droped[par_pm25])
        sb.regplot(x=x_pm25, y=droped[par_pm25], scatter=False, color='r')
        plt.ylabel(f'Jumlah Partikel {par_pm25}')
        plt.xlabel('Indeks PM2.5')
        plt.legend()
        st.pyplot(plt)
        plt.close()
    
    with st.container():
        st.subheader("Hubungan Indeks PM2.5 dan PM10 dengan Jam")
        jam = sorted(droped['hour'].unique())
        pm_index = st.selectbox('Pilih indeks partikel:', ('PM2.5','PM10'), key='hour_selectbox')

        plt.plot(jam, droped.groupby('hour')[pm_index].mean(), "r-", label=pm_index)
        plt.ylabel(f'indeks {pm_index}')
        plt.xlabel("Pukul (jam)")

        plt.tight_layout()
        st.pyplot(plt)
        plt.close()

    with st.container():
        st.subheader("Hubungan Kecepatan angin dengan variabel waktu, PM2.5 dan PM10")
        col1, col2 = st.columns(2)
        with col1:
            jam = sorted(droped['hour'].unique())
            rataan_wspm = droped.groupby('hour')['WSPM'].mean()
            plt.subplot(1, 3, 1)
            plt.plot(jam, rataan_wspm, "r-", label='Kecepatan Angin')
            plt.ylabel("Kecepatan Angin (m/s)")
            plt.xlabel("Pukul (jam)")
            plt.title("Kecepatan Angin vs Waktu")
            st.pyplot(plt)
            plt.close()
        
        with col2:
            parti_wind = st.selectbox('Pilih indeks yang ingin dilihat:', ('PM2.5', 'PM10'), key='particle_wind_selectbox')
            sb.scatterplot(x=droped[parti_wind], y=droped['WSPM'])
            sb.regplot(x=droped[parti_wind], y=droped['WSPM'], scatter=False, color='r')
            plt.ylim(0, max(droped['WSPM']) + 1)
            plt.ylabel("Kecepatan Angin (m/s)")
            plt.xlabel(f'Indeks : {parti_wind}')
            st.pyplot(plt)
            plt.close()

with tab2:
    st.header("Explaination")
    st.write("Section ini akan membahas pertanyaan analisis yang timbul dari data")
    
    st.header("Pertanyaan 1: Daerah Mana yang memiliki indeks kualitas udara paling baik? dan mengapa? (analisis lanjutan geo analisis)")
    with st.container():
        stasiun = sorted(droped['station'].unique())
        rataan = droped.groupby('station')['PM2.5'].mean()
        rataan2 = droped.groupby('station')['PM10'].mean()

        plt.figure(figsize=(15, 4))
        plt.suptitle("Rerata Indeks PM2.5 dan PM10 di Tiap Stasiun")
        plt.subplot(1, 2, 1)
        plt.bar(stasiun,rataan)
        plt.axhline(y=min(rataan), color='r', linestyle='--',label=f'nilai min')
        plt.axhline(y=max(rataan), color='r', linestyle='--',label=f'nilai max')
        plt.xticks(rotation=60)
        plt.title("rataan index PM2.5 tiap stasiun")
        plt.ylabel("indeks PM2.5")
        plt.xlabel("stasiun")

        plt.subplot(1, 2, 2)
        plt.bar(stasiun,rataan2)
        plt.axhline(y=min(rataan2), color='r', linestyle='--',label=f'nilai min')
        plt.axhline(y=max(rataan2), color='r', linestyle='--',label=f'nilai max')
        plt.xticks(rotation=60)
        plt.title("rataan index PM2.5 tiap stasiun")
        plt.ylabel("indeks PM210")
        plt.xlabel("stasiun")
        plt.show()
        st.pyplot(plt)
        plt.close()  
    
    with st.container():
        st.subheader("Data geospasial untuk PM10 dan PM2.5")
        stasiun = ['Aotizhongxin', 'Changping', 'Dingling', 'Dongsi', 'Guanyuan', 
                'Gucheng', 'Huairou', 'Nongzhanguan', 'Shunyi', 'Tiantan', 
                'Wanliu', 'Wanshouxigong']
        #berdasarkan google map
        koor = {
            'Aotizhongxin': (39.988, 116.407),
            'Changping': (40.217, 116.231),
            'Dingling': (40.296, 116.181),
            'Dongsi': (39.928, 116.417),
            'Guanyuan': (39.933, 116.365),
            'Gucheng': (39.927, 116.202),
            'Huairou': (40.316, 116.637),
            'Nongzhanguan': (39.936, 116.454),
            'Shunyi': (40.126, 116.654),
            'Tiantan': (39.883, 116.412),
            'Wanliu': (39.974, 116.299),
            'Wanshouxigong': (39.886, 116.361)
        }

        rataan = droped.groupby('station')['PM10'].mean()
        rataan_df = rataan.reset_index()

        rataan_df['coordinates'] = rataan_df['station'].map(koor)
        rataan_df['geometry'] = rataan_df['coordinates'].apply(lambda x: Point(x[1], x[0]))

        gdf = gpd.GeoDataFrame(rataan_df, geometry='geometry')
        gdf.set_crs(epsg=4326, inplace=True)

        m = folium.Map(location=[39.9, 116.4], zoom_start=10, tiles='CartoDB positron', 
                        scrollWheelZoom=False, zoom_control=False)

        heat_data = [[point.y, point.x, pm] for point, pm in zip(gdf.geometry, gdf['PM10']) if 80 <= pm <= 120]
        gradient = {
            0.0: 'blue',
            0.4: 'green',
            0.7: 'yellow',     
            1.0: 'red'
        }

        max_pm25 = 90 
        heat_data_scaled = [[point[0], point[1], point[2] / max_pm25] for point in heat_data]

        HeatMap(
            heat_data_scaled, 
            gradient=gradient, 
            radius=25, 
            blur=15
        ).add_to(m)

        for station, (lat, lon) in koor.items():
            pm_value = rataan_df.loc[rataan_df['station'] == station, 'PM10'].values[0]
            folium.Marker(
                location=[lat, lon],
                popup=f"{station}: {pm_value:.2f}",
                icon=folium.Icon(color='blue')
            ).add_to(m)
        m
        
        st_folium(m, width=1000, height=600)
    
    with st.container():
        stasiun = sorted(droped['station'].unique())
        rataan_temp = droped.groupby('station')['TEMP'].mean()
        rataan_pres = droped.groupby('station')['PRES'].mean()
        rataan_o3 = droped.groupby('station')['O3'].mean()

        plt.figure(figsize=(8, 12))
        plt.subplot(3, 1, 1)
        plt.bar(stasiun, rataan_temp, label='TEMPERATUR')
        plt.ylabel("Temperature")
        plt.axhline(y=min(rataan_temp), color='r', linestyle='--', label=f'nilai min')
        plt.xticks([])

        plt.subplot(3, 1, 2)
        plt.bar(stasiun, rataan_pres, label='TEKANAN')
        plt.ylabel("Tekanan")
        plt.axhline(y=min(rataan_pres), color='r', linestyle='--', label=f'nilai min')
        plt.xticks([])
        plt.ylim(min(rataan_pres)-50, max(rataan_pres)+10)

        plt.subplot(3, 1, 3)
        plt.bar(stasiun, rataan_o3, label='O3')
        plt.ylabel("O3")
        plt.xlabel("Stasiun")
        plt.axhline(y=min(rataan_o3), color='r', linestyle='--', label=f'nilai min')
        plt.xticks(rotation=60)

        plt.tight_layout()
        st.pyplot(plt)
        plt.close() 
    st.write("Ketiga daerah terendah dengan indeks polutan udara berdasarkan PM2.5 dan PM.10 adalah Huairou, Dingling, dan Changping. Dari plot temperatur, tekanan, dan O3 menunjukkan (hipotesis) berada pada daerah dataran tinggi. Dataran tinggi cenderung memiliki temperatur yang rendah serta tekanan, hipotesis ini diperkuat dengan tingginya tingkat O3 yang umum pada daerah dataran tinggi Dataran tinggi umumnya memiliki kegiatan industrial dan aktivitas manusia yang lebih rendah dari daerah perkotaan, ini menjadikan salah satu sebab dari mengapa daerah ini memiliki kualitas udara yang lebih baik. Data ini menunjukkan bahwa keadaan sosial dan lingkungan yang berbeda-beda tiap daerah dapat berpengaruh pada baik-buruknya kualitas udara \n Sumber :https://study.com/academy/lesson/the-effect-of-altitude-on-air-pressure.html#:~:text=yet%20closely%20related.-,As%20altitude%20on%20Earth%20increases%2C%20the%20air%20becomes%20less%20dense,the%20pressure%20is%20much%20reduced.)")
    
    st.header("Pertanyaan 2: Unsur kimia mana yang paling berpengaruh terhadap nilai indeks kualitas udara berdasarkan PM2.5 dan PM10?")
    with st.container():
        st.subheader("Hubungan Indeks PM10 dengan Unsur Kimia Berbahaya")
        x_pm10 = droped['PM10']
        parti_pm10 = st.selectbox('Pilih partikel untuk PM10:', ('SO2', 'CO', 'O3', 'NO2'))
        plt.figure(figsize=(10, 6))  
        sb.scatterplot(x=x_pm10, y=droped[parti_pm10])
        sb.regplot(x=x_pm10, y=droped[parti_pm10], scatter=False, color='r')
        plt.ylabel(f'Jumlah Partikel {parti_pm10}')
        plt.xlabel('Indeks PM10')
        plt.legend()
        st.pyplot(plt)
        plt.close()

    with st.container():
        st.subheader("Hubungan Indeks PM2.5 dengan Unsur Kimia Berbahaya")
        x_pm25 = droped['PM2.5']
        parti_pm25 = st.selectbox('Pilih partikel untuk PM2.5:', ('SO2', 'CO', 'O3', 'NO2'))
        plt.figure(figsize=(10, 6))
        sb.scatterplot(x=x_pm25, y=droped[parti_pm25])
        sb.regplot(x=x_pm25, y=droped[parti_pm25], scatter=False, color='r')
        plt.ylabel(f'Jumlah Partikel {parti_pm25}')
        plt.xlabel('Indeks PM2.5')
        plt.legend()
        st.pyplot(plt)
        plt.close()
    st.write("Dengan menggunakan regresi linear dan plotting scatter terdapat hubungan antara beberapa partikel dengan indeks PM2.5 dan PM10. Partikel CO, NO2 dan SO2(walau tak setinggi yang lainya) memiliki hubungan kesetaraan yang positif, artinya ketiga partikel ini menyebabkan peningkatan nilai pada kedua indeks apabila mengalami peningkatan nilai. Sedangkan O3, tidak terlalu berkorelasi, hal ini dihipotesis karena O3 mudah ditemukan pada daerah tinggi dan mudah untuk mengalami pemecahan pada ketinggian tersebut.")
    st.header("Pertanyaan 3: Bagaimana tingkat polusi rata-rata tiap waktunya? dan dipengaruhi oleh apa?")
    with st.container():
        st.subheader("Hubungan Indeks PM2.5 dan PM10 dengan Jam")
        jam = sorted(droped['hour'].unique())
        pm_index = st.selectbox('Pilih indeks partikel:', ('PM2.5','PM10'))

        plt.plot(jam, droped.groupby('hour')[pm_index].mean(), "r-", label=pm_index)
        plt.ylabel(f'indeks {pm_index}')
        plt.xlabel("Pukul (jam)")

        plt.tight_layout()
        st.pyplot(plt)
        plt.close()

    with st.container():
        st.subheader("Hubungan Kecepatan angin dengan variabel waktu, PM2.5 dan PM10")
        col1, col2 = st.columns(2)
        with col1:
            jam = sorted(droped['hour'].unique())
            rataan_wspm = droped.groupby('hour')['WSPM'].mean()
            plt.subplot(1, 3, 1)
            plt.plot(jam, rataan_wspm, "r-", label='Kecepatan Angin')
            plt.ylabel("Kecepatan Angin (m/s)")
            plt.xlabel("Pukul (jam)")
            plt.title("Kecepatan Angin vs Waktu")
            st.pyplot(plt)
            plt.close()
        
        with col2:
            parti_wind = st.selectbox('Pilih indeks yang ingin dilihat:', ('PM2.5', 'PM10'))
            sb.scatterplot(x=droped[parti_wind], y=droped['WSPM'])
            sb.regplot(x=droped[parti_wind], y=droped['WSPM'], scatter=False, color='r')
            plt.ylim(0, max(droped['WSPM']) + 1)
            plt.ylabel("Kecepatan Angin (m/s)")
            plt.xlabel(f'Indeks : {parti_wind}')
            st.pyplot(plt)
            plt.close()
    st.write("Pada plot berdasarkan waktu terlihat bahwa indeks polusi baik PM2.5 dan PM10 mengalami peningkatan pada siang-malam-pagi. Apabila dikaitkan dengan kecepatan udara nilai keduanya berbanding terbalik (walau nilai kedekatan regresinya tak terlalu baik). Hal ini terlihat pada pagi hingga siang, kecepatan udara meningkat dan mencapai titik tertingginya, dan akan menurun setelahnya hingga keesokan harinya. Data ini kemudian menunjukkan bahwa kecepatan angin mampu mereduksi nilai polutan. Hal ini didukung dengan sumber berikut, yang menyatakan bahwa kecepatan angin yang tinggi mampu mengangkat polutan agar tatak terlalu lama berada di area rendah.\nsumber : https://airly.org/en/why-is-air-quality-worse-at-night/#:~:text=During%20the%20day%2C%20the%20sun%20heats%20up%20the%20ground%2C%20causing,and%20settle%20near%20the%20surface.")
