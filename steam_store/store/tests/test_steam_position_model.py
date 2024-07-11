from django.test import TestCase
from store.models import SteamPayReplenishment
from django.core.exceptions import ValidationError


class SteamPositionTest(TestCase):

    def test_primary_key_creation(self):
        """Создаеться ли кастомный первичный ключ сосотоящий
        из суммы пополнения и валюты
        """
        position = SteamPayReplenishment(replenishment=10, amount=100)
        position.save()
        self.assertEqual(position.pk, '10-usd')

    def test_not_valid_replenishment(self):
        """
        Запрещено создавать позиции стоимостью которые не прописаны в классе
        """
        incorrect_value = 11
        position = SteamPayReplenishment(replenishment=incorrect_value, amount=100)
        with self.assertRaises(ValidationError):
            position.full_clean()


class SteamPositionManagerTest(TestCase):

    """Тест менеджера SteamPayReplenishment"""

    def setUp(self):
        self._create_positions()
        self.assertEqual(SteamPayReplenishment.objects.count(),2)

    def _create_positions(self):
        self.p10 = SteamPayReplenishment.objects.create(replenishment=10, amount=100)
        self.p20 = SteamPayReplenishment.objects.create(replenishment=20, amount=100, _available=False)


    def test_available_only(self):
        """Проверка коректности фильтрации с помощю менеджера"""
        qs = SteamPayReplenishment.available.all()
        self.assertEqual(qs.count(), 1, 'В бд должны быть только 1 доступная позиция')
        self.assertTrue(self.p10 in qs, msg='Доступная позиция должны быть в результате')
        self.assertFalse(self.p20 in qs, msg='Не доступная позиция должна отсутствовать в результате')


