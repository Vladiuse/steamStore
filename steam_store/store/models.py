from django.db import models

USD = 'usd'

class SteamPayReplenishment(models.Model):
    ReplenishmentAmounts = (
        (10, 10),
        (20, 20),
        (50, 50),
        (75, 75),
        (100, 100),
    )
    id = models.CharField(primary_key=True, max_length=10, editable=False)
    amount = models.PositiveIntegerField(choices=ReplenishmentAmounts, unique=True)

    def save(self, **kwargs):
        if not self.pk:
            self.pk = str(self.amount) + '-' + USD
        super().save(**kwargs)



class SteamPayReplenishmentCode(models.Model):
    code = models.CharField(max_length=15, primary_key=True)
    type = models.ForeignKey(to=SteamPayReplenishment, on_delete=models.PROTECT)
    available = models.BooleanField(default=True)
