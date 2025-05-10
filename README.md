# Real-Time-Earthquake-Visualizer
# 🌍 Real-Time Earthquake Visualizer

This Python application retrieves and visualizes real-time earthquake data from the [USGS Earthquake API](https://earthquake.usgs.gov/). It uses `requests` to fetch earthquake data in GeoJSON format and leverages `Matplotlib` with `Cartopy` to render an interactive world map.

## 📊 Features

- Fetches real-time earthquake data from USGS (past 7 days by default)
- Plots global earthquake locations on a geospatial map
- Dynamically adjusts marker size and color based on earthquake magnitude
- Supports easy customization for different timeframes (e.g., hourly, daily)

## 🧰 Dependencies

- `requests`
- `matplotlib`
- `cartopy`

You can install them via pip:

```bash
pip install requests matplotlib cartopy
