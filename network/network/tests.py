from __future__ import annotations

from django.test import Client
from django.test import TestCase
from django.urls import reverse

from .models import NewPost
from .models import User


class NewPostModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user('user', 'user@gmail.com', 'user')
        self.new_post = NewPost.objects.create(
            user=self.user, body='This is a test post',
        )

    def test_create_new_post(self):
        self.assertEqual(self.new_post.body, 'This is a test post')
        self.assertEqual(self.new_post.number_of_likes, 0)


class NewPostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_user', password='test_password',
        )
        self.data = {'body': 'This is a new post body'}
        self.post = NewPost.objects.create(
            user=self.user, body=self.data['body'],
        )
        self.url = reverse('new_post')

    def test_get_request(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/new_post.html')

    def test_post_request_valid_data(self):
        response = self.client.post(self.url, self.data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post.body, self.data['body'])
