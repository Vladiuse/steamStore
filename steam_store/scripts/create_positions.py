from store.models import SteamPayReplenishment

RUB_PRICE = {
    10: 879,
    20: 1757,
    50: 4393,
    75: 6590,
    100: 8786,
}
for replenishment,_ in SteamPayReplenishment.ReplenishmentAmounts:
    amount=RUB_PRICE[replenishment]
    SteamPayReplenishment.objects.create(replenishment=replenishment, amount=amount)

print('Created SteamPayReplenishment', SteamPayReplenishment.objects.count())