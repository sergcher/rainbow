from django.db import models
from main.models import Apartment, ApartmentDetail
from tariff.models import Tariff


class CapitalRepair(models.Model):
    # Долг на начало месяца
    debt = models.FloatField(null=True, blank=True)
    # Пеня
    fine = models.FloatField(null=True, blank=True)
    # Оплачено
    paid = models.FloatField(null=True, blank=True)
    # Перерасчет
    recalculation = models.FloatField(null=True, blank=True)
    serialNumber = models.ForeignKey(to=Apartment, on_delete=models.CASCADE)

    def accrued(self):
        apartment_detail = ApartmentDetail.objects.get(serialNumber=self.serialNumber)
        tariff = Tariff.objects.get(id=apartment_detail.tariff_id)
        return round(apartment_detail.totalArea * tariff.capital_repair, 2)

    def total(self):
        total = self.accrued() + self.debt + self.fine - self.paid - self.recalculation
        return round(total, 2)
