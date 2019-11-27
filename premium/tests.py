from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from django.conf import settings

# from .forms import PaymentForm, PremiumPurchaseForm
from .models import PremiumPurchase


# --------------------- MODELS ---------------------
class TestPremiumModel(TestCase):

    def test_premium_model_returns_correct_str_value(self):
        user = User.objects.create_user(
            'test_user', 'a@b.com', 'test_password')
        test_obj = PremiumPurchase.objects.create(user=user)
        self.assertEqual(str(test_obj), "1-test_user")


# --------------------- VIEWS ---------------------
class TestPremiumView(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(
            'test_user', 'a@b.com', 'test_password')
        self.c.login(username='test_user', password='test_password')

    def test_premium_view(self):
        response = self.c.get(reverse('premium'))
        self.assertEqual(response.status_code, 200)

    def test_premium_loads_correct_template(self):
        page = self.c.get(reverse('premium'))
        self.assertTemplateUsed(page, 'premium/premium.html')

