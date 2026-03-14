import xarray as xr
import pandas as pd
import numpy as np

def standardize_dims(ds: xr.Dataset) -> xr.Dataset:
    """
    Self-healing method to rename non-standard dimension names to standard ones.
    Standard targets: 'time', 'lat', 'lon'
    """
    rename_dict = {}
    
    # Common aliases
    time_aliases = ['time', 't', 'Time', 'time_series', 'date', 'Date']
    lat_aliases = ['lat', 'latitude', 'Lat', 'Latitude', 'y', 'Y']
    lon_aliases = ['lon', 'longitude', 'Lon', 'Longitude', 'x', 'X']
    
    dims = ds.dims
    for dim in dims:
        dim_str = str(dim)
        if dim_str.lower() in [a.lower() for a in time_aliases] and dim_str != 'time':
            rename_dict[dim_str] = 'time'
        elif dim_str.lower() in [a.lower() for a in lat_aliases] and dim_str != 'lat':
            rename_dict[dim_str] = 'lat'
        elif dim_str.lower() in [a.lower() for a in lon_aliases] and dim_str != 'lon':
            rename_dict[dim_str] = 'lon'
            
    if rename_dict:
        ds = ds.rename(rename_dict)
        
    return ds

def load_dataset(uploaded_file=None) -> xr.Dataset:
    """
    Loads dataset from uploaded file, or falls back to xarray tutorial 'air_temperature'.
    """
    if uploaded_file is not None:
        # Load from uploaded uploaded_file
        # uploaded_file is likely a BytesIO or similar from Streamlit
        # xarray can read from bytes via h5netcdf or netCDF4, but it's tricky.
        import os
        import tempfile
        # Write bytes to a temporary file, then open with xarray
        with tempfile.NamedTemporaryFile(delete=False, suffix=".nc") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
        ds = xr.open_dataset(tmp_path)
    else:
        # Load fallback dataset
        ds = xr.tutorial.open_dataset('air_temperature')
        
    # Standardize dimensions
    ds = standardize_dims(ds)
    
    # Optionally chunk the dataset for efficient slicing if using dask
    # For now, memory based is fine unless dataset is huge, but we can chunk anyway
    # require dask to chunk
    try:
        ds = ds.chunk({'time': 30})
    except ValueError:
        pass # If dataset is too small or dask is not present, ignore chunking
        
    return ds

def get_variables(ds: xr.Dataset):
    """
    Returns a list of data variables (excluding coordinates).
    """
    return [var for var in ds.data_vars if len(ds[var].dims) > 0]
