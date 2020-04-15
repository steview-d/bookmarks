from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from .models import Page, Collection, Bookmark
from .utils.page_utils import build_empty_collection_order


# --------------------- SETUP ---------------------

def create_test_page():
    Page.objects.create(
        name="test_page",
        position=1,
        collection_order_2=build_empty_collection_order(2),
        collection_order_3=build_empty_collection_order(3),
        collection_order_4=build_empty_collection_order(4),
        collection_order_5=build_empty_collection_order(5),
        )


def create_test_collection():
    Collection.objects.create(
        name="test_collection",
        position=1,
    )


def create_test_bookmark():
    Bookmark.objects.create(
        url="http://www.google.com",
        title="Google",
        description="Search & Stuff",
        position=1,
    )


# --------------------- VIEWS ---------------------

class TestMainAppView(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(
            'test_user', 'a@b.com', 'test_password')
        self.c.login(username='test_user', password='test_password')
        create_test_page()

    def test_app_view(self):
        response = self.c.get(reverse('links', args=['test_page']))
        self.assertEqual(response.status_code, 200)

    def test_app_loads_correct_template(self):
        page = self.c.get(reverse('links', args=['test_page']))
        self.assertTemplateUsed(page, 'links/links.html')


class TestArrangeCollectionsView(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(
            'test_user', 'a@b.com', 'test_password')
        self.c.login(username='test_user', password='test_password')
        create_test_page()

    def test_arrange_collections_view(self):
        response = self.c.get(
            reverse('arrange_collections', args=['test_page']))
        self.assertEqual(response.status_code, 200)

    def test_arrange_collections_loads_correct_template(self):
        page = self.c.get(
            reverse('arrange_collections', args=['test_page']))
        self.assertTemplateUsed(page, 'links/arrange_collections.html')


class TestEditBookmarkView(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(
            'test_user', 'a@b.com', 'test_password')
        self.c.login(username='test_user', password='test_password')
        create_test_page()
        create_test_collection()
        create_test_bookmark()

    def test_edit_bookmark_view(self):
        response = self.c.get(
            reverse('edit_bookmark', args=['test_page', '1']))
        self.assertEqual(response.status_code, 200)

    def test_edit_bookmark_loads_correct_template(self):
        page = self.c.get(reverse('edit_bookmark', args=['test_page', '1']))
        self.assertTemplateUsed(page, 'links/edit_bookmark.html')


class TestAddBookmarkView(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(
            'test_user', 'a@b.com', 'test_password')
        self.c.login(username='test_user', password='test_password')
        create_test_page()

    def test_add_bookmark_view(self):
        response = self.c.get(reverse('add_bookmark', args=['test_page']))
        self.assertEqual(response.status_code, 200)

    def test_add_bookmark_loads_correct_template(self):
        page = self.c.get(reverse('add_bookmark', args=['test_page']))
        self.assertTemplateUsed(page, 'links/add_bookmark.html')


class TestMoveBookmarkView(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(
            'test_user', 'a@b.com', 'test_password')
        self.c.login(username='test_user', password='test_password')
        create_test_page()

    def test_move_bookmark_view(self):
        pass

    def test_move_bookmark_loads_correct_template(self):
        pass


class TestImportUrlView(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(
            'test_user', 'a@b.com', 'test_password')
        self.c.login(username='test_user', password='test_password')

    def test_import_url_view(self):
        pass

    def test_import_url_loads_correct_template(self):
        pass


class TestImportUrlSuccessView(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(
            'test_user', 'a@b.com', 'test_password')
        self.c.login(username='test_user', password='test_password')
        create_test_page()

    def test_import_url_success_view(self):
        pass

    def test_import_url_success_loads_correct_template(self):
        pass
