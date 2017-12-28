from django.db import models
from django.utils import timezone

class Search(models.Model):
    user = models.ForeignKey('auth.User')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    #dateRange = models.DateTimeField()
    #locationFriendlyName = models.CharField(max_length=200)
    location_Search = models.CharField(max_length=200)
    search_date = models.DateTimeField()

    def publish(self):
        self.search_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.location_Search)
        #result = (str(float(self.latitude)), str(float(self.longitude)))
        #return str(result)
