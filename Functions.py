import asyncio
from aioelectricitymaps import ElectricityMaps, ZoneRequest
from ipyleaflet import Map, GeoJSON, WidgetControl, FullScreenControl, ZoomControl, Marker
from IPython.display import display
import numpy as np
import bqplot.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from pkgutil import iter_modules
import ipywidgets as widgets
from bqplot import (
    CATEGORY10,
    LinearScale,
    Axis,
    Figure,
    OrdinalScale,
    Bars,
    DateScale
)

#Carbon Intensity per day function
async def Carbon_Intensity_per_day(X):
        async with ElectricityMaps(token="OjtTdeocDJUab") as em:
                response = await em.latest_carbon_intensity(ZoneRequest(X))

        param1 = response.carbon_intensity
        param2 = response.timestamp

        consumption_data = param1
        datetime_data = np.array([param2], dtype="datetime64")
        fig = plt.figure(title="Carbon intensity per day")
        bar = plt.bar(datetime_data, [param1, 700])
        display(fig)

#Hourly Power Consumption
async def Hourly_Power_Consumption(x):
    async with ElectricityMaps(token="OjtTdeocDJUab") as em:
        response_history= await em.power_breakdown_history(ZoneRequest(x))

    param1 = [param.time for param in response_history.history]
    param2 = [param.power_consumption_total for param in response_history.history]
    datetime_data = np.array(param1, dtype="datetime64")
    Power_Consumption = param2
    fig = plt.figure(title="Hourly Power Consumption")
    bar = plt.bar(datetime_data, Power_Consumption)
    display(fig) 

#Hourly Hourly Import Export Power Consumption 
async def Hourly_Imp_Exp_Power_Consumption(x):
        async with ElectricityMaps(token="OjtTdeocDJUab") as em:
                response_history= await em.power_breakdown_history(ZoneRequest("FR"))
        param1 = [param.power_export_total for param in response_history.history]
        param2 = [param.power_import_total for param in response_history.history]
        datetime_data = np.array(param1, dtype="datetime64[s]")
        Power_Consumption = param2
        fig_above = plt.figure(title="Power Export Total")
        above_bar = plt.bar(datetime_data, param1, colors=['blue'], labels=['Above'])
        fig_below = plt.figure(title="Power Import Total")
        below_bar = plt.bar(datetime_data, param2, colors=['red'], labels=['Below'])
        display(widgets.HBox([fig_above, fig_below]))
        
#Hourly Hourly Import Export Power Consumption
async def Hourly_Exp_Imp_Power_Consumption(x):
        async with ElectricityMaps(token="OjtTdeocDJUab") as em:
                response_history= await em.power_breakdown_history(ZoneRequest("FR"))
        param1 = [param.power_export_total for param in response_history.history]
        param2 = [param.power_import_total for param in response_history.history]
        datetime_data=[param.time for param in response_history.history]
        hour_data = [dt.hour for dt in datetime_data]

        x_ord = DateScale(dtype="datetime64")
        y_sc = LinearScale()

        bar = Bars(
        x=hour_data, 
        y=[param2, param1], 
        scales={"x": x_ord, "y": y_sc},
        padding=0.2,
        colors=CATEGORY10,
        )
        ax_x = Axis(scale=x_ord)
        ax_y = Axis(scale=y_sc, orientation="vertical", tick_format="0.2f")

        display(Figure(marks=[bar], axes=[ax_x, ax_y]))

#Power consumption by source
async def Power_Consumption_Source(x):
    async with ElectricityMaps(token="OjtTdeocDJUab") as em:
            response_history= await em.power_breakdown_history(ZoneRequest("FR"))
    data=response_history.history[0].power_consumption_breakdown
    categories = list(data.keys())
    values = list(data.values())
    x_ord = OrdinalScale()
    y_sc = LinearScale()

    bar = Bars(
        x=categories,
        y=values,
        scales={"x": x_ord, "y": y_sc},
        padding=0.2,
        colors=CATEGORY10,
        color_mode="group",
    )
    ax_x = Axis(scale=x_ord)
    ax_y = Axis(scale=y_sc, orientation="vertical", tick_format="0.2f")

    bar.orientation = "horizontal"
    ax_x.orientation = "vertical"
    ax_y.orientation = "horizontal"
    display(Figure(marks=[bar], axes=[ax_x, ax_y],title="Electricity consumption by source"))

  
