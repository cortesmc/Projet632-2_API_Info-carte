import folium
import webbrowser
import osmnx as ox
import geojson
import requests
from geopy.geocoders import Nominatim
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from difflib import SequenceMatcher
from time import sleep
import math

class Mark4:
    
    def __init__(self,place,recherche):
        geolocator = Nominatim(user_agent="cortesmc")

        self.place=place
        coor=geolocator.geocode(self.place,timeout=10)
        self.coordinates=[coor.latitude,coor.longitude]
        
        self.map=FoliumMap(self.place,self.coordinates)
        
        self.map.set_points('amenity',recherche)        
        
        self.map.display_map()

class web_info:
    
    def __init__ (self):
        PATH = "C:\Program Files (x86)\chromedrive.exe"
        options = webdriver.ChromeOptions() 
        options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})
        self.driver = webdriver.Chrome(options=options,executable_path=PATH)
        
    
    def get_info_review(self,list_names,place,domaine,search):
        list_reviews=[]
        
        for name in (list_names):
            rest= [' ',' ',' ']
            try:
                self.driver.get("https://www.tripadvisor.com/")
                sleep(1)
                input_search = self.driver.find_element(By.XPATH,('/html/body/div[1]/main/div[3]/div/div/div/form/input[1]'))
                input_search.click()
                input_search = self.driver.find_element(By.XPATH,('/html/body/div[1]/main/div[3]/div/div/div/form/input[1]'))
                input_search.send_keys(place+' '+name+' '+search)
                input_search.send_keys(Keys.ENTER)
                sleep(2)
                
                rest[0]=(self.driver.find_element(By.XPATH,('/html/body/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/div/div/div[1]/div/div/div/div[2]/div/div[1]/span')).text)
                rest[1]=(self.driver.find_element(By.XPATH,('/html/body/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/div/div/div[1]/div/div/div/div[2]/div/div[2]/div/span')).get_attribute('alt'))
                rest[2]=(self.driver.find_element(By.XPATH,('/html/body/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/div/div/div[1]/div/div/div/div[2]/div/div[3]/div[1]')).text)
            except:
                rest.append(name)
            list_reviews.append(rest)
        return list_reviews
    
    
class FoliumMap:
    
    def __init__(self,place,coord,set_zoom =13):
        self.place =place
        self.coordinates = coord
        self.map = folium.Map(location=self.coordinates, tiles="OpenStreetMap", zoom_start=set_zoom)
        
    def get_map(self):
        return self.map
    def get_coordinates(self):
        return self.coordinates
    
    def set_points(self,domaine,search):
        navigator = web_info()
        point_names = []
        place =self.place
        
        tags = {domaine: search}
        plc = ox.geometries_from_place(place, tags=tags)
        for val in plc.get('name'):
            point_names.append(val)
            
        place_points = plc[plc.geom_type == 'Point'][:100]
        

        pointInfo = navigator.get_info_review(point_names,place,domaine,search)       
        
        listTextPopup = []
        listTextPopupNames = []
        for elem in pointInfo:
            try:
                textPopup = ''
                textPopup = textPopup + elem[0] +'\n'+elem[1]+'\n'+elem[2]
                listTextPopup.append(textPopup)
                listTextPopupNames.append(elem[0])
            except:
                textPopup = ''
                textPopup = textPopup + elem[0]
        locs = zip(place_points.geometry.y, place_points.geometry.x)
        for ind,location in enumerate(locs):
            try:
                if(listTextPopupNames[ind]!=' '):
                    folium.Marker(location=location,popup=folium.Popup(html=listTextPopup[ind], parse_html=False, max_width='100%')).add_to(self.get_map())
                else:
                    folium.Marker(location=location,popup=folium.Popup(html=point_names[ind], parse_html=False, max_width='100%')).add_to(self.get_map())
            except:
                folium.Marker(location=location,popup=folium.Popup(html=point_names[ind], parse_html=False, max_width='100%')).add_to(self.get_map())
    
    def set_information(self,geoJson):
        vector_layer = folium.Choropleth(geoJson, 
                                  options={'vectorHeight': 25, 'vectorWidth': 2, 'opacity': 0.8},
                                  vector_options={'color': 'red'}, 
                                  tooltip=folium.features.GeoJsonTooltip(fields=['u', 'v']))
        vector_layer.add_to(self.map)

    
    def display_map(self):
        self.get_map().save("index.html")
        webbrowser.open("index.html")
        
if __name__== "__main__":
    
    mark4 = Mark4("Lyon,France","bar")
