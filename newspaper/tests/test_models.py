from django.contrib.auth import get_user_model
from django.test import TestCase

from newspaper.models import Topic, Newspaper


class ModelsTests(TestCase):
    def setUp(self) -> None:
        self.topic = Topic.objects.create(name="test")

        self.username = "test.test"
        self.password = "test12345"
        self.years_of_experience = 5
        self.redactor = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
            first_name="first_name",
            last_name="test_last",
            years_of_experience=self.years_of_experience,
        )

        self.newspaper = Newspaper.objects.create(
            title="test_title",
            topic=self.topic,
            content="some text",
            published_date="2022-11-11",
        )

    def test_topic_str(self):
        self.assertEqual(
            str(self.topic),
            f"{self.topic.name}",
        )

    def test_redactor_str(self):
        self.assertEqual(
            str(self.redactor),
            f"{self.redactor.username} "
            f"({self.redactor.first_name} {self.redactor.last_name})",
        )

    def test_newspaper_str(self):
        self.assertEqual(
            str(self.newspaper),
            f"{self.topic.name} {self.newspaper.title} {self.newspaper.published_date}"
        )

    def test_create_redactor_with_years_of_experience(self):
        self.assertEqual(self.redactor.username, self.username)
        self.assertTrue(self.redactor.check_password(self.password))
        self.assertEqual(self.redactor.years_of_experience, self.years_of_experience)
