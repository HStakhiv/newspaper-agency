from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from newspaper.forms import RedactorCreationForm, RedactorUpdateForm
from newspaper.models import Newspaper, Topic


class FormTest(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "test.test",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "first",
            "last_name": "last",
            "years_of_experience": 9,
        }

    def test_redactor_creation_form_with_years_of_experience(self):
        form = RedactorCreationForm(data=self.form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_redactor_update_form(self):
        form_data = {
            "years_of_experience": 8,
            "first_name": "first_name",
            "last_name": "last_name",
        }
        form = RedactorUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_newspaper_creation_form(self):
        redactor = get_user_model().objects.create_superuser(
            username="test.test",
            password="password12345",
            first_name="first",
            last_name="last",
            years_of_experience=5,
        )
        topic = Topic.objects.create(name="test")
        form_data = {
            "title": "title test",
            "content": "some content" * 100,
            "published_date": "2020-01-01",
            "topic": topic.id,
            "redactor": redactor.id,
        }
        url = reverse("newspaper:newspaper-create")
        response = self.client.post(url, form_data)

        self.assertEqual(response.status_code, 302)
