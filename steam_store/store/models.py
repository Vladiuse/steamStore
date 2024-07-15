from django.db import models

USD = 'usd'


class SteamPayReplenishmentAvailableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(_available=True)


class SteamAccount(models.Model):
    price = models.PositiveIntegerField(unique=True)

class SteamPayReplenishment(models.Model):
    objects = models.Manager()
    available = SteamPayReplenishmentAvailableManager()
    """Типы купонов на пополнения баланса в стим"""
    ReplenishmentAmounts = (
        (777,777),
        (10, 10),
        (20, 20),
        (50, 50),
        (75, 75),
        (100, 100),
    )
    id = models.CharField(primary_key=True, max_length=10, editable=False)
    replenishment = models.PositiveIntegerField(
        choices=ReplenishmentAmounts,
        unique=True,
        verbose_name='Сумма пополнения в USD',
    )
    amount = models.PositiveIntegerField(verbose_name='Стоимость в рублях')
    _available = models.BooleanField(default=True, verbose_name='Есть в наличии')

    def save(self, **kwargs):
        # создаеться кастомный первичный ключ на базе валюты и суммы купона
        if not self.pk:
            self.pk = str(self.replenishment) + '-' + USD
        super().save(**kwargs)



class SteamPayReplenishmentCode(models.Model):
    """Коды купонов на пополнение в системе стим"""
    code = models.CharField(max_length=15, primary_key=True)
    type = models.ForeignKey(to=SteamPayReplenishment, on_delete=models.PROTECT)
    available = models.BooleanField(default=True)
