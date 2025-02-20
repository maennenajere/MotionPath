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
#
# --------------------------------------------------------------
# --- 1. Time Interval (Based on Metadata) ---
# Start time: "2025-02-19 13:27:01.115 UTC+02:00"
# End time: "2025-02-19 13:31:20.440 UTC+02:00"
# Time difference: 4 min 19.325 s = 259.325 s

# --- 2. Distance (Calculated from Speed and Time) ---
# Given walking speed: 1.52 m/s (≈ 5.49 km/h)
# Time: 259.325 s (from metadata)
# Distance = 1.52 m/s * 259.325 s = 393.174 m
# GPS distance: 390.15 m
# Difference: 393.17 - 390.15 = 3.02 m
# Small difference

# --- 3. Distance (Calculated from Steps) ---
# Given step count: 467 steps
# Given step length: 0.84 m/step
# Distance 467 * 0.84 = 392.28 m
# GPS distance: 390.15 m
# Difference: 390.15 - 392.28 = -2.13 m

# --- 4. Time (Calculated from GPS Distance and Speed) ---
# Given GPS distance: 390.15 m
# Given speed: 1.52 m/s
# Time 390.15 m / 1.52 m/s = 256.68 s = 4 min 17 s
# Metadata time: 259.325 s
# Difference: 259.325 - 256.68 = 2.645 s
# Small difference

# --- 5. Step Rate and Speed Verification ---
# Given steps: 467
# Time: 256.68 s (GPS)
# Steps per second 467 / 256.68 = 1.819 steps/s
# Steps per minute = 1.819 * 60 = 109.1 steps/min
# Speed from steps = 0.84 m/step * 1.819 steps/s = 1,5279 m/s
# Given speed: 1.52 m/s
# Difference: 1.52 - 1.53 = -0.01 m/s
# Very small difference.

# --- Summary ---
# Metadata-based distance: 393.17 m (speed * time)
# Step-based distance: 392.28 m (steps * step length)
# GPS distance: 390.15 m (given)
# Time comparison: 259.325 s (metadata) vs 256.68 s (GPS-based)
# Speed: 1.52 m/s (given) vs 1.53 m/s (step-based)
# small variations in distances and times, likely due to GPS accuracy and step length.

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, find_peaks
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title='MotionPath', page_icon=':bar_chart:', initial_sidebar_state='expanded')
st.title('PhysicsFinalProject-2025')
st.write('**Soveltava matematiikka ja fysiikka ohjelmoinnissa**')
st.markdown('---')

# CSV data
location_df = pd.read_csv('Location.csv')  # "Time (s)","Latitude (°)","Longitude (°)","Height (m)","Velocity (m/s)","Direction (°)","Horizontal Accuracy (m)","Vertical Accuracy (°)"
accelerometer_df = pd.read_csv('linearAccelerometer.csv')  # "Time (s)","X (m/s^2)","Y (m/s^2)","Z (m/s^2)"

# Average speed
average_speed_m_s = location_df['Velocity (m/s)'].mean()
average_speed_km_h = average_speed_m_s * 3.6
st.write(f'Average speed: {average_speed_km_h:.2f} km/h ({average_speed_m_s:.2f} m/s)')

# Distance
location_df = location_df.dropna(subset=['Time (s)', 'Velocity (m/s)'])
distance = np.trapezoid(location_df['Velocity (m/s)'], location_df['Time (s)'])
st.write(f'Distance travelled: {distance:.2f} m')

# Duration
duration = location_df['Time (s)'].iloc[-1] - location_df['Time (s)'].iloc[0]
st.write(f'Exercise duration: {duration:.2f} s ({duration/60:.2f} min)')

# Suodattimen määrittely
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, nyq, order=5):
    b, a = butter_lowpass(cutoff, fs, order)
    y = filtfilt(b, a, data)
    return y

def butter_highpass_filter(data, cutoff, fs, nyq, order=5):
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    y = filtfilt(b, a, data)
    return y

# Filtterien parametrit
T = accelerometer_df['Time (s)'][len(accelerometer_df['Time (s)'])-1] - accelerometer_df['Time (s)'][0] # Koko datan pituus
n = len(accelerometer_df['Time (s)']) # Datapisteiden lukumäärä
fs = n/T # Näytteenottotaajuus (olettaen vakioksi)
nyq = fs/2 # Nyqvistin taajuus
order = 3 # Kertaluku
cutoff = 1 / 0.05  # Cut-off taajuus

# Suodatetaan data
accelerometer_df['filter_a_x'] = butter_lowpass_filter(accelerometer_df['X (m/s^2)'], cutoff, fs, nyq, order)
accelerometer_df['filter_a_y'] = butter_lowpass_filter(accelerometer_df['Y (m/s^2)'], cutoff, fs, nyq, order)
accelerometer_df['filter_a_z'] = butter_lowpass_filter(accelerometer_df['Z (m/s^2)'], cutoff, fs, nyq, order)

