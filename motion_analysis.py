# Analyysi ja visualisointi
#
# Tutki, missä kiihtyvyyden komponentissa kävelyliike havaitaan parhaiten, valitse se analyysiin kiihtyvyyden osalta.
#
# Määrittele havainnoista kurssilla oppimasi perusteella seuraavat asiat ja esitä ne numeroina visualisoinnissasi:
# - Askelmäärä laskettuna suodatetusta kiihtyvyysdatasta
# - Askelmäärä laskettuna kiihtyvyysdatasta Fourier-analyysin perusteella
# - Keskinopeus (GPS-datasta)
# - Kuljettu matka (GPS-datasta)
# - Askelpituus (lasketun askelmäärän ja matkan perusteella)
#
# -Esitä seuraavat kuvaajat-
#
# Suodatettu kiihtyvyysdata, jota käytit askelmäärän määrittelemiseen.
# Analyysiin valitun kiihtyvyysdatan komponentin tehospektritiheys
# Reittisi kartalla
# --------------------------------------------------------------
# Alkuperäinen aikaväli metadatan perusteella:
# Start: "2025-02-18 17:40:27.666"
# End: "2025-02-18 17:49:58.077"
# Aikaväli = 9 min 30.411 s = 570.411 s

# Kävelynopeus on 1.44 m/s, mikä on noin 5.20 km/h.
# Matka = 1.44 m/s * 570.411 s = 821.79 m (itse)
# Matka = 815.59 m (GPS-datasta laskettu)
# Ero noin 6.20 m. Voi johtua siitä, että GPS-datasta puuttuu joitain pisteitä tuottaen virheitä.

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import butter, filtfilt
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title='MotionPath', page_icon=':bar_chart:', initial_sidebar_state='expanded')
st.title('PhysicsFinalProject-2025')

# CSV data
location_df = pd.read_csv('Location.csv')  # "Time (s)","Latitude (°)","Longitude (°)","Height (m)","Velocity (m/s)","Direction (°)","Horizontal Accuracy (m)","Vertical Accuracy (°)"
accelerometer_df = pd.read_csv('linearAccelerometer.csv')  # "Time (s)","X (m/s^2)","Y (m/s^2)","Z (m/s^2)"

# Average speed (from GPS data) | Fun fact: average walking speed for humans is 1.4 m/s
average_speed_m_s = location_df['Velocity (m/s)'].mean()
average_speed_km_h = average_speed_m_s * 3.6
st.write(f'Average speed: {average_speed_km_h:.2f} km/h ({average_speed_m_s:.2f} m/s)')

# Distance travelled (from GPS data)
location_df = location_df.dropna(subset=['Time (s)', 'Velocity (m/s)'])
distance = np.trapezoid(location_df['Velocity (m/s)'], location_df['Time (s)'])
st.write(f'Distance travelled: {distance:.2f} m')

#Tuodaan filtterifunktiot
def butter_lowpass_filter(data, cutoff, fs, nyq, order):
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

def butter_highpass_filter(data, cutoff, fs, nyq, order):
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    y = filtfilt(b, a, data)
    return y

#Filtterien parametrit
T = accelerometer_df['Time (s)'][len(accelerometer_df['Time (s)'])-1] - accelerometer_df['Time (s)'][0] #Koko datan pituus
n = len(accelerometer_df['Time (s)']) #Datapisteiden lukumäärä
fs = n / T #Näytteenottotaajuus (olettaen vakioksi)
nyq = fs / 2 #Nyqvistin taajuus
order = 3 #Kertaluku
cutoff = 1/(0.05) #Cut-off taajuus

# Apply the low-pass filter
accelerometer_df['X (m/s^2)'] = butter_lowpass_filter(accelerometer_df['X (m/s^2)'], cutoff, fs, nyq, order)
accelerometer_df['Y (m/s^2)'] = butter_lowpass_filter(accelerometer_df['Y (m/s^2)'], cutoff, fs, nyq, order)
accelerometer_df['Z (m/s^2)'] = butter_lowpass_filter(accelerometer_df['Z (m/s^2)'], cutoff, fs, nyq, order)

# Plot the filtered acceleration data
st.subheader('Filtered Acceleration Data (X-axis)')
st.line_chart(
    accelerometer_df[['Time (s)', 'X (m/s^2)']],
    x='Time (s)',
    y='X (m/s^2)',
    y_label='Acceleration (m/s²)',
    x_label='Time (s)'
)
st.subheader('Filtered Acceleration Data (Y-axis)')
st.line_chart(
    accelerometer_df[['Time (s)', 'Y (m/s^2)']],
    x='Time (s)',
    y='Y (m/s^2)',
    y_label='Acceleration (m/s²)',
    x_label='Time (s)'
)
st.subheader('Filtered Acceleration Data (Z-axis)')
st.line_chart(
    accelerometer_df[['Time (s)', 'Z (m/s^2)']],
    x='Time (s)',
    y='Z (m/s^2)',
    y_label='Acceleration (m/s²)',
    x_label='Time (s)'
)

# Tehospektri
st.subheader('Tehospektri')
# chart_data = pd.DataFrame(np.transpose(np.array([freq[L],psd[L].real])), columns=["freq", "psd"])
# st.line_chart(chart_data,x = 'freq', y = 'psd' , y_label = 'Teho',x_label = 'Taajuus [Hz]')

# Plot the route on the map
st.subheader('Route on the Map')
start_coords = (location_df["Latitude (°)"].iloc[0], location_df["Longitude (°)"].iloc[0])
m = folium.Map(location=start_coords, zoom_start=15)
route = list(zip(location_df["Latitude (°)"], location_df["Longitude (°)"]))
folium.PolyLine(route, color='red', weight=3.5, opacity=1).add_to(m)
st_folium(m, width=900, height=650)