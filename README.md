# MotionPath

This project uses measured GPS and acceleration data to visualize movement with Streamlit.
It acts as a prototype for a sports app designed to analyze motion during exercise.
The data was collected using a smartphone with the phypox app.

## Features

- **Step Count**
- **Fourier Analysis**
- **Average Speed**
- **Distance Traveled**
- **Step Length**
- **Visualizations and route on the map**

## Data Files
- `Location.csv`
- `linearAccelerometer.csv`

## Installation
1. Clone the repository:
    ```sh
    git clone https://https://github.com/maennenajere/MotionPath.git
    cd MotionPath
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Collect some data (Linear Accelerometer and Location) with e.g. the `phypox` app.

2. Place the `Location.csv` and `linearAccelerometer.csv` files in the project folder.

3. Run the Streamlit application:
    ```sh
    streamlit run motion_analysis.py
    ```
4. Open the provided URL in your web browser.

## Analysis and Visualization
The analysis includes the following steps:

1. **Step Count**:
   - Calculated from filtered acceleration data.
   - Calculated from acceleration data using Fourier analysis.

2. **Average Speed**:
   - Calculated from GPS data.

3. **Distance Traveled**:
   - Calculated from GPS data.

4. **Step Length**:
   - Calculated from the step count and distance traveled.

### Visualizations
- Filtered acceleration data used for step count determination.
- Power spectral density of the selected acceleration component.
- Route on the map