import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import xarray as xr
from data_loader import load_dataset, standardize_dims

# Page config
st.set_page_config(
    page_title="PyClimaExplorer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme CSS for high-tech scientific look
st.markdown("""
    <style>
    /* Main app background */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    /* Header styling */
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-family: 'Inter', sans-serif;
    }
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌍 PyClimaExplorer Dashboard")
st.markdown("### Interactive visualization of multidimensional NetCDF climate data")

# -- SIDEBAR --
st.sidebar.header("📁 Data Loader")
uploaded_file = st.sidebar.file_uploader("Upload NetCDF (.nc)", type=['nc'])

@st.cache_resource
def get_cached_dataset(file_bytes=None):
    # To handle uploaded file safely with cache
    # We pass bytes instead of UploadedFile object
    class DummyUploader:
        def __init__(self, b):
            self.bytes = b
        def getvalue(self):
            return self.bytes
            
    if file_bytes is not None:
        return load_dataset(DummyUploader(file_bytes))
    return load_dataset(None)

file_bytes = uploaded_file.getvalue() if uploaded_file is not None else None

try:
    with st.spinner("Loading dataset..."):
        ds = get_cached_dataset(file_bytes)
        
    st.sidebar.success("Dataset loaded successfully!")
    
    # Identify variables
    # Filter out variables that don't have lat/lon/time
    data_vars = [v for v in ds.data_vars if len(ds[v].dims) >= 2]
    if not data_vars:
        st.error("No valid multi-dimensional variables found in dataset.")
        st.stop()
        
    selected_var = st.sidebar.selectbox("Select Variable", options=data_vars)
    
    # Detect dimensions
    has_time = 'time' in ds[selected_var].dims
    
    if has_time:
        times = ds['time'].values
        # Convert times to a readable format if they are datetime64
        if np.issubdtype(times.dtype, np.datetime64):
            times_str = pd.to_datetime(times).strftime('%Y-%m-%d %H:%M')
        else:
            times_str = [str(t) for t in times]
            
        st.sidebar.subheader("Temporal Selection")
        selected_time_idx = st.sidebar.slider("Select Time Slice", 0, len(times)-1, 0)
        selected_time = times[selected_time_idx]
        st.sidebar.text(f"Current Time: {times_str[selected_time_idx]}")
    else:
        selected_time = None

    # App Modes
    app_mode = st.radio("Select View Mode", ["Standard View", "Comparison Mode (Anomalies)"], horizontal=True)
    
    # ---------------------------------------------------------
    # STANDARD VIEW
    # ---------------------------------------------------------
    if app_mode == "Standard View":
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.subheader(f"Global Heatmap: {selected_var}")
            # Spatial View using Plotly imshow
            if has_time:
                data_slice = ds[selected_var].isel(time=selected_time_idx)
            else:
                data_slice = ds[selected_var]
                
            fig_spatial = px.imshow(
                data_slice.values,
                x=ds['lon'].values if 'lon' in data_slice.dims else None,
                y=ds['lat'].values if 'lat' in data_slice.dims else None,
                color_continuous_scale="Viridis",
                origin="lower",
                labels={'color': selected_var}
            )
            fig_spatial.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color="white",
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig_spatial, use_container_width=True)
            
        with col2:
            st.subheader("Temporal Line Chart")
            if has_time:
                # Let user pick a point
                if 'lat' in ds.dims and 'lon' in ds.dims:
                    lat_opts = ds['lat'].values
                    lon_opts = ds['lon'].values
                    
                    sub_col1, sub_col2 = st.columns(2)
                    with sub_col1:
                        sel_lat_idx = st.number_input("Lat Index", min_value=0, max_value=len(lat_opts)-1, value=len(lat_opts)//2)
                    with sub_col2:
                        sel_lon_idx = st.number_input("Lon Index", min_value=0, max_value=len(lon_opts)-1, value=len(lon_opts)//2)
                        
                    sel_lat = lat_opts[sel_lat_idx]
                    sel_lon = lon_opts[sel_lon_idx]
                    
                    st.write(f"Showing series for Lat: {sel_lat:.2f}, Lon: {sel_lon:.2f}")
                    
                    ts_data = ds[selected_var].isel(lat=sel_lat_idx, lon=sel_lon_idx)
                    
                    fig_ts = px.line(
                        x=times, 
                        y=ts_data.values,
                        labels={'x': 'Time', 'y': selected_var},
                        template="plotly_dark"
                    )
                    fig_ts.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                    )
                    st.plotly_chart(fig_ts, use_container_width=True)
            else:
                st.info("Dataset variable does not have a time dimension.")
                
    # ---------------------------------------------------------
    # COMPARISON MODE
    # ---------------------------------------------------------
    elif app_mode == "Comparison Mode (Anomalies)":
        if not has_time:
            st.warning("Comparison mode requires a time dimension.")
        else:
            st.subheader("Compare Two Time Periods")
            time_col1, time_col2 = st.columns(2)
            with time_col1:
                t1_idx = st.slider("Time Period 1", 0, len(times)-1, 0, key="t1")
                st.write(f"**{times_str[t1_idx]}**")
            with time_col2:
                t2_idx = st.slider("Time Period 2", 0, len(times)-1, len(times)//2, key="t2")
                st.write(f"**{times_str[t2_idx]}**")
                
            map_col1, map_col2 = st.columns(2)
            
            slice1 = ds[selected_var].isel(time=t1_idx)
            slice2 = ds[selected_var].isel(time=t2_idx)
            anomaly = slice2 - slice1
            
            with map_col1:
                st.markdown(f"**{selected_var} at {times_str[t1_idx]}**")
                fig1 = px.imshow(
                    slice1.values, x=ds['lon'].values, y=ds['lat'].values,
                    color_continuous_scale="Viridis", origin="lower"
                )
                fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig1, use_container_width=True)
                
            with map_col2:
                st.markdown(f"**{selected_var} at {times_str[t2_idx]}**")
                fig2 = px.imshow(
                    slice2.values, x=ds['lon'].values, y=ds['lat'].values,
                    color_continuous_scale="Viridis", origin="lower"
                )
                fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig2, use_container_width=True)
                
            st.markdown("### Anomaly (Period 2 - Period 1)")
            fig_anomaly = px.imshow(
                anomaly.values, x=ds['lon'].values, y=ds['lat'].values,
                color_continuous_scale="RdBu_r", origin="lower",
                zmin=-np.max(np.abs(anomaly.values)), zmax=np.max(np.abs(anomaly.values))
            )
            fig_anomaly.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig_anomaly, use_container_width=True)

except Exception as e:
    st.error(f"Error processing dataset: {str(e)}")