# Step count - Filter
filtered_accel = accelerometer_df['filter_a_z']
peaks, _ = find_peaks(filtered_accel, height=0.5, distance=fs*0.5)
step_count_filtered = len(peaks)

# Step count - Fourier
f = accelerometer_df['filter_a_y']
t = accelerometer_df['Time (s)']
N = len(f)
dt = np.max(t)/N

# Fourier muunnos
fourier = np.fft.fft(f, N)
psd = fourier * np.conj(fourier)/N
freq = np.fft.fftfreq(N, dt)
L = np.arange(1, int(N/2))
step_count_fourier = np.argmax(psd[L].real)

st.write(f"Step count from filtered data: {step_count_filtered}")
st.write(f"Step count from Fourier analysis: {step_count_fourier}")

# Step length
distance = np.trapz(location_df['Velocity (m/s)'], location_df['Time (s)'])
if step_count_filtered > 0:
    step_length = distance / step_count_filtered
    st.write(f'Step length (filtered): {step_length:.2f} m')
else:
    st.write("Step length (filtered): null")

if step_count_fourier > 0:
    step_length_fourier = distance / step_count_fourier
    st.write(f'Step length (Fourier): {step_length_fourier:.2f} m')
else:
    st.write("Step length (Fourier): null")

st.markdown('---')

# Plot filtered acceleration data
st.subheader('Filtered Acceleration Data')
plt.figure(figsize=(14, 10))

# X
plt.subplot(3, 1, 1)
plt.plot(accelerometer_df['Time (s)'], accelerometer_df['filter_a_x'], linestyle='-', label='Filtered X (m/s²)')
plt.xlabel('Time (s)', fontsize=12)
plt.ylabel('Acceleration (m/s²)', fontsize=12)
plt.title('Filtered Acceleration Data (X-axis)', fontsize=14, fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.7)

# Y
plt.subplot(3, 1, 2)
plt.plot(accelerometer_df['Time (s)'], accelerometer_df['filter_a_y'], linestyle='-', label='Filtered Y (m/s²)')
plt.xlabel('Time (s)', fontsize=12)
plt.ylabel('Acceleration (m/s²)', fontsize=12)
plt.title('Filtered Acceleration Data (Y-axis)', fontsize=14, fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.7)

# Z
plt.subplot(3, 1, 3)
plt.plot(accelerometer_df['Time (s)'], accelerometer_df['filter_a_z'], linestyle='-', label='Filtered Z (m/s²)')
plt.xlabel('Time (s)', fontsize=12)
plt.ylabel('Acceleration (m/s²)', fontsize=12)
plt.title('Filtered Acceleration Data (Z-axis)', fontsize=14, fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout(pad=3.0)
st.pyplot(plt)

# Power Spectral Density X-axis
st.subheader('Power Spectral Density (Y-axis)')
f = accelerometer_df['filter_a_y']  # Suodatettu signaali
N = len(f)                          # Havaintojen määrä
fourier = np.fft.fft(f, N)           # Fourier muunnos
psd = fourier * np.conj(fourier)/N   # Power Spectral Density
freq = np.fft.fftfreq(N, dt)         # Taajuudet
L = np.arange(1, N // 2)             # Rajataan taajuudet
f_max = freq[L][np.argmax(psd[L].real)]

plt.figure(figsize=(10, 5))
plt.plot(freq[L], psd[L].real, linestyle="solid", color="black", linewidth=1)
plt.xlim([0, 50])
plt.xlabel('Frequency [Hz]')
plt.ylabel('Power')
plt.title('Power Spectral Density (PSD)')
plt.grid()
st.pyplot(plt)
st.write(f'Most powerful frequency: {f_max:.2f} Hz')

# Route on the map
st.subheader('Route on the Map')
start_coords = (location_df["Latitude (°)"].iloc[0], location_df["Longitude (°)"].iloc[0])
end_coords = (location_df["Latitude (°)"].iloc[-1], location_df["Longitude (°)"].iloc[-1])
m = folium.Map(location=start_coords, zoom_start=15)
route = list(zip(location_df["Latitude (°)"], location_df["Longitude (°)"]))
folium.PolyLine(route, color='red', weight=3.5, opacity=1).add_to(m)
folium.Marker(start_coords, popup='Start', icon=folium.Icon(color='green')).add_to(m)
folium.Marker(end_coords, popup='End', icon=folium.Icon(color='red')).add_to(m)
st_folium(m, width=900, height=700)

st.markdown('---')

# some data tables
st.subheader('Location Data')
st.write(location_df)
st.subheader('Accelerometer Data')
st.write(accelerometer_df)

st.markdown('---')