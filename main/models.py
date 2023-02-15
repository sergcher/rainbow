from django.db import models


class Apartment(models.Model):
    owner = models.CharField(max_length=200)
    serialNumber = models.IntegerField()


class ApartmentDetail(models.Model):
    registredQt = models.IntegerField()
    livedQt = models.IntegerField()
    totalArea = models.FloatField()
    personalAccount = models.IntegerField()
    serialNumber = models.ForeignKey(to=Apartment, on_delete=models.CASCADE)

    class Meta:
        db_table = "main_apartmentdetail"
