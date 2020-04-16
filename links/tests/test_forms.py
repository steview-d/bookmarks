from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from links.models import Page, Collection

from .setup import create_test_page, create_test_collection


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

    def test_add_a_new_collection_to_empty_page(self):
        self.c.post(
            "/app/test_page",
            {'collection_name': ['new collection test'],
             'column': 1,
             'is_empty': ['yes'],
             'new_page-num_of_columns': 2,
             'add-collection': ['Add Collection']}
        )
        self.assertTrue(Collection.objects.filter(
            name="new collection test").exists())

    def test_add_a_new_collection_to_an_existing_page(self):
        self.c.post(
            "/app/test_page",
            {'collection_name': ['new collection test'],
             'column': 1,
             'new_page-num_of_columns': 2,
             'add-collection': ['Add Collection']}
        )
        self.assertTrue(Collection.objects.filter(
            name="new collection test").exists())

    def test_renaming_a_collection(self):
        create_test_collection()
        self.c.post(
            "/app/test_page",
            {'new-collection-name': ['collection rename test'],
             'collection-position': 1,
             'rename-collection-form': ['Submit']}
        )
        self.assertTrue(Collection.objects.filter(
            name="collection rename test").exists())

    def test_deleting_a_collection(self):
        create_test_collection()
        self.c.post(
            "/app/test_page",
            {'collection': ['test_collection'],
             'delete-collection-form': ['DELETE']}
        )
        self.assertFalse(Collection.objects.filter(
            name="test_collection").exists())
