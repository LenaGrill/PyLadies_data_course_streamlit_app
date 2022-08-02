import streamlit as st
import pandas as pd
import numpy as np

from geopy.geocoders import Nominatim

st.title('There and back again')
st.header('My personal travel map collection')

st.write('''Upon opening, the map below is empty. In the sidebar on the left, you can choose a country that 
I have visited. Upon selection, the map will load again, showing places visited in that country.
Below the map, you will find a short description of the stay there.''')

places_visited = pd.read_excel("places_visited.xlsx", sheet_name = "places_visited") # loads an excel file containing the data

country = places_visited["country"] 
countries = places_visited.country.unique() # shows every country only 1x, no matter how many places
countries = np.append(countries, ["All"]) # adds a field "All" that shows all countries visited
countries = np.append(countries, [" "]) # adds an empty field which leads to an empty map
countries = np.sort(countries, axis = None) # sorts countries alphabetically
country_choice = st.sidebar.selectbox('Select a country:', countries) # creates the selectionbox in the sidebar

if country_choice == "All":
    places_visited2 = places_visited # uses full list of places and countries
else:
    places_visited2 = places_visited.loc[places_visited['country'] == country_choice] # filters for places within the chosen country

def compute_coord_lat(places_visited2): # this function is used to find/create the latitude coordinate of a place
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

def compute_coord_lon(places_visited2): # this function is used to find/create the longitude coordinate of a place
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

if country_choice == " ": # if the selectbox is empty, an empty map will be shown
    st.map(data=None, zoom = 1)
else:
    places_visited2["lat"] = places_visited2.apply(compute_coord_lat, axis = 1)
    places_visited2["lon"] = places_visited2.apply(compute_coord_lon, axis = 1)
    st.map(places_visited2, zoom = 1) # the map will show places visited within the selected country

# the following code adds a short description to each country that is written on a second sheet in the excel file
countries_visited = pd.read_excel("places_visited.xlsx", sheet_name = "description")

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


