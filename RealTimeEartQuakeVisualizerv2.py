import requests
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import logging
import argparse
from matplotlib.lines import Line2D
import cartopy.io.shapereader as shpreader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# USGS API Endpoint
BASE_URL = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{}.geojson'


def parse_args():
    parser = argparse.ArgumentParser(description='Plot recent earthquakes.')
    parser.add_argument('--timeframe', default='all_week', choices=['all_hour', 'all_day', 'all_week', 'all_month'],
                        help='Time range for earthquake data')
    parser.add_argument('--output', help='Save plot to file (e.g., output.png)')
    return parser.parse_args()


def fetch_earthquake_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Network error: {e}")
        raise
    except ValueError as e:
        logger.error(f"JSON parsing error: {e}")
        raise


def plot_earthquakes(data):
    # Set up map
    fig = plt.figure(figsize=(12, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    # Set title with ocean blue color
    ax.set_title("Real-Time Earthquakes (Past 7 Days)", fontsize=15, pad=25, color='#006994')
    ax.add_feature(cfeature.LAND)

    # Define continent colors
    continent_colors = {
        'North America': '#F2CB05',
        'South America': '#400036',
        'Africa': '#8C031C',
        'Asia': '#FF81D0',
        'Europe': '#F24405',
        'Australia': '#A83E51'
    }

    # Add colored continents
    shapename = 'admin_0_countries'
    shp = shpreader.natural_earth(resolution='110m', category='cultural', name=shapename)
    reader = shpreader.Reader(shp)

    for record in reader.records():
        name = record.attributes['CONTINENT']
        if name in continent_colors:
            ax.add_geometries([record.geometry], ccrs.PlateCarree(),
                              facecolor=continent_colors[name],
                              edgecolor='black', linewidth=0.5)

    # Add ocean and other features
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.gridlines(draw_labels=True)

    # Extract data
    lons, lats, sizes, colors = [], [], [], []
    for feature in data['features']:
        try:
            coords = feature['geometry']['coordinates']
            if not isinstance(coords, list) or len(coords) < 2:
                logger.warning(f"Invalid coordinates: {coords}")
                continue
            lon, lat = coords[0], coords[1]
            mag = feature['properties'].get('mag')
            if mag is None or not isinstance(mag, (int, float)):
                logger.warning(f"Invalid magnitude: {mag}")
                continue
            lons.append(lon)
            lats.append(lat)
            sizes.append(max(2, min(mag * 2, 20)))
            colors.append('red' if mag >= 5 else 'orange' if mag >= 3 else 'yellow')
        except (KeyError, TypeError) as e:
            logger.warning(f"Skipping invalid feature: {e}")
            continue

    # Plot data
    ax.scatter(lons, lats, s=sizes, c=colors, alpha=0.6, transform=ccrs.Geodetic())

    # Add legend
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='yellow', markersize=5, label='Mag < 3'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=8, label='Mag 3-5'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Mag ≥ 5')
    ]
    ax.legend(handles=legend_elements, loc='lower left', title='Magnitude')

    return fig


if __name__ == '__main__':
    args = parse_args()
    URL = BASE_URL.format(args.timeframe)
    try:
        data = fetch_earthquake_data(URL)
        fig = plot_earthquakes(data)
        if args.output:
            plt.savefig(args.output, dpi=300, bbox_inches='tight')
        plt.show()
    except Exception as e:
        logger.error(f"Error: {e}")