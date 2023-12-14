from django.test import TestCase
from django.urls import reverse

from http import HTTPStatus

class TestRoutes(TestCase):

    def test_home_page(self):
        # Вызываем метод get для клиента (self.client)
        # и загружаем главную страницу.
        url = reverse('news:home')
        responce = self.client.get(url)
        # Проверяем, что код ответа равен 200.
        self.assertEqual(responce.status_code, HTTPStatus.OK)