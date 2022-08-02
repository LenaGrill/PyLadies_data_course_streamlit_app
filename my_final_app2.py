import streamlit as st
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt

from shapely.geometry import Point, Polygon
import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
# from geopy.extra.rate_limiter import RateLimiter


# for this streamlit app to work, I had to install several libraries.
# geopandas did not work initially. After search, I found that it needs shapely, fiona and GDAL 
# to work properly. Fiona and GDAL versions need to be adjusted to the version of python used.
# for my Python 3.10.2 version to work, I installed Fiona‑1.8.21‑cp310‑cp310‑win_amd64.whl
# and GDAL‑3.4.3‑cp310‑cp310‑win_amd64.whl from 
# https://gis.stackexchange.com/questions/330840/error-installing-geopandas

# for the implementation of wikipedia, wikipedia-api has to be installed.
# import wikipediaapi


st.title('There and back again')
st.header('My personal travel map collection')

st.write('''Upon opening, the map below is empty. In the sidebar on the left, you can choose a country that 
I have visited. Upon selection, the map will load again, showing places visited in that country.
Below the map, you will find a short description of the stay there.''')


places_visited = pd.read_excel("places_visited.xlsx", sheet_name = "places_visited")

country = places_visited["country"]
countries = places_visited.country.unique() 
countries = np.append(countries, ["All"]) # adds a field "All" that shows all countries visited
countries = np.append(countries, [" "]) # adds an empty field which leads to an empty map
countries = np.sort(countries, axis = None) # sorts countries alphabetically
country_choice = st.sidebar.selectbox('Select a country:', countries)

# st.write(countries)

if country_choice == "All":
    places_visited2 = places_visited
else:
    places_visited2 = places_visited.loc[places_visited['country'] == country_choice]

def compute_coord_lat(places_visited2):
    lat = places_visited2["lat coord"]
    city = places_visited2["place/city"]
    country = places_visited2["country"]

    if pd.isna(lat):        # if latitude is NA, it will be located and returned
        geolocator1 = Nominatim(user_agent="GTA Lookup")
        location1 = geolocator1.geocode(city+", "+country) 
        lat = location1.latitude
        return lat
    else:
        return lat

def compute_coord_lon(places_visited2):
    lon = places_visited2["lon coord"]
    city = places_visited2["place/city"]
    country = places_visited2["country"]

    if pd.isna(lon):        # if longitude is NA, it will be located and returned
        geolocator1 = Nominatim(user_agent="GTA Lookup")
        location1 = geolocator1.geocode(city+", "+country) 
        lon = location1.longitude 
        return lon
    else:
        return lon

if country_choice == " ":
    st.map(data=None, zoom = 1)
else:
    places_visited2["lat"] = places_visited2.apply(compute_coord_lat, axis = 1)
    places_visited2["lon"] = places_visited2.apply(compute_coord_lon, axis = 1)
    # st.write(places_visited)

    st.map(places_visited2, zoom = 1)

countries_visited = pd.read_excel("places_visited.xlsx", sheet_name = "description")
# st.write(countries_visited)

if country_choice == ' ':
    st.write('Make a selection on the sidebar.')
elif country_choice == 'All':
    st.write('These are all places I\'ve visited over the years.')
else:
    text = countries_visited.loc[countries_visited['country'] == country_choice]
    textAsString = text.to_string(columns = ['country'], na_rep = '', header = False, index = False)
    st.header(textAsString)
    subtextAsString = text.to_string(columns = ['description', 'year'], na_rep = '', header = False, index = False)
    st.subheader(subtextAsString)
    furtherDescriptionAsString = text.to_string(columns = ['related link or further description'], na_rep = '', header = False, index = False)
    st.write(furtherDescriptionAsString)


