from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from .forms import UpdateUserEmailForm
from .views import register


# --------------------- FORMS ---------------------
class TestUpdateUserEmailForm(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'test_user', 'existing@email.com', 'test_password')

    def test_clean_email_on_user_update_email_form(self):
        form = UpdateUserEmailForm(
            {"email": "unique@email.com"}
        )
        self.assertTrue(form.is_valid())

    def test_user_update_email_form_catches_duplicate_emails(self):
        form = UpdateUserEmailForm(
            {"email": "existing@email.com"}
        )
        self.assertEqual(
            form.errors['email'],
            ['This email address already exists, please choose another'])


class TestRegisterAccountForm(TestCase):
    """
    when registering an account, if the form is completed correctly and
    all data is valid, the user will be logged in and redirected.
    the first test looks for a 302 redirect to confirm the form has
    worked.
    """

    def setUp(self):
        self.c = Client()

    def test_register_account_form_works(self):
        response = self.c.post(
            reverse('register'),
            {'username': 'user_1', 'email': 'email@test.com',
             'password1': 'test_password', 'password2': 'test_password'}
        )
        self.assertEqual(response.status_code, 302)

    def test_register_account_form_picks_up_passwords_not_matching(self):
        response = self.c.post(
            reverse('register'),
            {'username': 'user_1', 'email': 'email@test.com',
             'password1': 'this_password', 'password2': 'does_not_match'}
        )
        self.assertEqual(
            response.context['form'].errors['password2'],
            ["The two password fields didn't match."]
        )


# --------------------- VIEWS ---------------------
class TestRegisterView(TestCase):

    def setUp(self):
        self.c = Client()

    def test_register_view(self):
        response = self.c.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_loads_correct_template(self):
        page = self.c.get(reverse('register'))
        self.assertTemplateUsed(page, 'accounts/register.html')

    def test_register_page_redirects_logged_in_users(self):
        User.objects.create_user(
            'test_user', 'a@b.com', 'test_password')
        self.c.login(username='test_user', password='test_password')
        response = self.c.get(reverse(register))
        self.assertRedirects(response, reverse('profile'), 302, 200)


class TestAboutView(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(
            'test_user', 'a@b.com', 'test_password')
        self.c.login(username='test_user', password='test_password')

    def test_login_view(self):
        response = self.c.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_login_loads_correct_template(self):
        page = self.c.get(reverse('about'))
        self.assertTemplateUsed(page, 'accounts/about_app.html')


class TestProfileView(TestCase):

    def setUp(self):
        pass
