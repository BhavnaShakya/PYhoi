import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Climate Comparison - PyClimaExplorer",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
    .comparison-card {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #ff6b6b;
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
</style>
""", unsafe_allow_html=True)

# Generate synthetic climate data
@st.cache_data
def generate_climate_data():
    np.random.seed(42)
    
    lats = np.linspace(-90, 90, 30)
    lons = np.linspace(-180, 180, 60)
    years_range = np.arange(1970, 2027)
    
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

# Sidebar
with st.sidebar:
    st.title("🔄 Comparison Mode")
    st.markdown("---")
    
    # Variable selection
    st.subheader("Variable")
    variable_map = {
        "Temperature (°C)": "temperature",
        "Precipitation (mm)": "precipitation",
        "Wind Speed (m/s)": "wind_speed"
    }
    variable_display = st.selectbox("Select Variable", list(variable_map.keys()))
    variable = variable_map[variable_display]
    
    # Time period 1
    st.subheader("Period 1")
    year1 = st.slider("Select Year", 1970, 2026, 1990, key="year1")
    
    # Time period 2
    st.subheader("Period 2")
    year2 = st.slider("Select Year", 1970, 2026, 2026, key="year2")
    
    st.markdown("---")
    
    # Back to dashboard
    if st.button("← Back to Dashboard", use_container_width=True):
        st.switch_page("app.py")
    
    st.markdown("---")
    st.caption("PyClimaExplorer v1.0")

# Main content
st.title("Climate Comparison Analysis")
st.markdown(f"### Comparing {year1} vs {year2}")

# Load data
with st.spinner("Loading climate data..."):
    climate_data = generate_climate_data()

# Get data for both periods — reset index to avoid alignment errors
data_period1 = climate_data[climate_data['year'] == year1].reset_index(drop=True)
data_period2 = climate_data[climate_data['year'] == year2].reset_index(drop=True)

# Calculate difference
data_diff = data_period2.copy()
data_diff[variable] = data_period2[variable].values - data_period1[variable].values

# Summary metrics
st.subheader("📊 Summary Statistics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg1 = data_period1[variable].mean()
    st.metric(f"{year1} Average", f"{avg1:.2f}")

with col2:
    avg2 = data_period2[variable].mean()
    st.metric(f"{year2} Average", f"{avg2:.2f}")

with col3:
    change = avg2 - avg1
    change_pct = (change / avg1) * 100 if avg1 != 0 else 0
    st.metric("Absolute Change", f"{change:.2f}", f"{change_pct:.1f}%")

with col4:
    max_diff = abs(data_diff[variable]).max()
    st.metric("Max Regional Change", f"{max_diff:.2f}")

st.markdown("---")

# Side-by-side heatmaps
st.subheader("🗺️ Side-by-Side Comparison")

col_map1, col_map2 = st.columns(2)

with col_map1:
    st.markdown(f"#### {year1}")
    
    fig1 = go.Figure(data=go.Scattergeo(
        lon=data_period1['lon'],
        lat=data_period1['lat'],
        mode='markers',
        marker=dict(
            size=8,
            color=data_period1[variable],
            colorscale='RdYlBu_r' if variable == 'temperature' else 'Blues',
            showscale=True,
            colorbar=dict(title=variable_display, x=1.0, xanchor='left', thickness=15),
            line=dict(width=0),
            cmin=data_period1[variable].min(),
            cmax=data_period2[variable].max()
        ),
        text=[f"{val:.1f}" for val in data_period1[variable]],
        hoverinfo='text'
    ))
    
    fig1.update_layout(
        geo=dict(
            projection_type='natural earth',
            showland=True,
            landcolor='rgb(30, 33, 48)',
            coastlinecolor='rgb(100, 100, 100)',
            showocean=True,
            oceancolor='rgb(14, 17, 23)',
            bgcolor='rgb(14, 17, 23)',
            domain=dict(x=[0, 0.85])
        ),
        height=400,
        margin=dict(l=0, r=60, t=0, b=0),
        paper_bgcolor='rgb(14, 17, 23)',
        plot_bgcolor='rgb(14, 17, 23)'
    )
    
    st.plotly_chart(fig1, use_container_width=True)

with col_map2:
    st.markdown(f"#### {year2}")
    
    fig2 = go.Figure(data=go.Scattergeo(
        lon=data_period2['lon'],
        lat=data_period2['lat'],
        mode='markers',
        marker=dict(
            size=8,
            color=data_period2[variable],
            colorscale='RdYlBu_r' if variable == 'temperature' else 'Blues',
            showscale=True,
            colorbar=dict(title=variable_display, x=1.0, xanchor='left', thickness=15),
            line=dict(width=0),
            cmin=data_period1[variable].min(),
            cmax=data_period2[variable].max()
        ),
        text=[f"{val:.1f}" for val in data_period2[variable]],
        hoverinfo='text'
    ))
    
    fig2.update_layout(
        geo=dict(
            projection_type='natural earth',
            showland=True,
            landcolor='rgb(30, 33, 48)',
            coastlinecolor='rgb(100, 100, 100)',
            showocean=True,
            oceancolor='rgb(14, 17, 23)',
            bgcolor='rgb(14, 17, 23)',
            domain=dict(x=[0, 0.85])
        ),
        height=400,
        margin=dict(l=0, r=60, t=0, b=0),
        paper_bgcolor='rgb(14, 17, 23)',
        plot_bgcolor='rgb(14, 17, 23)'
    )
    
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Difference visualization
st.subheader("🔥 Climate Change Visualization")
st.markdown(f"#### Difference Map ({year2} - {year1})")

fig_diff = go.Figure(data=go.Scattergeo(
    lon=data_diff['lon'],
    lat=data_diff['lat'],
    mode='markers',
    marker=dict(
        size=10,
        color=data_diff[variable],
        colorscale='RdBu_r',
        showscale=True,
        colorbar=dict(title=f"Change in {variable_display}"),
        line=dict(width=0),
        cmid=0
    ),
    text=[f"Change: {val:+.2f}" for val in data_diff[variable]],
    hoverinfo='text'
))

fig_diff.update_layout(
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

st.plotly_chart(fig_diff, use_container_width=True)

st.markdown("---")

# Comparison graphs
st.subheader("📈 Detailed Comparison Analysis")

col_graph1, col_graph2 = st.columns(2)

with col_graph1:
    # Distribution comparison
    fig_dist = go.Figure()
    
    fig_dist.add_trace(go.Histogram(
        x=data_period1[variable],
        name=str(year1),
        opacity=0.7,
        marker_color='#00d4ff',
        nbinsx=30
    ))
    
    fig_dist.add_trace(go.Histogram(
        x=data_period2[variable],
        name=str(year2),
        opacity=0.7,
        marker_color='#ff6b6b',
        nbinsx=30
    ))
    
    fig_dist.update_layout(
        title="Distribution Comparison",
        xaxis_title=variable_display,
        yaxis_title="Frequency",
        barmode='overlay',
        height=350,
        paper_bgcolor='rgb(14, 17, 23)',
        plot_bgcolor='rgb(30, 33, 48)',
        font=dict(color='white'),
        legend=dict(x=0.7, y=0.95)
    )
    
    st.plotly_chart(fig_dist, use_container_width=True)

with col_graph2:
    # Regional comparison (by latitude bands)
    band_labels = ['Polar S', 'Temp S', 'Trop S', 'Trop N', 'Temp N', 'Polar N']
    bins = [-90, -66.5, -23.5, 0, 23.5, 66.5, 90]

    data_period1['lat_band'] = pd.cut(data_period1['lat'], bins=bins, labels=band_labels)
    data_period2['lat_band'] = pd.cut(data_period2['lat'], bins=bins, labels=band_labels)

    regional_data = pd.DataFrame({
        'Region': band_labels,
        year1: [data_period1[data_period1['lat_band'] == band][variable].mean() for band in band_labels],
        year2: [data_period2[data_period2['lat_band'] == band][variable].mean() for band in band_labels],
    })
    
    fig_regional = go.Figure()
    
    fig_regional.add_trace(go.Bar(
        x=regional_data['Region'],
        y=regional_data[year1],
        name=str(year1),
        marker_color='#00d4ff'
    ))
    
    fig_regional.add_trace(go.Bar(
        x=regional_data['Region'],
        y=regional_data[year2],
        name=str(year2),
        marker_color='#ff6b6b'
    ))
    
    fig_regional.update_layout(
        title="Regional Comparison",
        xaxis_title="Region",
        yaxis_title=variable_display,
        barmode='group',
        height=350,
        paper_bgcolor='rgb(14, 17, 23)',
        plot_bgcolor='rgb(30, 33, 48)',
        font=dict(color='white')
    )
    
    st.plotly_chart(fig_regional, use_container_width=True)

# Insights
st.markdown("---")
st.subheader("💡 Comparison Insights")

col_ins1, col_ins2, col_ins3 = st.columns(3)

with col_ins1:
    warming_regions = len(data_diff[data_diff[variable] > 0])
    total_regions = len(data_diff)
    pct_warming = (warming_regions / total_regions) * 100
    
    st.markdown(f"""
    <div class="comparison-card">
        <h4>Regions with Increase</h4>
        <h2>{warming_regions} / {total_regions}</h2>
        <p>{pct_warming:.1f}% of all regions</p>
    </div>
    """, unsafe_allow_html=True)

with col_ins2:
    avg_change = data_diff[variable].mean()
    
    st.markdown(f"""
    <div class="comparison-card">
        <h4>Average Change</h4>
        <h2>{avg_change:+.2f}</h2>
        <p>{variable_display}</p>
    </div>
    """, unsafe_allow_html=True)

with col_ins3:
    std_change = data_diff[variable].std()
    
    st.markdown(f"""
    <div class="comparison-card">
        <h4>Variability</h4>
        <h2>{std_change:.2f}</h2>
        <p>Standard deviation of change</p>
    </div>
    """, unsafe_allow_html=True)

# Time series comparison for sample locations
st.markdown("---")
st.subheader("📍 Sample Location Trends")

# Select 3 sample locations
sample_lats = [0, 45, -45]  # Equator, Mid-latitude N, Mid-latitude S
sample_lons = [0, 0, 0]

fig_samples = make_subplots(
    rows=1, cols=3,
    subplot_titles=["Equator (0°, 0°)", "Mid-Latitude N (45°, 0°)", "Mid-Latitude S (-45°, 0°)"]
)

for idx, (lat, lon) in enumerate(zip(sample_lats, sample_lons)):
    # Find closest lat/lon in data
    closest_lat = min(climate_data['lat'].unique(), key=lambda x: abs(x - lat))
    closest_lon = min(climate_data['lon'].unique(), key=lambda x: abs(x - lon))
    
    location_data = climate_data[(climate_data['lat'] == closest_lat) & 
                                 (climate_data['lon'] == closest_lon)]
    
    fig_samples.add_trace(
        go.Scatter(
            x=location_data['year'],
            y=location_data[variable],
            mode='lines',
            name=f"({closest_lat:.0f}°, {closest_lon:.0f}°)",
            line=dict(width=2),
            showlegend=False
        ),
        row=1, col=idx+1
    )
    
    # Add vertical lines for comparison years
    fig_samples.add_vline(x=year1, line_dash="dash", line_color="#00d4ff", 
                         opacity=0.5, row=1, col=idx+1)
    fig_samples.add_vline(x=year2, line_dash="dash", line_color="#ff6b6b", 
                         opacity=0.5, row=1, col=idx+1)

fig_samples.update_layout(
    height=300,
    paper_bgcolor='rgb(14, 17, 23)',
    plot_bgcolor='rgb(30, 33, 48)',
    font=dict(color='white'),
    showlegend=False
)

fig_samples.update_xaxes(title_text="Year")
fig_samples.update_yaxes(title_text=variable_display)

st.plotly_chart(fig_samples, use_container_width=True)

# Footer
st.markdown("---")
st.caption("PyClimaExplorer - Climate Comparison Mode | Data: Synthetic Climate Model")
