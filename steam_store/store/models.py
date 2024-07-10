from django.db import models

USD = 'usd'

class SteamPayReplenishment(models.Model):
    """Типы купонов на пополнения баланса в стим"""
    ReplenishmentAmounts = (
        (10, 10),
        (20, 20),
        (50, 50),
        (75, 75),
        (100, 100),
    )
    id = models.CharField(primary_key=True, max_length=10, editable=False)
    amount = models.PositiveIntegerField(choices=ReplenishmentAmounts, unique=True)
    available = models.BooleanField(default=True, verbose_name='Есть в наличии')

    def save(self, **kwargs):
        # создаеться кастомный первичный ключ на базе валюты и суммы купона
        if not self.pk:
            self.pk = str(self.amount) + '-' + USD
        super().save(**kwargs)



class SteamPayReplenishmentCode(models.Model):
    """Коды купонов на пополнение в системе стим"""
    code = models.CharField(max_length=15, primary_key=True)
    type = models.ForeignKey(to=SteamPayReplenishment, on_delete=models.PROTECT)
    available = models.BooleanField(default=True)
