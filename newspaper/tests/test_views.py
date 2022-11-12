from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from newspaper.models import Topic, Newspaper, Redactor

TOPIC_LIST_URL = reverse("newspaper:topic-list")
NEWSPAPER_LIST_URL = reverse("newspaper:newspaper-list")
REDACTOR_LIST_URL = reverse("newspaper:redactor-list")


class PublicTopicTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(TOPIC_LIST_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateTopicTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123",
        )
        self.client.force_login(self.user)

    def test_retrieve_topic(self):
        Topic.objects.create(name="test1")
        Topic.objects.create(name="test2")

        response = self.client.get(TOPIC_LIST_URL)
        topics = Topic.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["topic_list"]),
            list(topics),
        )
        self.assertTemplateUsed(response, "newspaper/topic_list.html")


class PublicNewspaperTests(TestCase):
    def test_newspaper_list_page_login_required(self):
        response = self.client.get(NEWSPAPER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_newspaper_detail_page_login_required(self):
        url = reverse("newspaper:newspaper-detail", args=[1])
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)


class PrivateNewspaperTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="Teat134test",
            years_of_experience=3,
        )
        topic = Topic.objects.create(name="test")
        Newspaper.objects.create(
            title="test",
            content="text test",
            published_date="2021-10-10",
            topic=topic,
        )
        self.client.force_login(self.user)

    def test_newspaper_list_retrieve(self):
        response = self.client.get(NEWSPAPER_LIST_URL)
        newspaper = Newspaper.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["newspaper_list"]),
            list(newspaper),
        )
        self.assertTemplateUsed(response, "newspaper/newspaper_list.html")

    def test_newspaper_detail_retrieve(self):
        url = reverse("newspaper:newspaper-detail", args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


class PublicRedactorTests(TestCase):
    def test_redactor_list_page_login_required(self):
        response = self.client.get(REDACTOR_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_redactor_detail_page_login_required(self):
        url = reverse("newspaper:redactor-detail", args=[1])
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)


class PrivateRedactorTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345",
        )
        self.client.force_login(self.user)

    def test_redactor_list_retrieve(self):
        response = self.client.get(REDACTOR_LIST_URL)
        redactor = Redactor.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["redactor_list"]),
            list(redactor),
        )
        self.assertTemplateUsed(response, "newspaper/redactor_list.html")

    def test_redactor_detail_retrieve(self):
        url = reverse("newspaper:redactor-detail", args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_redactor(self):
        form_data = {
            "username": "test.test",
            "password1": "test11111",
            "password2": "test11111",
            "first_name": "first",
            "last_name": "last",
            "years_of_experience": 3,
        }

        self.client.post(reverse("newspaper:redactor-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.years_of_experience, form_data["years_of_experience"])
