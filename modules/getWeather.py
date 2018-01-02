import urllib.request
import json

def getForecast(coordDict, start_date=None, end_date=None):
    lat, long = coordDict['lat'], coordDict['lng']
    secretKey = '2e4ab645b354924cfc779607723745ce'
    urlString = 'https://api.darksky.net/forecast/'
    urlString += secretKey + '/' + str(lat) + ',' + str(long) + '?units=us&' + 'exclude=minutely,hourly&'
    data = urllib.request.urlopen(urlString).read()
    data = json.loads(data)
    return data

"""
def get_weather_icon(data_json):
    icon_list = ['clear-day', 'clear-night', 'rain', 'snow', 'sleet', 'wind', 'fog', 'cloudy', 'partly-cloudy-day', 'partly-cloudy-night', 'hail', 'thunderstorm', 'tornado']
    #data_json = json.loads(data_json)
    icon = data_json['currently']['icon']
    default_icon_location = '/static/images/forecast_images/'
    if icon in icon_list:
        return default_icon_location + icon + '.png'
    else:
        return default_icon_location + 'loading.gif'

"""


"""
class currentForecastObject:
    def __init__(self, json_data):
        def get_weather_icon(data_json):
            icon_list = ['clear-day', 'clear-night', 'rain', 'snow', 'sleet', 'wind', 'fog', 'cloudy',
                         'partly-cloudy-day', 'partly-cloudy-night', 'hail', 'thunderstorm', 'tornado']
            icon = data_json['currently']['icon']
            default_icon_location = '/static/images/forecast_images/'
            if icon in icon_list:
                return default_icon_location + icon + '.png'
            else:
                return default_icon_location + 'loading.gif'
        self.timezone = json_data['timezone']
        self.icon = get_weather_icon(json_data)
        self.time = json_data['currently']['time']
        self.description = json_data['currently']['summary']
        self.temperature = json_data['currently']['temperature']
        self.apparentTemperature = json_data['currently']['apparentTemperature']
        self.windSpeed = json_data['currently']['windSpeed']
        self.windGust = json_data['currently']['windGust']
        self.windBearing = json_data['currently']['windBearing']
        try:
            self.precipitation = json_data['currently']['precipType']
        except:
            self.precipitation = 'None'
        self.precipitationProbability = json_data['currently']['precipProbability']
"""