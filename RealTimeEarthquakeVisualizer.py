import requests
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# USGS API Endpoint (Change 'all_week' to 'all_day', 'all_hour', etc.)
URL = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson'

def fetch_earthquake_data():
    response = requests.get(URL)
    response.raise_for_status()
    return response.json()

def plot_earthquakes(data):
    # Set up map
    fig = plt.figure(figsize=(12, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_title("Real-Time Earthquakes (Past 7 Days)", fontsize=15)
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.gridlines(draw_labels=True)

    # Extract and plot earthquake data
    for feature in data['features']:
        coords = feature['geometry']['coordinates']
        lon, lat = coords[0], coords[1]
        mag = feature['properties']['mag'] or 0

        # Scale color and size by magnitude
        color = 'red' if mag >= 5 else 'orange' if mag >= 3 else 'yellow'
        size = mag * 2 if mag else 2

        ax.plot(lon, lat, marker='o', color=color, markersize=size, alpha=0.6, transform=ccrs.Geodetic())

    plt.show()

if __name__ == '__main__':
    try:
        data = fetch_earthquake_data()
        plot_earthquakes(data)
    except Exception as e:
        print(f"Error: {e}")
