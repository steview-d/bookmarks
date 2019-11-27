from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse


# --------------------- VIEWS ---------------------
class TestAboutView(TestCase):

    def setUp(self):
        self.c = Client()

    def test_about_view(self):
        response = self.c.get(reverse('about_page'))
        self.assertEqual(response.status_code, 200)

    def test_about_loads_correct_template(self):
        page = self.c.get(reverse('about_page'))
        self.assertTemplateUsed(page, 'pages/index.html')

    def test_about_page_redirects_logged_in_users(self):
        User.objects.create_user(
            'test_user', 'a@b.com', 'test_password')
        self.c.login(username='test_user', password='test_password')
        response = self.c.get(reverse('about_page'))
        self.assertRedirects(response, reverse('profile'), 302, 200)


class TestPricingView(TestCase):

    def setUp(self):
        self.c = Client()

    def test_aboutr_view(self):
        response = self.c.get(reverse('pricing_page'))
        self.assertEqual(response.status_code, 200)

    def test_about_loads_correct_template(self):
        page = self.c.get(reverse('pricing_page'))
        self.assertTemplateUsed(page, 'pages/pricing.html')

    def test_about_page_redirects_logged_in_users(self):
        User.objects.create_user(
            'test_user', 'a@b.com', 'test_password')
        self.c.login(username='test_user', password='test_password')
        response = self.c.get(reverse('pricing_page'))
        self.assertRedirects(response, reverse('profile'), 302, 200)


class TestFaqView(TestCase):

    def setUp(self):
        self.c = Client()

    def test_aboutr_view(self):
        response = self.c.get(reverse('faq_page'))
        self.assertEqual(response.status_code, 200)

    def test_about_loads_correct_template(self):
        page = self.c.get(reverse('faq_page'))
        self.assertTemplateUsed(page, 'pages/faq.html')

    def test_about_page_redirects_logged_in_users(self):
        User.objects.create_user(
            'test_user', 'a@b.com', 'test_password')
        self.c.login(username='test_user', password='test_password')
        response = self.c.get(reverse('faq_page'))
        self.assertRedirects(response, reverse('profile'), 302, 200)
