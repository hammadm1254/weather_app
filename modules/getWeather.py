import urllib.request
import json
import datetime

def getForecast(coordDict, t=None):
    lat, long = coordDict['lat'], coordDict['lng']
    secretKey = '387c6f2b5de7823d44477fe1b655d39e'
    urlString = 'https://api.darksky.net/forecast/'
    if t:
        url = urlString + secretKey + '/' + str(lat) + ',' + str(long) + ',' + str(
        int(t)) + '?units=us&' + 'exclude=currently,hourly,alerts&'
    else:
        url = urlString + secretKey + '/' + str(lat) + ',' + str(long) + '?units=us&' + 'exclude=minutely,hourly&'

    try:
        data = urllib.request.urlopen(url).read()
        data = json.loads(data)
    except:
        return None

    for dailyData in data['daily']['data']:
        dailyData['time'] = datetime.datetime.utcfromtimestamp(dailyData['time']).strftime("%m-%d-%Y")

    return data


def compileHistory(coordinates_Dict, location):
    tempMax = []
    tempMin = []
    precip = []
    windSpeed = []
    historyDict = {}
    presentTime = int(datetime.datetime.utcnow().timestamp())
    epoch_day = 86400
    period_in_days = 5 # limit to 5 days to prevent lockout from darkSky
    for day in range(presentTime-(epoch_day*period_in_days), presentTime, epoch_day):
        day_string = datetime.datetime.utcfromtimestamp(day).strftime("%m-%d-%Y")
        weather_data = getForecast(coordinates_Dict, day)
        if weather_data:
            try:
                tempMax.append({"label": day_string, "value": str(weather_data['daily']['data'][0]['temperatureMax'])})
            except KeyError:
                tempMax.append({"label": day_string, "value": ""})
            try:
                tempMin.append({"label": day_string, "value": str(weather_data['daily']['data'][0]['temperatureMin'])})
            except KeyError:
                tempMin.append({"label": day_string, "value": ""})
            try:
                precip.append({"label": day_string, "value": str(weather_data['daily']['data'][0]['precipAccumulation'])})
            except KeyError:
                precip.append({"label": day_string, "value": "0"})
            try:
                windSpeed.append({"label": day_string, "value": str(weather_data['daily']['data'][0]['windSpeed'])})
            except KeyError:
                windSpeed.append({"label": day_string, "value": "0"})
        else:
            tempMax.append({"label": day_string, "value": "0"})
            tempMin.append({"label": day_string, "value": "0"})
            precip.append({"label": day_string, "value": "0"})
            windSpeed.append({"label": day_string, "value": "0"})
    historyDict['tempMax'] = {'chart': {"caption": "Max Temps. for last five days",
            "subCaption": location,
            "xAxisName": "Date",
            "yAxisName": "Temp. in F",
            "numberPrefix": "",
            "theme": "zune"}, 'data': tempMax[:]}
    historyDict['tempMin'] = {'chart': {"caption": "Min Temps. for last five days",
            "subCaption": location,
            "xAxisName": "Date",
            "yAxisName": "Temp. in F",
            "numberPrefix": "",
            "theme": "zune"}, 'data': tempMin[:]}
    historyDict['precip'] = {'chart': {"caption": "Rain accumulation for last five days",
            "subCaption": location,
            "xAxisName": "Date",
            "yAxisName": "Rain in inches",
            "numberPrefix": "",
            "theme": "zune"}, 'data': precip[:]}
    historyDict['windSpeed'] = {'chart': {"caption": "Wind speed for last five days",
            "subCaption": location,
            "xAxisName": "Date",
            "yAxisName": "Wind Speed (mph)",
            "numberPrefix": "",
            "theme": "zune"}, 'data': windSpeed[:]}
    return historyDict


## All deprecated functions/classes are below
"""
def getForecast(coordDict, start_date=None, end_date=None):
    lat, long = coordDict['lat'], coordDict['lng']
    secretKey = '2e4ab645b354924cfc779607723745ce'
    urlString = 'https://api.darksky.net/forecast/'
    urlString += secretKey + '/' + str(lat) + ',' + str(long) + '?units=us&' + 'exclude=minutely,hourly&'
    data = urllib.request.urlopen(urlString).read()
    data = json.loads(data)
    return data


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