# PyClimaExplorer - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
streamlit run app.py
```

### Step 3: Open Your Browser
Navigate to: `http://localhost:8501`

---

## 📋 Quick Reference

### Main Dashboard Actions

| Action | How To |
|--------|--------|
| Change variable | Use sidebar dropdown (Temperature/Precipitation/Wind Speed) |
| Select time range | Drag the year slider in sidebar |
| View location trend | Select lat/lon from dropdowns |
| See predictions | Scroll to "Future Climate Predictions" section |
| Open comparison | Click "Climate Comparison Mode" button |

### Comparison Mode Actions

| Action | How To |
|--------|--------|
| Compare years | Use Period 1 and Period 2 sliders |
| View difference | Check the "Climate Change Visualization" map |
| See statistics | Look at the summary metrics at top |
| Return to dashboard | Click "← Back to Dashboard" |

---

## 🎯 Common Tasks

### Task 1: Analyze Temperature Trends
1. Select "Temperature (°C)" from sidebar
2. Choose year range (e.g., 1970-2019)
3. Pick a location using lat/lon dropdowns
4. View the time-series graph
5. Check AI insights for patterns

### Task 2: Compare Two Decades
1. Click "Climate Comparison Mode"
2. Set Period 1 to 1990
3. Set Period 2 to 2019
4. Select variable (e.g., Temperature)
5. Analyze the difference map

### Task 3: View Future Predictions
1. On main dashboard, select a location
2. Scroll to "Future Climate Predictions"
3. Blue line = historical data
4. Red dashed line = predictions
5. Hover for exact values

---

## 🎨 Understanding the Colors

### Temperature Maps
- 🔴 Red = Hot
- 🟡 Yellow = Warm
- 🔵 Blue = Cold

### Precipitation Maps
- 💙 Dark Blue = High precipitation
- 🔷 Light Blue = Low precipitation

### Difference Maps (Comparison Mode)
- 🔴 Red = Increase
- ⚪ White = No change
- 🔵 Blue = Decrease

---

## ⚡ Pro Tips

1. **Faster Loading**: Use shorter year ranges (e.g., 10 years instead of 50)
2. **Better Insights**: Compare extreme years (hottest vs coldest)
3. **Regional Focus**: Select specific regions in sidebar
4. **Hover Everything**: Hover over charts and maps for detailed info
5. **Zoom In**: Use mouse wheel to zoom on maps

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| App won't start | Check Python version (need 3.8+) |
| Port in use | Use: `streamlit run app.py --server.port 8502` |
| Slow performance | Reduce year range, close other tabs |
| Charts not loading | Refresh page (Ctrl+R or Cmd+R) |
| Import errors | Run: `pip install --upgrade -r requirements.txt` |

---

## 📊 Sample Workflows

### Workflow 1: Climate Change Analysis
```
1. Main Dashboard
2. Select Temperature
3. Year range: 1970-2019
4. Note the metrics (average temp)
5. Click Comparison Mode
6. Compare 1970 vs 2019
7. Analyze difference map
8. Check "Regions with Increase"
```

### Workflow 2: Location Deep Dive
```
1. Main Dashboard
2. Select location (e.g., 45°N, 0°E)
3. View time-series trend
4. Read AI insights
5. Check future predictions
6. Try different variables
7. Compare with other locations
```

### Workflow 3: Regional Comparison
```
1. Comparison Mode
2. Select two years
3. Choose variable
4. View side-by-side maps
5. Check regional comparison chart
6. Analyze sample location trends
7. Review comparison insights
```

---

## 🔧 Customization Quick Tips

### Change Color Theme
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#00d4ff"  # Change this
backgroundColor = "#0e1117"  # And this
```

### Modify Data Range
In `app.py`, change:
```python
years_range = np.arange(1970, 2020)  # Modify years
```

### Add More Locations
In `app.py`, modify:
```python
lats = np.linspace(-90, 90, 30)  # More points
lons = np.linspace(-180, 180, 60)  # More points
```

---

## 📱 Device Compatibility

| Device | Status | Notes |
|--------|--------|-------|
| Desktop | ✅ Best | Full features |
| Laptop | ✅ Great | All features work |
| Tablet | ✅ Good | Touch-friendly |
| Mobile | ⚠️ Limited | Small screen, basic features |

---

## 🎓 Learning Path

### Beginner
1. Explore the main dashboard
2. Try different variables
3. Click around the map
4. View time-series for one location

### Intermediate
1. Use comparison mode
2. Analyze trends over decades
3. Understand AI insights
4. Interpret predictions

### Advanced
1. Modify the code
2. Add real climate data
3. Customize visualizations
4. Implement new features

---

## 📚 Additional Resources

- **Full Documentation**: See [README.md](README.md)
- **Installation Help**: See [INSTALLATION.md](INSTALLATION.md)
- **Feature Details**: See [FEATURES.md](FEATURES.md)
- **Streamlit Docs**: https://docs.streamlit.io
- **Plotly Docs**: https://plotly.com/python/

---

## 💡 Did You Know?

- The app uses machine learning for predictions
- All data is cached for faster performance
- You can zoom and pan on all maps
- The dark theme reduces eye strain
- Comparison mode shows 6 different visualizations
- AI insights update in real-time

---

## 🎯 Next Steps

After mastering the basics:
1. Try all three variables (temp, precip, wind)
2. Compare multiple time periods
3. Analyze different regions
4. Study the AI insights
5. Explore future predictions
6. Customize the code for your needs

---

## ⌨️ Keyboard Shortcuts

- `R` - Refresh page
- `Ctrl/Cmd + K` - Command menu
- `Ctrl/Cmd + Shift + R` - Hard refresh
- `Esc` - Close dialogs

---

## 🌟 Best Practices

1. **Start Global**: Begin with global view, then zoom in
2. **Compare Wisely**: Choose meaningful time periods
3. **Check Insights**: Always read AI-generated insights
4. **Verify Trends**: Cross-check with multiple locations
5. **Use Predictions**: Consider future projections in analysis

---

## 🆘 Need Help?

1. Check this guide first
2. Review error messages in terminal
3. Restart the application
4. Clear browser cache
5. Reinstall dependencies
6. Check the full documentation

---

**Ready to explore climate data? Run `streamlit run app.py` and start your journey! 🌍**
