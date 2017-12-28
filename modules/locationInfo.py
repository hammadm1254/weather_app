import urllib.request
import urllib.parse
import json

class Location():
    def __init__(self, locationString):

        def getLocation(locationString):
            locationData = {}
            searchQuery = urllib.parse.quote_plus(locationString)
            base_url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
            api_key = '&key=AIzaSyCl89dsojF7pgkVSs1ALxx0nUUThfHypSI'
            requestUrl = base_url + searchQuery + api_key
            try:
                data = urllib.request.urlopen(requestUrl)
                locationData = json.load(data)
            except:
                return "error with query"
            finally:
                return locationData

        self.locationData = {}
        self.coordinates = {}
        self.zip = ''
        self.city = ''
        self.state = ''
        self.country = ''
        self.timezone = ''
        self.address = ''
        self.streetName = ''
        self.streetNumber = ''
        try:
            self.locationData = getLocation(locationString)
        except:
            pass

        try:
            self.coordinates = self.locationData["results"][0]['geometry']['location']
        except:
            pass
        try:
            self.address = self.locationData['results'][0]['formatted_address']
        except:
            pass
    def __str__(self):
        return str(self.address)


#testLocation_1 = Location('60148')
#print(testLocation_1.coordinates)