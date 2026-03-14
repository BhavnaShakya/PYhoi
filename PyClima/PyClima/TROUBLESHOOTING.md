# Troubleshooting Guide - PyClimaExplorer

## Common Issues and Solutions

---

## Installation Issues

### Issue 1: "python: command not found"

**Symptoms:**
```bash
python: command not found
```

**Solutions:**
1. Check if Python is installed:
   ```bash
   python3 --version
   ```
2. Use `python3` instead of `python`:
   ```bash
   python3 -m pip install -r requirements.txt
   python3 -m streamlit run app.py
   ```
3. Install Python from [python.org](https://python.org)

---

### Issue 2: "pip: command not found"

**Symptoms:**
```bash
pip: command not found
```

**Solutions:**
1. Use Python module syntax:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Install pip:
   ```bash
   python -m ensurepip --upgrade
   ```

---

### Issue 3: Permission Denied

**Symptoms:**
```bash
ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied
```

**Solutions:**
1. Use user installation:
   ```bash
   pip install --user -r requirements.txt
   ```
2. Use virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

---

### Issue 4: Package Version Conflicts

**Symptoms:**
```bash
ERROR: Cannot install package-a and package-b because these package versions have conflicting dependencies
```

**Solutions:**
1. Create fresh virtual environment:
   ```bash
   python -m venv fresh_env
   source fresh_env/bin/activate
   pip install -r requirements.txt
   ```
2. Update pip:
   ```bash
   pip install --upgrade pip
   ```
3. Install packages one by one:
   ```bash
   pip install streamlit
   pip install plotly
   pip install pandas
   pip install numpy
   pip install scikit-learn
   ```

---

## Runtime Issues

### Issue 5: "streamlit: command not found"

**Symptoms:**
```bash
streamlit: command not found
```

**Solutions:**
1. Use Python module syntax:
   ```bash
   python -m streamlit run app.py
   ```
2. Add Python Scripts to PATH (Windows):
   - Add `C:\Users\YourName\AppData\Local\Programs\Python\Python3X\Scripts` to PATH
3. Reinstall Streamlit:
   ```bash
   pip uninstall streamlit
   pip install streamlit
   ```

---

### Issue 6: Port Already in Use

**Symptoms:**
```bash
OSError: [Errno 48] Address already in use
```

**Solutions:**
1. Use different port:
   ```bash
   streamlit run app.py --server.port 8502
   ```
2. Kill process using port 8501:
   
   **Mac/Linux:**
   ```bash
   lsof -ti:8501 | xargs kill -9
   ```
   
   **Windows:**
   ```bash
   netstat -ano | findstr :8501
   taskkill /PID <PID> /F
   ```

---

### Issue 7: Module Import Errors

**Symptoms:**
```bash
ModuleNotFoundError: No module named 'streamlit'
```

**Solutions:**
1. Verify installation:
   ```bash
   pip list | grep streamlit
   ```
2. Reinstall requirements:
   ```bash
   pip install --upgrade -r requirements.txt
   ```
3. Check Python environment:
   ```bash
   which python
   which pip
   ```
4. Ensure you're in correct virtual environment

---

### Issue 8: Page Not Loading

**Symptoms:**
- Browser shows "This site can't be reached"
- Connection refused error

**Solutions:**
1. Check if Streamlit is running:
   - Look for "You can now view your Streamlit app in your browser" message
2. Verify URL:
   - Should be `http://localhost:8501`
   - Not `https://` (no 's')
3. Try different browser
4. Clear browser cache:
   - Chrome: Ctrl+Shift+Delete
   - Firefox: Ctrl+Shift+Delete
   - Safari: Cmd+Option+E
5. Disable browser extensions
6. Check firewall settings

---

## Visualization Issues

### Issue 9: Maps Not Displaying

**Symptoms:**
- Blank space where map should be
- "Loading..." that never completes

**Solutions:**
1. Refresh page (F5 or Ctrl+R)
2. Hard refresh (Ctrl+Shift+R)
3. Check browser console for errors:
   - Press F12
   - Look at Console tab
4. Update Plotly:
   ```bash
   pip install --upgrade plotly
   ```
5. Try different browser
6. Disable ad blockers

---

### Issue 10: Charts Not Interactive

**Symptoms:**
- Can't hover over charts
- Zoom doesn't work
- No tooltips

**Solutions:**
1. Enable JavaScript in browser
2. Check browser compatibility:
   - Chrome 90+
   - Firefox 88+
   - Safari 14+
   - Edge 90+
3. Update browser to latest version
4. Clear browser cache
5. Disable conflicting extensions

---

### Issue 11: Slow Performance

**Symptoms:**
- App takes long to load
- Interactions are laggy
- Browser becomes unresponsive

**Solutions:**
1. Reduce year range:
   - Use 10-20 years instead of 50
2. Close other browser tabs
3. Increase browser memory:
   - Chrome: chrome://settings/system
   - Enable "Use hardware acceleration"
4. Restart the application
5. Clear Streamlit cache:
   - Click menu (☰) → "Clear cache"
6. Check system resources:
   - Close unnecessary applications
   - Free up RAM
7. Reduce data resolution in code:
   ```python
   lats = np.linspace(-90, 90, 15)  # Reduce from 30
   lons = np.linspace(-180, 180, 30)  # Reduce from 60
   ```

---

## Data Issues

### Issue 12: "No Data Available"

**Symptoms:**
- Empty charts
- "No data to display" messages

**Solutions:**
1. Check year range selection:
   - Ensure start year < end year
2. Verify data generation:
   - Check terminal for errors
3. Restart application
4. Clear cache and reload

---

### Issue 13: Incorrect Data Values

**Symptoms:**
- Unrealistic temperature values
- Negative precipitation
- Strange patterns

**Solutions:**
1. This is synthetic data - expected behavior
2. For real data, check data loading function
3. Verify data preprocessing
4. Check for NaN values:
   ```python
   print(data.isnull().sum())
   ```

---

## Navigation Issues

### Issue 14: Can't Switch to Comparison Mode

**Symptoms:**
- Button click doesn't work
- Error when clicking button

**Solutions:**
1. Check if `pages/comparison.py` exists
2. Verify file structure:
   ```
   PyClimaExplorer/
   ├── app.py
   └── pages/
       └── comparison.py
   ```
3. Restart application
4. Check terminal for errors

---

### Issue 15: "Page Not Found" Error

**Symptoms:**
```
Page not found
```

**Solutions:**
1. Ensure correct file structure
2. Check file names (case-sensitive)
3. Verify pages directory exists
4. Restart Streamlit

---

## UI/UX Issues

### Issue 16: Dark Theme Not Applied

**Symptoms:**
- Light background instead of dark
- Wrong colors

**Solutions:**
1. Check if `.streamlit/config.toml` exists
2. Verify config file contents
3. Restart application
4. Clear browser cache
5. Try incognito/private mode

---

### Issue 17: Sidebar Not Showing

**Symptoms:**
- No sidebar visible
- Controls missing

**Solutions:**
1. Click the arrow (>) in top-left corner
2. Expand sidebar manually
3. Check browser width (needs minimum width)
4. Try different browser
5. Refresh page

---

### Issue 18: Responsive Layout Issues

**Symptoms:**
- Elements overlapping
- Text cut off
- Charts too small

**Solutions:**
1. Zoom out browser (Ctrl + -)
2. Use full-screen mode (F11)
3. Increase browser window size
4. Try landscape mode on tablet
5. Use desktop for best experience

---

## Error Messages

### Issue 19: "StreamlitAPIException"

**Symptoms:**
```bash
StreamlitAPIException: ...
```

**Solutions:**
1. Check Streamlit version:
   ```bash
   pip show streamlit
   ```
2. Update to latest:
   ```bash
   pip install --upgrade streamlit
   ```
3. Check for deprecated functions
4. Review error message details

---

### Issue 20: "KeyError" in Session State

**Symptoms:**
```bash
KeyError: 'selected_location'
```

**Solutions:**
1. Clear browser cache
2. Restart application
3. Reset session state:
   - Click menu (☰) → "Clear cache"
4. Refresh page

---

## Platform-Specific Issues

### Windows Issues

**Issue 21: Script Execution Policy**

**Symptoms:**
```bash
cannot be loaded because running scripts is disabled
```

**Solutions:**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

**Issue 22: Path Issues**

**Symptoms:**
- Can't find files
- Import errors

**Solutions:**
1. Use forward slashes in paths:
   ```python
   path = "pages/comparison.py"  # Not "pages\comparison.py"
   ```
2. Use raw strings:
   ```python
   path = r"C:\Users\Name\PyClima"
   ```

---

### Mac Issues

**Issue 23: SSL Certificate Errors**

**Symptoms:**
```bash
SSL: CERTIFICATE_VERIFY_FAILED
```

**Solutions:**
1. Install certificates:
   ```bash
   /Applications/Python\ 3.X/Install\ Certificates.command
   ```
2. Update certifi:
   ```bash
   pip install --upgrade certifi
   ```

---

### Linux Issues

**Issue 24: Display Issues**

**Symptoms:**
- Browser doesn't open automatically

**Solutions:**
1. Manually open browser to `http://localhost:8501`
2. Set DISPLAY variable:
   ```bash
   export DISPLAY=:0
   ```
3. Use headless mode:
   ```bash
   streamlit run app.py --server.headless true
   ```

---

## Advanced Troubleshooting

### Debug Mode

Enable debug logging:
```bash
streamlit run app.py --logger.level=debug
```

### Check Dependencies

Verify all packages:
```bash
pip check
```

### System Information

Check Python environment:
```python
import sys
print(sys.version)
print(sys.executable)
```

### Network Issues

Check if port is accessible:
```bash
curl http://localhost:8501
```

---

## Getting More Help

### 1. Check Logs
Look at terminal output for error messages

### 2. Browser Console
Press F12 and check Console tab for JavaScript errors

### 3. Streamlit Documentation
Visit: https://docs.streamlit.io

### 4. Plotly Documentation
Visit: https://plotly.com/python/

### 5. Community Forums
- Streamlit Forum: https://discuss.streamlit.io
- Stack Overflow: Tag with `streamlit` and `plotly`

### 6. GitHub Issues
Check if issue is already reported

---

## Preventive Measures

### Best Practices

1. **Use Virtual Environments**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. **Keep Dependencies Updated**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Regular Restarts**
   - Restart app after major changes
   - Clear cache periodically

4. **Browser Maintenance**
   - Clear cache weekly
   - Update to latest version
   - Disable unnecessary extensions

5. **System Resources**
   - Close unused applications
   - Monitor RAM usage
   - Keep disk space available

---

## Quick Diagnostic Checklist

When something goes wrong, check:

- [ ] Python version (3.8+)
- [ ] All packages installed
- [ ] Correct directory
- [ ] Virtual environment activated
- [ ] Port 8501 available
- [ ] Browser up to date
- [ ] JavaScript enabled
- [ ] No firewall blocking
- [ ] Sufficient RAM
- [ ] Internet connection (for initial setup)

---

## Emergency Reset

If all else fails:

```bash
# 1. Stop the application (Ctrl+C)

# 2. Remove virtual environment
rm -rf venv  # Mac/Linux
rmdir /s venv  # Windows

# 3. Create fresh environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows

# 4. Reinstall everything
pip install --upgrade pip
pip install -r requirements.txt

# 5. Clear browser cache

# 6. Restart application
streamlit run app.py
```

---

## Still Having Issues?

If you've tried everything and still have problems:

1. Document the issue:
   - What you were trying to do
   - What happened instead
   - Error messages (full text)
   - Your environment (OS, Python version, etc.)

2. Check all documentation files:
   - README.md
   - INSTALLATION.md
   - FEATURES.md
   - QUICKSTART.md

3. Try a minimal example:
   ```python
   import streamlit as st
   st.write("Hello World")
   ```

4. Seek community help with detailed information

---

**Remember: Most issues have simple solutions. Stay calm and work through the checklist systematically!** 🔧
