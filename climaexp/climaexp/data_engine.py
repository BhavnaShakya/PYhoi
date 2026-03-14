import xarray as xr
import numpy as np
import tempfile
import os

def load_dataset(uploaded_file=None):
    """
    Loads dataset from an uploaded file or fallback to tutorial dataset.
    """
    if uploaded_file is None:
        ds = xr.tutorial.open_dataset('air_temperature')
    else:
        # Save uploaded file to a temporary file, since xarray requires a path
        # for standard netCDF4 reading
        file_path = ""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.nc') as tmp:
            tmp.write(uploaded_file.getvalue())
            file_path = tmp.name
        
        # Open the dataset
        ds = xr.open_dataset(file_path)
    
    return standardize_dataset(ds)

def standardize_dataset(ds):
    """
    Standardize dimension names to common 'lat', 'lon', 'time'.
    Provides self-healing for differently named dimensions.
    """
    rename_dict = {}
    
    for dim in ds.dims:
        d_lower = str(dim).lower()
        if d_lower in ['latitude', 'y', 'lat_dim']:
            rename_dict[dim] = 'lat'
        elif d_lower in ['longitude', 'x', 'lon_dim']:
            rename_dict[dim] = 'lon'
        elif d_lower in ['t', 'date', 'datetime']:
            rename_dict[dim] = 'time'
            
    if rename_dict:
        try:
            ds = ds.rename_dims(rename_dict)
            # rename coordinates if they match
            coord_rename = {k: v for k, v in rename_dict.items() if k in ds.coords}
            if coord_rename:
                ds = ds.rename_vars(coord_rename)
        except Exception as e:
            pass # Ignore if rename fails
            
    return ds

def get_data_vars(ds):
    """
    Extract meaningful data variables that have minimum dimensions needed for spatial plotting.
    """
    valid_vars = []
    for var_name in ds.data_vars:
        dims = ds[var_name].dims
        if ('lat' in dims and 'lon' in dims) or ('latitude' in dims and 'longitude' in dims):
            valid_vars.append(var_name)
    return valid_vars

def extract_map_slice(ds, variable, time_val):
    """
    Extract a 2D spatial slice for plotting on a map.
    """
    data = ds[variable]
    if 'time' in data.dims:
        data = data.sel(time=time_val, method='nearest')
    return data

def extract_time_series(ds, variable, lat_val, lon_val):
    """
    Extract a 1D time-series slice for a specific location.
    """
    data = ds[variable]
    if 'lat' in data.dims and 'lon' in data.dims:
        return data.sel(lat=lat_val, lon=lon_val, method='nearest')
    return None

def compute_anomaly(ds, variable, time_1, time_2):
    """
    Compute point-by-point difference between two time slices.
    """
    slice1 = extract_map_slice(ds, variable, time_1)
    slice2 = extract_map_slice(ds, variable, time_2)
    
    return slice2 - slice1
