# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 21:45:58 2023

@author: Dhr
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 17:56:42 2023

@author: Dhr
"""

import folium
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Function to authenticate and retrieve the Google Drive service
def authenticate_drive():
    SERVICE_ACCOUNT_FILE = 'C:\\Work 2\\Wm\\client_secrets.json'
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    drive_service = build('drive', 'v3', credentials=credentials)
    return drive_service

# Function to get image links from Google Drive folder
def get_image_links(folder_id):
    drive_service = authenticate_drive()
    
    results = drive_service.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id, name, webContentLink)"
    ).execute()

    files = results.get('files', [])
    image_links = {file['name']: file['webContentLink'] for file in files}
    
    return image_links

# Assume you have a DataFrame with station details (name, latitude, longitude)
stations = pd.read_excel("C:\\Work 2\\RS_stns_list.xlsx")

# Set the longitude range
min_lon, max_lon = -180, 180

# Filter stations based on longitude range
stations = stations[(stations['lon'] >= min_lon) & (stations['lon'] <= max_lon)]

# Google Drive folder ID
google_drive_folder_id = '1ZVdxM7iuuoYWU1bruayyNPEEvPlx7mZl'

# Get image links from the Google Drive folder
image_links = get_image_links(google_drive_folder_id)

# Create a Folium map centered around an arbitrary location
map_center = [0, 0]
mymap = folium.Map(location=map_center, zoom_start=2, control_scale=True)

# Initialize a list to keep track of initially added markers
initial_markers = []

# Add markers for each station
for index, station in stations.iterrows():
    
    # Generate the Google Drive shared link for the graph
    graph_url = image_links.get(f"{station['name']}.png", "")  # Replace with your actual filename and extension

    # Create the popup content with the iframe
    popup_content = f"{station['name']}<br>Lat: {station['lat']}<br>Lon: {station['lon']}<br><img src='{graph_url}' width='600' height='400'>"

    # Create the marker
    marker = folium.Marker([station['lat'], station['lon']], popup=popup_content)
    
    # Add the marker to the map
    marker.add_to(mymap)

    # Add the marker to the initial_markers list
    initial_markers.append(marker)

# Save the map to an HTML file or display it in a Jupyter notebook
with open("map_with_google_drive_mod.html", "w") as file:
    file.write(mymap.get_root().render())
