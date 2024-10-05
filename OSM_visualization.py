import folium
import io
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from collections import deque


# Function to draw a map, add points and save as an image
def screenshot_image(html_path, image_path, indexes): #indexes is to use to plot the sequential images
    # Create ChromeOptions and set it to run in headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode

    # Initialize a Selenium web driver with the headless option
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(html_path)

    driver.set_window_size(800, 600)
    driver.save_screenshot(image_path)
    driver.quit()
    print('save image frame id='+str(indexes)+', done')
    
def save_image(savedmap, image_path):
    img_data = savedmap._to_png(5)
    img = Image.open(io.BytesIO(img_data))
    img.save(image_path)

def save_map_with_points(latitudes, longitudes, 
                         loc_lat, loc_lon,
                         min_lat_cur, max_lat_cur, min_lon_cur, max_lon_cur, indexes,
                         map_file="map.html", zoom_start=20, image_file=demo_filepath+'test.png',
                         save_index=True, show_index=True):
    # Check if latitudes and longitudes are of the same length
    assert len(latitudes) == len(longitudes), "Mismatched latitudes and longitudes."
    
    diff = max(abs(min_lon_cur-max_lon_cur), abs(max_lat_cur-min_lat_cur))*10 #adjust to set the map scale
    # Initialize the map
    # You can initialize with the average of provided latitudes and longitudes
    # map style: https://python-visualization.github.io/folium/latest/user_guide/raster_layers/tiles.html
    m = folium.Map(max_bounds=True,
                   location=[loc_lat, loc_lon], 
                   min_lat=min_lat_cur-diff, 
                   max_lat=max_lat_cur+diff,
                   min_lon=min_lon_cur-diff,
                   max_lon=max_lon_cur+diff,
                   zoom_start=zoom_start, #zoom in/out parameters
                   tiles="Cartodb Positron",
                   zoom_scale=False,zoom_control=False,
                   scrollWheelZoom=False, dragging=False)
    folium.TileLayer(opacity=0.0).add_to(m)
    
    # Add points to the map
    for lat, lon in zip(latitudes, longitudes):
        folium.CircleMarker(location=[lat, lon], radius=2, color='green', fill=True, fill_opacity=0.7).add_to(m)
    
    # Save the map as an HTML file
    m.save(map_file)
    if save_index==True:
        screenshot_image(map_file, image_file,indexes)
    if show_index == True:
        return m

filepath = "C:/Users/Allen/Desktop/tracking/StrongSORT-YOLO"
#a simple example
#suppose we have data already that has lat lon 
min_lat_cur, max_lat_cur = min(data['lat'].values), max(data['lat'].values)
min_lon_cur, max_lon_cur = min(data['lon'].values), max(data['lon'].values)

loc_lat = sum(data['lat'].values)/data.shape[0]
loc_lon = sum(data['lon'].values)/data.shape[0]

save_map_with_points(list(data['lat'].values),
                     list(data['lon'].values),
                     loc_lat, loc_lon,
                     min_lat_cur, max_lat_cur, min_lon_cur, max_lon_cur, 0,
                     zoom_start=30, map_file=filepath+"map.html", image_file=filepath+'test2.jpg',
                     save_index=False)