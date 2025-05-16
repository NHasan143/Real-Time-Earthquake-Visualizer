# 🌍 Real-Time Earthquake Visualizer

This Python project visualizes recent earthquake activity across the globe using real-time data from the USGS Earthquake Hazards Program. The tool fetches earthquake data from the past hour, day, week, or month and plots it on a world map using `matplotlib` and `cartopy`.


### 📌 Features

-   Retrieves real-time earthquake data via USGS GeoJSON feeds.
-   Supports different timeframes: past hour, day, week, or month.
-   Plots earthquake locations on a world map with magnitude-based color coding.
-   Customizable output: save plots as image files.
-   Error-handling for network/API issues and malformed data.

### 🧰 Dependencies Used

-   Python 3.7+
-   `matplotlib`
-   `cartopy`
-   `numpy`
-   `requests`


### 📈 Legend

Magnitude is visually encoded by color and size:

🟡 Yellow: Magnitude < 3  
🟠 Orange: Magnitude 3–5  
🔴 Red: Magnitude ≥ 5

All your files and folders are presented as a tree in the file explorer. You can switch from one to another by clicking a file in the tree.

### 📃 License

This project is licensed under the MIT License.


Author: Naymul Hasan
Linkedin: https://www.linkedin.com/in/naymulhasan143/  
Blog: https://naymulhasan.hashnode.dev/

