import pandas as pd
import geocoder
#import webbrowser
import os
#from pyvirtualdisplay import Display 
from selenium import webdriver
import folium
import time



# m = folium.Map(
#     location=[45.5236, -122.6750],
#     tiles='Stamen Toner',
#     zoom_start=13,
#     max_zoom=16
# )

m=folium.Map()
#give in the normal address we know
address = geocoder.osm('Canada')
#add marker to map
folium.Marker(address.latlng, popup='Statue Of Unity', tooltip='Click Me!').add_to(m)


fn = '../data/maps/map.html' #path to the html file

# can be defined to fit all points on the map
#m.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]])
m.save(fn)

delay = 2
tmpurl = 'file://{path}/{mapfile}'.format(path=os.getcwd(),mapfile=fn)
m.save(fn)
your_browser_path= '/Applications/Firefox.app/Contents/MacOS'
driver = webdriver.Firefox()
driver.get(tmpurl)
#Give the map tiles some time to load
time.sleep(delay)
driver.save_screenshot(fn + ".png")
driver.close()













