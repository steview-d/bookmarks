from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from links.models import Page

from .setup import create_test_page


# --------------------- FORMS ---------------------

class TestPageForms(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(
            'test_user', 'a@b.com', 'test_password')
        self.c.login(username='test_user', password='test_password')
        create_test_page()

    def test_create_a_new_page(self):
        self.c.post(
            "/app/test_page",
            {'new_page-name': ['new name test'],
             'new_page-num_of_columns': 2,
             'add-page-form': ['Add Page']}
        )
        new_page = Page.objects.get(name="new name test")
        self.assertEqual("new name test", new_page.name)

    def test_renaming_a_page(self):
        self.c.post(
            "/app/test_page",
            {'name': ['rename test'],
             'edit-page-form': ['Rename']}
        )
        page = Page.objects.get(name="rename test")
        self.assertEqual("rename test", page.name)

    def test_deleting_a_page(self):
        self.c.post(
            "/app/test_page",
            {'delete-page-form': ['DELETE']}
        )
        self.assertFalse(Page.objects.filter(name="test page").exists())

    def test_deleting_last_page_so_it_creates_default_home_page(self):
        self.c.post(
            "/app/test_page",
            {'delete-page-form': ['DELETE']}
        )
        self.assertTrue(Page.objects.filter(name="home").exists())


class TestCollectionForms(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(
            'test_user', 'a@b.com', 'test_password')
        self.c.login(username='test_user', password='test_password')
        create_test_page()
