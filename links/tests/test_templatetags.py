from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from links.models import Page

from links.templatetags.modal_id_gens import bookmark_id, collection_id
from links.templatetags.replace_space import replace_space
from links.templatetags.icon_styling import icon_size, icon_font_size


# --------------------- TEMPLATE TAGS ------------

class TestTemplateTags(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(
            'test_user', 'a@b.com', 'test_password')
        self.c.login(username='test_user', password='test_password')
        Page.objects.create(name="test_page", position=1, )

    def test_bookmark_id_filter_returns_correct_string(self):
        result = bookmark_id(5)
        self.assertEqual(result, "modal-bm-5")

    def test_collection_id_filter_returns_correct_string(self):
        result = collection_id("has space")
        self.assertEqual(result, "modal-has_space")

    def test_replace_space_returns_correct_string(self):
        result = replace_space("has space")
        self.assertEqual(result, "has_space")

    def test_icon_size_returns_correct_value(self):
        result = icon_size(1)
        self.assertEqual(result, 54)

    def test_icon_size_returns_an_integer(self):
        result = icon_size(1)
        self.assertIsInstance(result, int)

    def test_icon_font_size_returns_correct_value(self):
        result = icon_font_size(1)
        self.assertEqual(result, 36.0)

    def test_icon_font_size_returns_a_float(self):
        result = icon_font_size(1)
        self.assertIsInstance(result, float)
