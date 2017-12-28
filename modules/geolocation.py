"""

from django.contrib.gis.geoip import GeoIP

def getGeoLocation():
    geoLoc = GeoIP()
    return geoLoc.city(request.META['REMOTE_ADDR'])
"""