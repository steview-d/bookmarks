from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from .setup import (create_test_page,
                    create_test_collection,
                    create_test_bookmark,
                    create_test_url)


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

    def test_app_redirects_if_page_does_not_exist(self):
        response = self.c.get(reverse('links', args=['non_existent_page']))
        self.assertEqual(response.status_code, 302)


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

    def test_arrange_collections_redirects_if_page_does_not_exist(self):
        response = self.c.get(
            reverse('arrange_collections', args=['non_existent_page']))
        self.assertEqual(response.status_code, 302)


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

    def test_edit_bookmark_redirects_if_page_does_not_exist(self):
        response = self.c.get(
            reverse('edit_bookmark', args=['non_existent_page', '1']))
        self.assertEqual(response.status_code, 302)

    def test_edit_bookmark_redirects_if_bookmark_does_not_exist(self):
        response = self.c.get(
            reverse('edit_bookmark', args=['test_page', '2']))
        self.assertEqual(response.status_code, 302)


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

    def test_add_bookmark_redirects_if_page_does_not_exist(self):
        response = self.c.get(
            reverse('add_bookmark', args=['non_existent_page']))
        self.assertEqual(response.status_code, 302)


class TestMoveBookmarkView(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(
            'test_user', 'a@b.com', 'test_password')
        self.c.login(username='test_user', password='test_password')
        create_test_page()
        create_test_collection()
        create_test_bookmark()

    def test_move_bookmark_view(self):
        response = self.c.get(
            reverse('move_bookmark', args=['test_page', '1']))
        self.assertEqual(response.status_code, 200)

    def test_move_bookmark_loads_correct_template(self):
        page = self.c.get(reverse('move_bookmark', args=['test_page', '1']))
        self.assertTemplateUsed(page, 'links/move_bookmark.html')

    def test_move_bookmark_redirects_if_page_does_not_exist(self):
        response = self.c.get(
            reverse('move_bookmark', args=['non_existent_page', '1']))
        self.assertEqual(response.status_code, 302)

    def test_move_bookmark_redirects_if_bookmark_does_not_exist(self):
        response = self.c.get(
            reverse('move_bookmark', args=['test_page', '2']))
        self.assertEqual(response.status_code, 302)


class TestImportUrlView(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(
            'test_user', 'a@b.com', 'test_password')
        self.c.login(username='test_user', password='test_password')
        create_test_page()
        create_test_collection()
        create_test_bookmark()

    def test_import_url_view(self):
        test_url = create_test_url()
        response = self.c.get(f'{reverse("import_url")}?url={test_url}')
        self.assertEqual(response.status_code, 200)

    def test_import_url_loads_correct_template(self):
        test_url = create_test_url()
        page = self.c.get(f'{reverse("import_url")}?url={test_url}')
        self.assertTemplateUsed(page, 'links/import_url.html')

    def test_view_redirects_if_no_url_to_import(self):
        response = self.c.get(reverse('import_url'))
        self.assertEqual(response.status_code, 302)


class TestImportUrlSuccessView(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(
            'test_user', 'a@b.com', 'test_password')
        self.c.login(username='test_user', password='test_password')
        create_test_page()

    def test_import_url_success_view(self):
        session = self.c.session
        session['imported_url'] = create_test_url()
        session.save()
        response = self.c.get(reverse('import_url_success'))
        self.assertEqual(response.status_code, 200)

    def test_import_url_success_loads_correct_template(self):
        session = self.c.session
        session['imported_url'] = create_test_url()
        session.save()
        page = self.c.get(reverse('import_url_success'))
        self.assertTemplateUsed(page, 'links/import_url_success.html')

    def test_import_url_success_redirects_if_no_url_in_session(self):
        response = self.c.get(reverse('import_url_success'))
        self.assertEqual(response.status_code, 302)