#Power imported by country
async def Power_Imported_Country(x):
    async with ElectricityMaps(token="OjtTdeocDJUab") as em:
        response_history= await em.power_breakdown_history(ZoneRequest("FR"))
    data=response_history.history[0].power_import_breakdown
    print(list(data.keys()))
    categories = list(data.keys())
    values = list(data.values())
    x_ord = OrdinalScale()
    y_sc = LinearScale()

    bar = Bars(
        x=categories,
        y=values,
        scales={"x": x_ord, "y": y_sc},
        padding=0.5,
        colors=CATEGORY10,
        color_mode="group",
    )
    ax_x = Axis(scale=x_ord)
    ax_y = Axis(scale=y_sc, orientation="vertical", tick_format="0.2f")

    bar.orientation = "horizontal"
    ax_x.orientation = "vertical"
    ax_y.orientation = "horizontal"
    display(Figure(marks=[bar], axes=[ax_x, ax_y],title="Electricity imported by country"))
    from ipyleaflet import Map, Marker
from geopy.geocoders import Nominatim
import asyncio

async def handle_click(marker, **kwargs):
    location = marker.location
    country = get_country_from_coordinates(location)
    print(f"Clicked location: {location}, Country: {country}")
    await Carbon_Intensity_per_day(Coutries_Abrreviation(country))

def get_country_from_coordinates(coordinates):
    geolocator = Nominatim(user_agent="geo_locator")
    location = geolocator.reverse(coordinates, language="en")
    address = location.address
    country = address.split(",")[-1].strip()
    return country

#Callback function that gets triggered when the marker is clicked.
def on_marker_click(event, **kwargs):
    loop = asyncio.get_event_loop()
    loop.create_task(handle_click(marker))

center = (52.204793, 360.121558)
m = Map(center=center, zoom=2)  
marker = Marker(location=center, draggable=True)
m.add_layer(marker)

# Use on_click without await
marker.on_click(on_marker_click)

m

