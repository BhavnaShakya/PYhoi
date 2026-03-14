# 🌍 PyClimaExplorer

An interactive climate data visualization dashboard built with Python and Streamlit. Explore global climate patterns, analyze trends, and visualize future predictions with AI-powered insights.

## Features

### Main Dashboard
- **Interactive Global Heatmap**: Visualize temperature, precipitation, and wind speed across the globe with dynamic color coding
- **Location-Based Time-Series**: Click any location to view historical climate trends over multiple decades
- **AI-Powered Insights**: Automatic detection of anomalies, patterns, and correlations in climate data
- **Future Climate Predictions**: Machine learning-based projections of climate variables
- **Dynamic Filtering**: Filter by dataset, variable, time range, and region

### Climate Comparison Mode
- **Side-by-Side Comparison**: Compare two different time periods with dual heatmaps
- **Difference Visualization**: Highlight climate change with color-coded difference maps
- **Statistical Analysis**: Distribution comparisons and regional breakdowns
- **Trend Analysis**: View sample location trends with comparison markers

## Technology Stack

- **Python 3.8+**
- **Streamlit**: Web dashboard framework
- **Plotly**: Interactive maps and charts
- **Pandas & NumPy**: Data processing
- **Scikit-learn**: Machine learning predictions

## Installation

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Navigate to the project directory:
```bash
cd PyClimaExplorer
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

3. The application will open in your default web browser at `http://localhost:8501`

## Usage

### Main Dashboard
1. Use the sidebar to select:
   - Dataset type
   - Climate variable (Temperature, Precipitation, Wind Speed)
   - Year range for analysis
   - Geographic region

2. Explore the interactive map:
   - Hover over points to see values
   - Zoom and pan to focus on specific regions

3. Select a location:
   - Use the dropdown menus to choose latitude and longitude
   - View historical trends in the time-series graph
   - See AI-generated insights in the right panel

4. View future predictions:
   - Machine learning projections appear as dashed lines
   - Compare historical data with predicted trends

### Comparison Mode
1. Click "Climate Comparison Mode" in the sidebar
2. Select two years to compare
3. Choose the climate variable
4. Analyze:
   - Side-by-side heatmaps
   - Difference visualization
   - Distribution comparisons
   - Regional statistics

## Project Structure

```
PyClimaExplorer/
├── app.py                 # Main dashboard application
├── pages/
│   └── comparison.py      # Climate comparison page
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Data

The application uses synthetic climate data generated with realistic patterns:
- Temperature with global warming trends
- Precipitation patterns based on latitude
- Wind speed variations
- 50 years of historical data (1970-2019)
- 30 years of future predictions (2020-2049)

For production use, replace the synthetic data generation with real climate datasets (NetCDF, GRIB, etc.) using libraries like `xarray`.

## Features Explained

### AI-Powered Insights
- Trend analysis comparing recent vs historical periods
- Anomaly detection using statistical methods
- Regional pattern recognition
- Automatic insight generation

### Machine Learning Predictions
- Linear regression models for each location
- 30-year future projections
- Separate predictions for temperature, precipitation, and wind speed

### Interactive Visualizations
- Zoomable and pannable maps
- Hover tooltips with detailed information
- Synchronized color scales for comparisons
- Responsive layout for different screen sizes

## Customization

### Adding Real Climate Data
Replace the `generate_climate_data()` function with code to load real datasets:

```python
import xarray as xr

def load_climate_data():
    ds = xr.open_dataset('your_climate_data.nc')
    # Process and return as pandas DataFrame
    return df
```

### Modifying Color Schemes
Update the `colorscale` parameter in Plotly figures:
- Temperature: `'RdYlBu_r'` (Red-Yellow-Blue reversed)
- Precipitation: `'Blues'`
- Custom: Any Plotly colorscale name

### Adding New Variables
1. Add to the `variable_map` dictionary in the sidebar
2. Ensure your data includes the new variable
3. Update the data generation or loading function

## Performance Notes

- Data is cached using `@st.cache_data` for faster reloads
- Synthetic data generation is optimized for quick startup
- For large real datasets, consider:
  - Downsampling spatial resolution
  - Pre-processing data files
  - Using Dask for out-of-core computation

## Browser Compatibility

Tested and working on:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## License

This project is open source and available for educational and research purposes.

## Contributing

Contributions are welcome! Areas for improvement:
- Integration with real climate datasets (CMIP6, ERA5, etc.)
- Additional ML models for predictions
- More sophisticated anomaly detection
- Export functionality for charts and data
- User authentication and saved preferences

## Support

For issues or questions, please open an issue in the repository.

## Acknowledgments

Built with Streamlit, Plotly, and the Python scientific computing ecosystem.
