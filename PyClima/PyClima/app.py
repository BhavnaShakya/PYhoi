import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="PyClimaExplorer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #2e3241;
    }
    .insight-card {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #00d4ff;
        margin: 10px 0;
    }
    h1, h2, h3 {
        color: #00d4ff;
    }
    .stButton>button {
        background-color: #00d4ff;
        color: #0e1117;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 24px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #00a8cc;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_location' not in st.session_state:
    st.session_state.selected_location = None
if 'selected_coords' not in st.session_state:
    st.session_state.selected_coords = None

# Generate synthetic climate data up to 2026
@st.cache_data
def generate_climate_data():
    np.random.seed(42)
    
    lats = np.linspace(-90, 90, 30)
    lons = np.linspace(-180, 180, 60)
    years_range = np.arange(1970, 2027)  # up to 2026
    
    data = []
    for year in years_range:
        for lat in lats:
            for lon in lons:
                base_temp = 15 + 20 * np.cos(np.radians(lat))
                trend = (year - 1970) * 0.02
                temp = base_temp + trend + np.random.normal(0, 2)
                
                precip = max(0, 100 + 50 * np.sin(np.radians(lat)) + np.random.normal(0, 20))
                wind = max(0, 10 + 5 * abs(np.sin(np.radians(lat))) + np.random.normal(0, 2))
                
                data.append({
                    'year': year,
                    'lat': lat,
                    'lon': lon,
                    'temperature': temp,
                    'precipitation': precip,
                    'wind_speed': wind
                })
    
    return pd.DataFrame(data)

# Generate predictions using linear regression + user assumptions
@st.cache_data
def generate_predictions(historical_data, years_ahead=30, scenario_mult=1.0,
                         temp_sensitivity=0.2, precip_change=0):
    from sklearn.linear_model import LinearRegression
    
    predictions = []
    
    for lat in historical_data['lat'].unique():
        for lon in historical_data['lon'].unique():
            subset = historical_data[(historical_data['lat'] == lat) & 
                                    (historical_data['lon'] == lon)]
            
            if len(subset) > 0:
                X = subset[['year']].values
                base_year = X.max()
                future_years = np.arange(base_year + 1, base_year + years_ahead + 1).reshape(-1, 1)

                for var in ['temperature', 'precipitation', 'wind_speed']:
                    y = subset[var].values
                    model = LinearRegression()
                    model.fit(X, y)
                    future_values = model.predict(future_years).copy()

                    # Apply assumption adjustments
                    decades = (future_years.flatten() - base_year) / 10
                    if var == 'temperature':
                        future_values += decades * temp_sensitivity * scenario_mult
                    elif var == 'precipitation':
                        future_values *= (1 + (precip_change / 100) * scenario_mult) ** decades

                    for i, year in enumerate(future_years.flatten()):
                        predictions.append({
                            'year': year,
                            'lat': lat,
                            'lon': lon,
                            var: future_values[i]
                        })
    
    return pd.DataFrame(predictions)

# AI-powered insights
def generate_insights(data, variable):
    insights = []
    
    # Trend analysis
    recent = data[data['year'] >= data['year'].max() - 10][variable].mean()
    old = data[data['year'] <= data['year'].min() + 10][variable].mean()
    change = ((recent - old) / old) * 100
    
    if variable == 'temperature':
        if change > 5:
            insights.append(f"🔥 Critical warming detected: {change:.1f}% increase over the period")
        elif change > 0:
            insights.append(f"📈 Temperature rising: {change:.1f}% increase observed")
    elif variable == 'precipitation':
        if abs(change) > 10:
            insights.append(f"💧 Significant precipitation change: {change:.1f}% variation")
    
    # Anomaly detection
    mean_val = data[variable].mean()
    std_val = data[variable].std()
    anomalies = data[abs(data[variable] - mean_val) > 2 * std_val]
    
    if len(anomalies) > 0:
        insights.append(f"⚠️ {len(anomalies)} anomalous readings detected ({len(anomalies)/len(data)*100:.1f}% of data)")
    
    # Regional patterns
    if 'lat' in data.columns:
        tropical = data[abs(data['lat']) < 23.5][variable].mean()
        polar = data[abs(data['lat']) > 66.5][variable].mean()
        
        if variable == 'temperature':
            insights.append(f"🌡️ Tropical regions: {tropical:.1f}°C | Polar regions: {polar:.1f}°C")
    
    return insights

# Sidebar
with st.sidebar:
    st.title("🌍 PyClimaExplorer")
    st.markdown("---")
    
    # Dataset selection
    st.subheader("Dataset")
    dataset = st.selectbox("Select Dataset", ["Global Climate Model", "Historical Records"])

    # File upload
    st.subheader("Upload Dataset")
    uploaded_file = st.file_uploader(
        "Upload NetCDF file",
        type=["nc"],
        help="Upload any NetCDF (.nc) file — you'll map its variables after upload"
    )
    if uploaded_file:
        try:
            import xarray as xr
            import tempfile, os
            tmp = tempfile.NamedTemporaryFile(suffix=".nc", delete=False)
            tmp.write(uploaded_file.read())
            tmp.close()
            tmp_path = tmp.name
            try:
                ds = xr.open_dataset(tmp_path)
                file_vars = list(ds.data_vars)
                file_dims = list(ds.dims)
                all_options = file_vars + file_dims
                ds.close()
            finally:
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass

            st.caption(f"Variables found: `{', '.join(file_vars)}` | Dims: `{', '.join(file_dims)}`")

            # Let user map variables
            st.markdown("**Map your variables:**")
            mc1, mc2 = st.columns(2)
            with mc1:
                map_temp  = st.selectbox("Temperature variable",  all_options, key="map_temp")
                map_precip = st.selectbox("Precipitation variable", all_options, key="map_precip")
            with mc2:
                map_wind  = st.selectbox("Wind Speed variable",   all_options, key="map_wind")
                map_lat   = st.selectbox("Latitude dim/var",      all_options, key="map_lat")
            mc3, mc4 = st.columns(2)
            with mc3:
                map_lon  = st.selectbox("Longitude dim/var", all_options, key="map_lon")
            with mc4:
                map_year = st.selectbox("Year/Time dim/var", all_options, key="map_year")

            if st.button("✅ Load Dataset", use_container_width=True):
                tmp2 = tempfile.NamedTemporaryFile(suffix=".nc", delete=False)
                uploaded_file.seek(0)
                tmp2.write(uploaded_file.read())
                tmp2.close()
                try:
                    ds2 = xr.open_dataset(tmp2.name)
                    rename_map = {
                        map_temp: 'temperature',
                        map_precip: 'precipitation',
                        map_wind: 'wind_speed',
                    }
                    # only rename vars that exist and differ
                    rename_map = {k: v for k, v in rename_map.items() if k in ds2.data_vars and k != v}
                    ds2 = ds2.rename(rename_map)
                    df = ds2[['temperature', 'precipitation', 'wind_speed']].to_dataframe().reset_index()
                    ds2.close()
                    dim_rename = {map_lat: 'lat', map_lon: 'lon', map_year: 'year'}
                    dim_rename = {k: v for k, v in dim_rename.items() if k in df.columns and k != v}
                    df = df.rename(columns=dim_rename).dropna()
                    st.session_state['uploaded_data'] = df
                    st.success(f"Loaded {len(df):,} rows from NetCDF")
                finally:
                    try:
                        os.unlink(tmp2.name)
                    except Exception:
                        pass

        except Exception as e:
            st.error(f"Error reading NetCDF file: {e}")

    if 'uploaded_data' in st.session_state and st.button("❌ Clear Upload", use_container_width=True):
        del st.session_state['uploaded_data']
        st.rerun()
    
    # Variable selection
    st.subheader("Variable")
    variable_map = {
        "Temperature (°C)": "temperature",
        "Precipitation (mm)": "precipitation",
        "Wind Speed (m/s)": "wind_speed"
    }
    variable_display = st.selectbox("Select Variable", list(variable_map.keys()))
    variable = variable_map[variable_display]
    
    # Year range
    st.subheader("Time Range")
    year_range = st.slider("Select Years", 1970, 2026, (1990, 2026))
    
    # Region selection
    st.subheader("Region")
    region = st.selectbox("Select Region", 
                         ["Global", "North America", "Europe", "Asia", "Africa", "South America", "Oceania"])

    # Prediction assumptions
    st.markdown("---")
    st.subheader("🔮 Prediction Assumptions")
    years_ahead = st.slider("Years to Predict", 5, 80, 30)
    scenario = st.selectbox("Emission Scenario", [
        "Business as Usual (High)",
        "Moderate Mitigation",
        "Aggressive Mitigation (Low)"
    ])
    scenario_multipliers = {
        "Business as Usual (High)": 1.5,
        "Moderate Mitigation": 1.0,
        "Aggressive Mitigation (Low)": 0.4
    }
    scenario_mult = scenario_multipliers[scenario]
    temp_sensitivity = st.slider("Warming Sensitivity (°C/decade)", 0.1, 0.8, 0.2, step=0.05,
                                  help="Assumed temperature rise per decade beyond the trend")
    precip_change = st.slider("Precipitation Trend (%/decade)", -20, 20, 0,
                               help="Assumed % change in precipitation per decade")
    
    st.markdown("---")
    
    # Comparison mode button
    if st.button("🔄 Climate Comparison Mode", use_container_width=True):
        st.switch_page("pages/comparison.py")
    
    st.markdown("---")
    st.caption("PyClimaExplorer v1.0")

# Main content
st.title("Climate Data Dashboard")

# Load data
if 'uploaded_data' in st.session_state:
    climate_data = st.session_state['uploaded_data']
    st.info("📂 Using uploaded dataset")
else:
    with st.spinner("Loading climate data..."):
        climate_data = generate_climate_data()
    
# Filter by year range
filtered_data = climate_data[(climate_data['year'] >= year_range[0]) & 
                             (climate_data['year'] <= year_range[1])]

# Get latest year data for map
latest_year = filtered_data['year'].max()
map_data = filtered_data[filtered_data['year'] == latest_year]

# Metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_temp = filtered_data['temperature'].mean()
    st.metric("Avg Temperature", f"{avg_temp:.1f}°C", f"+{(avg_temp - 15):.1f}°C")

with col2:
    avg_precip = filtered_data['precipitation'].mean()
    st.metric("Avg Precipitation", f"{avg_precip:.0f}mm", f"{(avg_precip - 100):.0f}mm")

with col3:
    avg_wind = filtered_data['wind_speed'].mean()
    st.metric("Avg Wind Speed", f"{avg_wind:.1f}m/s", f"{(avg_wind - 10):.1f}m/s")

with col4:
    data_points = len(filtered_data)
    st.metric("Data Points", f"{data_points:,}", "Active")

st.markdown("---")

# Interactive Global Heatmap
st.subheader(f"🗺️ Global {variable_display} Distribution ({latest_year})")

# Create heatmap
fig_map = go.Figure(data=go.Scattergeo(
    lon=map_data['lon'],
    lat=map_data['lat'],
    mode='markers',
    marker=dict(
        size=8,
        color=map_data[variable],
        colorscale='RdYlBu_r' if variable == 'temperature' else 'Blues',
        showscale=True,
        colorbar=dict(title=variable_display),
        line=dict(width=0)
    ),
    text=[f"Lat: {lat:.1f}, Lon: {lon:.1f}<br>{variable_display}: {val:.1f}" 
          for lat, lon, val in zip(map_data['lat'], map_data['lon'], map_data[variable])],
    hoverinfo='text'
))

fig_map.update_layout(
    geo=dict(
        projection_type='natural earth',
        showland=True,
        landcolor='rgb(30, 33, 48)',
        coastlinecolor='rgb(100, 100, 100)',
        showocean=True,
        oceancolor='rgb(14, 17, 23)',
        bgcolor='rgb(14, 17, 23)'
    ),
    height=500,
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor='rgb(14, 17, 23)',
    plot_bgcolor='rgb(14, 17, 23)'
)

# Capture click events
selected_point = st.plotly_chart(fig_map, use_container_width=True, key="map")

# Location selection for time series
st.markdown("---")
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📊 Location-Based Time-Series Trends")
    
    # Allow manual location selection
    sel_col1, sel_col2 = st.columns(2)
    with sel_col1:
        selected_lat = st.selectbox("Select Latitude", sorted(climate_data['lat'].unique()), 
                                    index=15)
    with sel_col2:
        selected_lon = st.selectbox("Select Longitude", sorted(climate_data['lon'].unique()), 
                                    index=30)
    
    # Get time series for selected location
    location_data = climate_data[(climate_data['lat'] == selected_lat) & 
                                 (climate_data['lon'] == selected_lon)]
    
    # Create time series plot
    fig_ts = go.Figure()
    
    fig_ts.add_trace(go.Scatter(
        x=location_data['year'],
        y=location_data[variable],
        mode='lines+markers',
        name='Historical',
        line=dict(color='#00d4ff', width=2),
        marker=dict(size=4)
    ))
    
    fig_ts.update_layout(
        title=f"{variable_display} Trend at ({selected_lat:.1f}°, {selected_lon:.1f}°)",
        xaxis_title="Year",
        yaxis_title=variable_display,
        height=400,
        paper_bgcolor='rgb(14, 17, 23)',
        plot_bgcolor='rgb(30, 33, 48)',
        font=dict(color='white'),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_ts, use_container_width=True)

with col_right:
    st.subheader("🤖 AI-Powered Insights")
    
    insights = generate_insights(filtered_data, variable)
    
    for insight in insights:
        st.markdown(f"""
        <div class="insight-card">
            {insight}
        </div>
        """, unsafe_allow_html=True)
    
    # Additional statistics
    st.markdown("### 📈 Statistics")
    st.write(f"**Min:** {filtered_data[variable].min():.2f}")
    st.write(f"**Max:** {filtered_data[variable].max():.2f}")
    st.write(f"**Std Dev:** {filtered_data[variable].std():.2f}")

# Future predictions
st.markdown("---")
st.subheader("🔮 Future Climate Predictions")

with st.spinner("Generating predictions..."):
    predictions = generate_predictions(
        location_data,
        years_ahead=years_ahead,
        scenario_mult=scenario_mult,
        temp_sensitivity=temp_sensitivity,
        precip_change=precip_change
    )
    
# Combine historical and predictions
fig_pred = go.Figure()

fig_pred.add_trace(go.Scatter(
    x=location_data['year'],
    y=location_data[variable],
    mode='lines+markers',
    name='Historical Data',
    line=dict(color='#00d4ff', width=2),
    marker=dict(size=4)
))

pred_location = predictions[(predictions['lat'] == selected_lat) & 
                           (predictions['lon'] == selected_lon)]

if variable in pred_location.columns:
    fig_pred.add_trace(go.Scatter(
        x=pred_location['year'],
        y=pred_location[variable],
        mode='lines',
        name='Predicted',
        line=dict(color='#ff6b6b', width=2, dash='dash')
    ))

fig_pred.update_layout(
    title=f"Historical & Predicted {variable_display} — {scenario}",
    xaxis_title="Year",
    yaxis_title=variable_display,
    height=400,
    paper_bgcolor='rgb(14, 17, 23)',
    plot_bgcolor='rgb(30, 33, 48)',
    font=dict(color='white'),
    hovermode='x unified'
)

st.plotly_chart(fig_pred, use_container_width=True)

# Footer
st.markdown("---")
st.caption("PyClimaExplorer - Interactive Climate Data Visualization | Data: Synthetic Climate Model")