#Trouver abrreviation du pays
def Countries_Abrreviation(country):
    countries = {
        'Afghanistan': 'AF',
        'Albania': 'AL',
        'Algeria': 'DZ',
        'American Samoa': 'AS',
        'Andorra': 'AD',
        'Angola': 'AO',
        'Anguilla': 'AI',
        'Antarctica': 'AQ',
        'Antigua and Barbuda': 'AG',
        'Argentina': 'AR',
        'Armenia': 'AM',
        'Aruba': 'AW',
        'Australia': 'AU',
        'Austria': 'AT',
        'Azerbaijan': 'AZ',
        'Bahamas': 'BS',
        'Bahrain': 'BH',
        'Bangladesh': 'BD',
        'Barbados': 'BB',
        'Belarus': 'BY',
        'Belgium': 'BE',
        'Belize': 'BZ',
        'Benin': 'BJ',
        'Bermuda': 'BM',
        'Bhutan': 'BT',
        'Bolivia ': 'BO',
        'Bonaire': 'BQ',
        'Bosnia ': 'BA',
        'Botswana': 'BW',
        'Bouvet Island': 'BV',
        'Brazil': 'BR',
        'British Indian Ocean Territory': 'IO',
        'Brunei Darussalam': 'BN',
        'Bulgaria': 'BG',
        'Burkina Faso': 'BF',
        'Burundi': 'BI',
        'Cabo Verde': 'CV',
        'Cambodia': 'KH',
        'Cameroon': 'CM',
        'Canada': 'CA',
        'Cayman Islands': 'KY',
        'Central African Republic': 'CF',
        'Chad': 'TD',
        'Chile': 'CL',
        'China': 'CN',
        'Christmas Island': 'CX',
        'Cocos Islands': 'CC',
        'Colombia': 'CO',
        'Comoros ': 'KM',
        'Congo ': 'CD',
        'Congo ': 'CG',
        'Cook Islands': 'CK',
        'Costa Rica': 'CR',
        'Croatia': 'HR',
        'Cuba': 'CU',
        'Curaçao': 'CW',
        'Cyprus': 'CY',
        'Czechia': 'CZ',
        'Côte d"Ivoire': 'CI',
        'Denmark': 'DK',
        'Djibouti': 'DJ',
        'Dominica': 'DM',
        'Dominican Republic': 'DO',
        'Ecuador': 'EC',
        'Egypt': 'EG',
        'El Salvador': 'SV',
        'Equatorial Guinea': 'GQ',
        'Eritrea': 'ER',
        'Estonia': 'EE',
        'Eswatini': 'SZ',
        'Ethiopia': 'ET',
        'Falkland Islands': 'FK',
        'Faroe Islands ': 'FO',
        'Fiji': 'FJ',
        'Finland': 'FI',
        'France': 'FR',
        'French Guiana': 'GF',
        'French Polynesia': 'PF',
        'French Southern Territories ': 'TF',
        'Gabon': 'GA',
        'Gambia ': 'GM',
        'Georgia': 'GE',
        'Germany': 'DE',
        'Ghana': 'GH',
        'Gibraltar': 'GI',
        'Greece': 'GR',
        'Greenland': 'GL',
        'Grenada': 'GD',
        'Guadeloupe': 'GP',
        'Guam': 'GU',
        'Guatemala': 'GT',
        'Guernsey': 'GG',
        'Guinea': 'GN',
        'Guinea-Bissau': 'GW',
        'Guyana': 'GY',
        'Haiti': 'HT',
        'Heard Island and McDonald Islands': 'HM',
        'Holy See': 'VA',
        'Honduras': 'HN',
        'Hong Kong': 'HK',
        'Hungary': 'HU',
        'Iceland': 'IS',
        'India': 'IN',
        'Indonesia': 'ID',
        'Iran': 'IR',
        'Iraq': 'IQ',
        'Ireland': 'IE',
        'Isle of Man': 'IM',
        'Israel': 'IL',
        'Italy': 'IT',
        'Jamaica': 'JM',
        'Japan': 'JP',
        'Jersey': 'JE',
        'Jordan': 'JO',
        'Kazakhstan': 'KZ',
        'Kenya': 'KE',
        'Kiribati': 'KI',
        'Korea (the Democratic People\'s Republic of)': 'KP',
        'Korea (the Republic of)': 'KR',
        'Kuwait': 'KW',
        'Kyrgyzstan': 'KG',
        'Lao People\'s Democratic Republic': 'LA',
        'Latvia': 'LV',
        'Lebanon': 'LB',
        'Lesotho': 'LS',
        'Liberia': 'LR',
        'Libya': 'LY',
        'Liechtenstein': 'LI',
        'Lithuania': 'LT',
        'Luxembourg': 'LU',
        'Macao': 'MO',
        'Madagascar': 'MG',
        'Malawi': 'MW',
        'Malaysia': 'MY',
        'Maldives': 'MV',
        'Mali': 'ML',
        'Malta': 'MT',
        'Marshall Islands ': 'MH',
        'Martinique': 'MQ',
        'Mauritania': 'MR',
        'Mauritius': 'MU',
        'Mayotte': 'YT',
        'Mexico': 'MX',
        'Micronesia': 'FM',
        'Moldova': 'MD',
        'Monaco': 'MC',
        'Mongolia': 'MN',
        'Montenegro': 'ME',
        'Montserrat': 'MS',
        'Morocco': 'MA',
        'Mozambique': 'MZ',
        'Myanmar': 'MM',
        'Namibia': 'NA',
        'Nauru': 'NR',
        'Nepal': 'NP',
        'Netherlands': 'NL',
        'New Caledonia': 'NC',
        'New Zealand': 'NZ',
        'Nicaragua': 'NI',
        'Niger': 'NE',
        'Nigeria': 'NG',
        'Niue': 'NU',
        'Norfolk Island': 'NF',
        'Northern Mariana Islands': 'MP',
        'Norway': 'NO',
        'Oman': 'OM',
        'Pakistan': 'PK',
        'Palau': 'PW',
        'Palestine, State of': 'PS',
        'Panama': 'PA',
        'Papua New Guinea': 'PG',
        'Paraguay': 'PY',
        'Peru': 'PE',
        'Philippines': 'PH',
        'Pitcairn': 'PN',
        'Poland': 'PL',
        'Portugal': 'PT',
        'Puerto Rico': 'PR',
        'Qatar': 'QA',
        'Republic of North Macedonia': 'MK',
        'Romania': 'RO',
        'Russia': 'RU',
        'Rwanda': 'RW',
        'Réunion': 'RE',
        'Saint Barthélemy': 'BL',
        'Saint Helena, Ascension and Tristan da Cunha': 'SH',
        'Saint Kitts and Nevis': 'KN',
        'Saint Lucia': 'LC',
        'Saint Martin': 'MF',
        'Saint Pierre and Miquelon': 'PM',
        'Saint Vincent and the Grenadines': 'VC',
    }
    for country_name, abbreviation in countries.items():
        if country.upper() == country_name.upper():
            return abbreviation
            
    return "Country not found"


