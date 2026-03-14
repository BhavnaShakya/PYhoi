import streamlit as st
import data_engine
import plotly.express as px
import pandas as pd
import numpy as np
import xarray as xr

# Streamlit Page Config
st.set_page_config(page_title="PyClimaExplorer", layout="wide", page_icon="🌍")

# Custom CSS for dark aesthetic
st.markdown("""
    <style>
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }
    .stPlotlyChart {
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌍 PyClimaExplorer Dashboard")
st.markdown("*Interactive visualizer for multi-dimensional climate model data (NetCDF)*")

# Sidebar - Data Loading & Slicing
st.sidebar.header("📁 Data Loader")
uploaded_file = st.sidebar.file_uploader("Upload a NetCDF file (.nc)", type=["nc"])

@st.cache_data
def load_and_cache_data(file_info):
    # Using a dummy argument `file_info` to trigger reload when a new file is uploaded
    return data_engine.load_dataset(uploaded_file)

# We use the file name and size as cache key. If no file, use default string.
file_key = f"{uploaded_file.name}-{uploaded_file.size}" if uploaded_file else "default-tutorial"
with st.spinner("Loading scientific dataset..."):
    ds = load_and_cache_data(file_key)

st.sidebar.success("Dataset loaded successfully!")

# Slicer controls
st.sidebar.header("🛠️ Multidimensional Slicer")
vars_list = data_engine.get_data_vars(ds)

if not vars_list:
    st.error("No valid 2D/3D variables found in the dataset.")
    st.stop()

selected_var = st.sidebar.selectbox("Select Variable to Visualize", vars_list)

# Determine the dimensions available for this variable
var_da = ds[selected_var]
has_time = 'time' in var_da.dims
has_latlon = 'lat' in var_da.dims and 'lon' in var_da.dims

st.sidebar.subheader("Spatial View Controls")
if has_time:
    time_vals = pd.to_datetime(var_da['time'].values)
    
    # Check if time_vals is empty or scalar
    if len(time_vals) > 0:
        # Use simple date strings
        time_options = time_vals.strftime('%Y-%m-%d %H:%M:%S').tolist()
        selected_time_idx = st.sidebar.slider("Select Time Slice", 0, len(time_options)-1, 0)
        selected_time = var_da['time'].values[selected_time_idx]
        display_time = time_options[selected_time_idx]
    else:
        selected_time = var_da['time'].values
        display_time = str(selected_time)
else:
    selected_time = None
    display_time = "N/A"

st.sidebar.subheader("Temporal View Controls")
if has_latlon:
    lat_vals = var_da['lat'].values
    lon_vals = var_da['lon'].values
    # Fallback default coordinates (center of the dataset)
    default_lat_idx = len(lat_vals) // 2
    default_lon_idx = len(lon_vals) // 2
    
    selected_lat = st.sidebar.select_slider("Select Latitude", options=np.round(lat_vals, 2), value=np.round(lat_vals[default_lat_idx], 2))
    selected_lon = st.sidebar.select_slider("Select Longitude", options=np.round(lon_vals, 2), value=np.round(lon_vals[default_lon_idx], 2))
else:
    selected_lat, selected_lon = None, None

# Main Dashboard layout
st.header("Visualizations")

# 1. Spatial View
st.subheader("🗺️ Global Spatial View")
with st.container():
    if has_latlon:
        if has_time:
            map_data = data_engine.extract_map_slice(ds, selected_var, selected_time)
            title=f"{selected_var} Distribution on {display_time}"
        else:
            map_data = var_da
            title=f"{selected_var} Distribution"
            
        fig_map = px.imshow(
            map_data.values,
            x=map_data['lon'].values,
            y=map_data['lat'].values,
            color_continuous_scale="Viridis",
            origin='lower',
            labels={'color': selected_var},
            title=title
        )
        fig_map.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Longitude",
            yaxis_title="Latitude"
        )
        st.plotly_chart(fig_map, width="stretch")
    else:
        st.warning("Spatial dimensions (lat/lon) missing for this variable.")

# 2. Temporal View
st.subheader("📈 Local Temporal View")
with st.container():
    if has_time and has_latlon:
        # Extract time series at selected lat/lon
        ts_data = data_engine.extract_time_series(ds, selected_var, selected_lat, selected_lon)
        
        if ts_data is not None:
            df_ts = pd.DataFrame({
                'Time': pd.to_datetime(ts_data['time'].values),
                selected_var: ts_data.values
            })
            
            fig_ts = px.line(
                df_ts, x='Time', y=selected_var,
                title=f"{selected_var} over Time at (Lat: {selected_lat}, Lon: {selected_lon})",
                markers=True
            )
            fig_ts.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            fig_ts.update_traces(line_color="#00b4d4")
            st.plotly_chart(fig_ts, width="stretch")
    else:
        st.warning("Time or spatial dimensions missing for this variable; cannot generate time-series.")

# Bonus: Comparison Mode
st.markdown("---")
st.header("🔍 Comparison Mode (Side-by-Side Analysis)")
compare_on = st.checkbox("Enable Comparison Mode")

if compare_on and has_time and has_latlon:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Period A")
        time_idx_a = st.selectbox("Select Time A", range(len(time_options)), format_func=lambda x: time_options[x], key='time_a')
        time_a = var_da['time'].values[time_idx_a]
        map_a = data_engine.extract_map_slice(ds, selected_var, time_a)
        fig_a = px.imshow(
            map_a.values, x=map_a['lon'].values, y=map_a['lat'].values, 
            color_continuous_scale="Plasma", origin='lower', title=f"Dataset at {time_options[time_idx_a]}"
        )
        fig_a.update_layout(template="plotly_dark", margin=dict(l=0,r=0,b=0,t=40))
        st.plotly_chart(fig_a, width="stretch")

    with col2:
        st.markdown("### Period B")
        time_idx_b = st.selectbox("Select Time B", range(len(time_options)), format_func=lambda x: time_options[x], key='time_b', index=min(1, len(time_options)-1))
        time_b = var_da['time'].values[time_idx_b]
        map_b = data_engine.extract_map_slice(ds, selected_var, time_b)
        fig_b = px.imshow(
            map_b.values, x=map_b['lon'].values, y=map_b['lat'].values, 
            color_continuous_scale="Plasma", origin='lower', title=f"Dataset at {time_options[time_idx_b]}"
        )
        fig_b.update_layout(template="plotly_dark", margin=dict(l=0,r=0,b=0,t=40))
        st.plotly_chart(fig_b, width="stretch")
        
    st.markdown("### 🧮 Anomaly (Period B minus Period A)")
    anomaly = data_engine.compute_anomaly(ds, selected_var, time_a, time_b)
    
    # Find max absolute anomaly to center colorscale at 0
    max_abs = float(np.abs(np.nanmax(anomaly.values)))
    
    fig_diff = px.imshow(
        anomaly.values,
        x=anomaly['lon'].values,
        y=anomaly['lat'].values,
        color_continuous_scale="RdBu_r",
        zmin=-max_abs,
        zmax=max_abs,
        origin='lower',
        title=f"Anomaly: {time_options[time_idx_b]} vs {time_options[time_idx_a]}"
    )
    fig_diff.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_diff, width="stretch")
elif compare_on:
    st.info("Comparison mode requires 'time', 'lat', and 'lon' dimensions.")
