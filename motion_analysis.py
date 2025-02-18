# -Analyysi ja visualisointi-
#
# Tutki, missä kiihtyvyyden komponentissa kävelyliike havaitaan parhaiten, valitse se analyysiin kiihtyvyyden osalta.
# Määrittele havainnoista kurssilla oppimasi perusteella seuraavat asiat ja esitä ne numeroina visualisoinnissasi:
# Number of steps calculated from filtered acceleration data
# Step rate calculated from acceleration data using Fourier analysis
# Average speed (from GPS data)
# Distance travelled (from GPS data)
# Stride length (based on calculated stride rate and distance)

# - Show the following graphs -
# The filtered acceleration data that you used to determine the number of steps.
# Power spectral density of the component of the acceleration data selected for analysis
# Your route on the map

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import butter, filtfilt
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title='MotionPath', page_icon=':bar_chart:', layout='wide', initial_sidebar_state='expanded')
st.title('PhysicsFinalProject-2025')

# CSV files
location_df = pd.read_csv('Location.csv')  # "Time (s)","Latitude (°)","Longitude (°)","Height (m)","Velocity (m/s)","Direction (°)","Horizontal Accuracy (m)","Vertical Accuracy (°)"
accelerometer_df = pd.read_csv('linearAccelerometer.csv')  # "Time (s)","X (m/s^2)","Y (m/s^2)","Z (m/s^2)"

# low-pass filter
def butter_lowpass_filter(data, cutoff, fs, nyq, order):
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

# high-pass filter
def butter_highpass_filter(data, cutoff, fs, nyq, order):
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    y = filtfilt(b, a, data)
    return y

# Filter parameters
T = accelerometer_df['Time (s)'][len(accelerometer_df['Time (s)'])-1] - accelerometer_df['Time (s)'][0] # Whole data length
n = len(accelerometer_df['Time (s)']) # Data points
fs = n/T # Data sampling frequency (assuming constant)
order = 3 # Order
cutoff = 1/(0.05) # Cut-off frequency

# Number of steps calculated from filtered acceleration data

# Step rate calculated from acceleration data using Fourier analysis

# Average speed (from GPS data)
average_speed = location_df['Velocity (m/s)'].mean()
st.write(f'Average speed: {average_speed:.2f} m/s')

# Distance travelled (from GPS data)

# Stride length (based on calculated stride rate and distance)


# The filtered acceleration data that you used to determine the number of steps.
st.subheader('The filtered acceleration data that you used to determine the number of steps.')

# Power spectral density of the component of the acceleration data selected for analysis
st.subheader('Power spectral density of the component of the acceleration data selected for analysis')

# route on the map
st.subheader('Route on the map')
start_coords = (location_df["Latitude (°)"].iloc[0], location_df["Longitude (°)"].iloc[0])
m = folium.Map(location=start_coords, zoom_start=15)
route = list(zip(location_df["Latitude (°)"], location_df["Longitude (°)"]))
folium.PolyLine(route, color="red", weight=2.5, opacity=0.8).add_to(m)
st_folium(m, width=700, height=500)