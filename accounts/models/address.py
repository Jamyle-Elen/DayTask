from django.db import models
from django_countries.fields import CountryField

class AddressModel(models.Model):
    street = models.CharField(max_length=120, null=False)
    number = models.CharField(max_length=20, null=False)
    neighborhood = models.CharField(max_length=120, blank=True, null=True)
    complement = models.CharField(max_length=120, blank=True, null=True)
    city = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=2, null=False)
    postal_code = models.CharField(max_length=20, null=False)
    country = CountryField(default='BR')
    
    def __str__(self):
        return f"{self.street}, {self.number} - {self.city}, {self.state}, {self.country}"