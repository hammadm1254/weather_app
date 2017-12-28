import urllib.request

def getForecast(coordDict):
    lat, long = coordDict['lat'], coordDict['lng']
    #language = 'en'
    #units = 'us'
    secretKey = '2e4ab645b354924cfc779607723745ce'
    urlString = 'https://api.darksky.net/forecast/'
    urlString += secretKey + '/' + str(lat) + ',' + str(long) # + time + 'lang=' + language + 'units=' + units
    data = urllib.request.urlopen(urlString).read()
    return data