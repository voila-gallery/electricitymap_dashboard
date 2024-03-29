import asyncio
from aioelectricitymaps import ElectricityMaps, ZoneRequest
from ipyleaflet import Map, GeoJSON, WidgetControl, FullScreenControl, ZoomControl,Marker
from IPython.display import display
from ipywidgets import Output, HBox,VBox as widgets
import numpy as np
import bqplot.pyplot as plt
import pandas as pd
import configparser
from datetime import datetime, timedelta
from pkgutil import iter_modules
import ipywidgets as widgets
from geopy.geocoders import Nominatim
import asyncio
from bqplot import (
    CATEGORY10,
    LinearScale,
    Axis,
    Figure,
    OrdinalScale,
    Bars,
    DateScale
)

config = configparser.ConfigParser()
config.read('.config')
token = config['DEFAULT']['token']

#Carbon Intensity per day function
async def Carbon_Intensity_per_day(x,bar,token):
        async with ElectricityMaps(token=token) as em:
                response = await em.latest_carbon_intensity(ZoneRequest(x))
        param1 = response.carbon_intensity
        param2 = response.timestamp
        consumption_data = param1
        datetime_data = np.array([param2], dtype="datetime64")
        bar.x=datetime_data
        bar.y=param1
    
#Hourly Power Consumption per day function
async def Hourly_Power_Consumption(country, bar, token):
    x= await Countries_Abrreviation_N(country)
    async with ElectricityMaps(token=token) as em:
        response_history = await em.power_breakdown_history(ZoneRequest(x))
    param1 = [param.time for param in response_history.history]
    param2 = [param.power_consumption_total for param in response_history.history]
    #datetime_data = np.array(param2, dtype="datetime64[s]")
    datetime_data = np.array([param1], dtype="datetime64")
    Power_Consumption = param2
    bar.x = datetime_data
    bar.y = Power_Consumption


#Hourly Import Export Power Consumption
async def Hourly_Imp_Exp_Power_Consumption(country, Exp_bar,Imp_bar, token):
    x= await Countries_Abrreviation_N(country)
    async with ElectricityMaps(token=token) as em:
        response_history = await em.power_breakdown_history(ZoneRequest(x))
    param1 = [param.power_export_total for param in response_history.history]
    param2 = [param.power_import_total for param in response_history.history]
    datetime_data = np.array(param1, dtype="datetime64[s]")
    Power_Consumption = param2
    Exp_bar.x = datetime_data
    Imp_bar.x = datetime_data
    Exp_bar.y = param1
    Imp_bar.y = param2

#Power consumption by source
async def Power_Consumption_Source(country,bar,token):
    x= await Countries_Abrreviation_N(country)
    async with ElectricityMaps(token=token) as em:
            response_history= await em.power_breakdown_history(ZoneRequest(x))
    data=response_history.history[0].power_consumption_breakdown
    categories = list(data.keys())
    values = list(data.values()) 
    bar.x =categories
    bar.y=values

#Power imported by country
async def Power_Imported_Country(country,bar,token):
    x= await Countries_Abrreviation_N(country)
    async with ElectricityMaps(token=token) as em:
        response_history= await em.power_breakdown_history(ZoneRequest(x))
    data=response_history.history[0].power_import_breakdown
    bar.x=list(data.keys())
    bar.y=list(data.values())



async def handle_click(marker, **kwargs):
    location = marker.location
    country = get_country_from_coordinates(location)
    print(f"Clicked location: {location}, Country: {country}")
    await Carbon_Intensity_per_day(Coutries_Abrreviation(country))

#Trouver abrreviation du pays
async def Countries_Abrreviation_N(country):
    async with ElectricityMaps(token=token) as em:
            response_history= await em.zones()
    countries = {key: zone.zone_name for key, zone in response_history.items()}
    for abbreviation, country_name in countries.items():
        if country.upper() == country_name.upper():
            return(abbreviation)
            break
    else:
        return("Country not found")