from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from .forms import SupportRequestForm
from .models import Ticket


# --------------------- MODELS ---------------------
class TestSupportModel(TestCase):

    def test_model_returns_correct_str_value(self):
        ticket = Ticket(title="test title")
        self.assertEqual(str(ticket), "test title")

    def test_ticket_has_admin_comment(self):
        ticket = Ticket(admin_comments="this is an admin comment")
        self.assertTrue(ticket.admin_commented())

    def test_ticket_does_not_have_admin_comment(self):
        ticket = Ticket()
        self.assertFalse(ticket.admin_commented())


# --------------------- VIEWS ---------------------
class TestSupportView(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(
            'test_user', 'a@b.com', 'test_password')
        self.c.login(username='test_user', password='test_password')

    def test_sending_support_email_to_user(self):
        mail.send_mail('test subject', 'test message',
                       'from@test.com', ['to@test.com'],
                       fail_silently=False)
        self.assertTrue(mail.outbox)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, 'from@test.com')

    def test_support_view(self):
        response = self.c.get(reverse('support'))
        self.assertEqual(response.status_code, 200)

    def test_correct_template_is_used(self):
        page = self.c.get(reverse('support'))
        self.assertTemplateUsed(page, "support/support.html")

    def test_form_data_is_valid(self):
        form_data = SupportRequestForm(
            {"title": "test title", "message": "test subject"}
        )
        self.assertTrue(form_data.is_valid())

    def test_form_does_not_allow_blanks(self):
        form_data = SupportRequestForm(
            {"title": "", "message": "test subject"}
        )
        self.assertEqual(
            form_data.errors['title'], ['This field is required.'])
        self.assertFalse(form_data.is_valid())
