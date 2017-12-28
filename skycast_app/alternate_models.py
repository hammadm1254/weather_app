from django.db import models
from django.utils import timezone

class Location(models.Model):
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    city = ''
    state = ''
    zip = ''
    elevation = ''


class Search(Location):
    user = models.ForeignKey('auth.User')
    location = models.ForeignKey('location')
    search_date = models.DateTimeField()

    def publish(self):
        self.search_date = timezone.now()
        self.save()

    def __str__(self):
        result = (str(float(self.lat)), str(float(self.long)))
        return str(result)