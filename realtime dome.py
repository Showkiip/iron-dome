import folium
import random
import math
import time
import webbrowser

# Class to represent an incoming threat (rocket/missile)
class Threat:
    def __init__(self, lat, lon, speed):
        self.lat = lat  # Latitude of the threat
        self.lon = lon  # Longitude of the threat
        self.speed = speed  # Speed of the threat

    def move(self):
        """Simulate the movement of the threat."""
        self.lat += self.speed * random.uniform(0.01, 0.05)  # Simulate movement in latitude
        self.lon += self.speed * random.uniform(0.01, 0.05)  # Simulate movement in longitude

# Initialize the target area (for example, somewhere in Israel)
target_lat = 32.0857
target_lon = 34.7818

# Initialize the Iron Dome system
target_area = folium.Marker([target_lat, target_lon], popup="Target Area", icon=folium.Icon(color="red"))

# Initialize the threat (simulating incoming missile)
threat = Threat(lat=random.uniform(32.0, 32.1), lon=random.uniform(34.7, 34.8), speed=0.002)

# Create a map centered on the target area
m = folium.Map(location=[target_lat, target_lon], zoom_start=12)

# Add the target area to the map
target_area.add_to(m)

# Add the threat as a blue marker
threat_marker = folium.Marker([threat.lat, threat.lon], popup="Incoming Threat", icon=folium.Icon(color="blue"))
threat_marker.add_to(m)

# Update the map in real-time
for i in range(50):  # Simulate for 50 steps
    time.sleep(0.5)  # Simulate a delay (for real-time-like updates)
    threat.move()

    # Update the threat's location on the map
    threat_marker.location = [threat.lat, threat.lon]

    # Save the updated map to an HTML file
    m.save("realtime_threat_map.html")

# Automatically open the saved HTML file in the default web browser
webbrowser.open("realtime_threat_map.html")
