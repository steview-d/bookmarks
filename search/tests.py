from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from links.models import Page


# --------------------- VIEWS ---------------------

class TestSearchView(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(
            'test_user', 'a@b.com', 'test_password')
        self.c.login(username='test_user', password='test_password')
        Page.objects.create(name="test_page", position=1, )

    def test_search_view(self):
        response = self.c.get(reverse('search'))
        self.assertEqual(response.status_code, 200)

    def test_search_loads_correct_template(self):
        page = self.c.get(reverse('search'))
        self.assertTemplateUsed(page, 'search/search_results.html')
