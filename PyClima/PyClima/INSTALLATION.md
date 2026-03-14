# Installation & Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 2GB RAM minimum
- Modern web browser (Chrome, Firefox, Safari, or Edge)

## Step-by-Step Installation

### 1. Verify Python Installation

Open your terminal/command prompt and check Python version:

```bash
python --version
```

If Python is not installed, download it from [python.org](https://www.python.org/downloads/)

### 2. Download PyClimaExplorer

Download or clone the project to your local machine.

### 3. Navigate to Project Directory

```bash
cd PyClimaExplorer
```

### 4. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- streamlit (web framework)
- plotly (interactive visualizations)
- pandas (data manipulation)
- numpy (numerical computing)
- scikit-learn (machine learning)

### 5. Run the Application

#### Option A: Using the run script (Windows)
```bash
run.bat
```

#### Option B: Using the run script (Mac/Linux)
```bash
chmod +x run.sh
./run.sh
```

#### Option C: Direct command
```bash
streamlit run app.py
```

### 6. Access the Dashboard

The application will automatically open in your default browser at:
```
http://localhost:8501
```

If it doesn't open automatically, manually navigate to the URL above.

## Troubleshooting

### Issue: "streamlit: command not found"

**Solution**: Add Python Scripts to your PATH or use:
```bash
python -m streamlit run app.py
```

### Issue: Port 8501 already in use

**Solution**: Specify a different port:
```bash
streamlit run app.py --server.port 8502
```

### Issue: Module import errors

**Solution**: Reinstall dependencies:
```bash
pip install --upgrade -r requirements.txt
```

### Issue: Slow performance

**Solution**: 
- Close other browser tabs
- Reduce the year range in the sidebar
- Use a smaller dataset (modify the code to generate less data)

## Virtual Environment (Recommended)

For a clean installation, use a virtual environment:

### Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### Mac/Linux
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Updating the Application

To update to the latest version:

1. Download the new files
2. Reinstall dependencies:
```bash
pip install --upgrade -r requirements.txt
```
3. Restart the application

## Uninstallation

To remove PyClimaExplorer:

1. Deactivate virtual environment (if used):
```bash
deactivate
```

2. Delete the project folder

3. (Optional) Uninstall packages:
```bash
pip uninstall streamlit plotly pandas numpy scikit-learn
```

## System Requirements

### Minimum
- CPU: Dual-core processor
- RAM: 2GB
- Storage: 500MB free space
- Internet: Required for initial package installation

### Recommended
- CPU: Quad-core processor
- RAM: 4GB or more
- Storage: 1GB free space
- Internet: Stable connection for smooth operation

## Next Steps

After successful installation:

1. Explore the main dashboard features
2. Try different climate variables
3. Click on locations to view time-series data
4. Navigate to Comparison Mode
5. Experiment with different time periods

For detailed usage instructions, see [README.md](README.md)

## Getting Help

If you encounter issues:

1. Check the Troubleshooting section above
2. Verify all dependencies are installed correctly
3. Ensure you're using Python 3.8 or higher
4. Check the Streamlit documentation: https://docs.streamlit.io
5. Review error messages in the terminal

## Development Mode

For developers who want to modify the code:

1. Install development dependencies:
```bash
pip install streamlit plotly pandas numpy scikit-learn jupyter
```

2. Enable auto-reload:
```bash
streamlit run app.py --server.runOnSave true
```

3. The app will automatically reload when you save changes to the code

## Performance Optimization

For better performance with large datasets:

1. Enable caching (already implemented with `@st.cache_data`)
2. Reduce spatial resolution in data generation
3. Limit the year range
4. Use data aggregation for visualizations
5. Consider using Dask for very large datasets

## Security Notes

- The application runs locally on your machine
- No data is sent to external servers
- Default port 8501 is only accessible from localhost
- For production deployment, configure proper security settings

## Browser Configuration

For the best experience:

1. Enable JavaScript
2. Allow pop-ups from localhost
3. Use hardware acceleration (for smooth animations)
4. Clear browser cache if visualizations don't load

## Additional Resources

- Streamlit Documentation: https://docs.streamlit.io
- Plotly Documentation: https://plotly.com/python/
- Pandas Documentation: https://pandas.pydata.org/docs/
- Scikit-learn Documentation: https://scikit-learn.org/stable/

Enjoy exploring climate data with PyClimaExplorer! 🌍
