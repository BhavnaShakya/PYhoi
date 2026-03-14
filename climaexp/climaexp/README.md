# 🌍 PyClimaExplorer

PyClimaExplorer is a rapid-prototype interactive visualizer for multidimensional climate model data (e.g., NetCDF files from CESM or ERA5 reanalysis). It allows researchers and the general public to easily upload, slice, dice, and view complex spatial and temporal dimensions of climate data in real-time.

## 🎯 Addressing the "Scientific Understanding" Goal
Visualizing complex simulation output is crucial for both scientific understanding and public outreach. PyClimaExplorer addresses these goals by providing:
- **Instant Accessibility:** With a dynamic data loader, users don't need to write Python code to inspect NetCDF files. Upload and instantly get visual feedback.
- **Scientific Highlighting via Comparison Mode:** Easily contrast two different time periods (e.g., 1990 vs 2020) and calculate their anomaly/difference to uncover key climate trends.
- **Multidimensional Splicing:** Interactive UI allows non-experts to drill down to local temporal behaviors or zoom out for a global spatial heat map.
- **Self-Healing Features:** Uses intuitive coordinate inference to handle NetCDF data sets even if dimension naming conventions vary slightly across standard formats (latitude vs lat vs y).

## 🚀 Features
- **Dynamic Data Loader:** Supports fast loading via `xarray` and netCDF4 backends. Falls back to a tutorial dataset (`air_temperature`) for instant demonstration.
- **Spatial View:** Global projection using Plotly showing the 2D distribution at a specific time step. 
- **Temporal View:** See what a specific grid box (Latitude, Longitude) experiences over time.
- **Comparison Mode:** Compare datasets and view raw data anomalies side-by-side.
- **Dark Scientific Aesthetic:** Ensures that visuals stand out and follow modern analytical application trends.

## 🛠️ Installation & Usage

1. **Prerequisites**
   Ensure you have Python 3.11+ installed.
   
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
3. **Run the Dashboard**
   ```bash
   streamlit run app.py
   ```
   
4. **Access the Application**
   Open your browser to the URL output by Streamlit (typically `http://localhost:8501`).
   
## 📂 Sample Data
You can test out the functionality without any data using the built-in `xarray` tutorial dataset.
For real-world NetCDF files, try downloading outputs from:
- [CESM Climate Variability and Predictability project](https://www.cesm.ucar.edu/projects/cvdp/data-repository)
- Any Copernicus/ERA5 Reanalysis public dumps.
