from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from .models import Tweet

User = get_user_model()


class TweetTestCase(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user = User.objects.create_user(username='abc', password='some_password')
        self.user_2 = User.objects.create_user(username='bcd', password='some_password')
        Tweet.objects.create(content='first tweet', user=self.user)
        Tweet.objects.create(content='second tweet', user=self.user)
        Tweet.objects.create(content='third tweet', user=self.user_2)
        self.initial_tweets_count = Tweet.objects.all().count()

    def test_tweet_created(self):
        tweet_obj = Tweet.objects.create(content='fourth tweet', user=self.user)
        self.assertEqual(tweet_obj.id, self.initial_tweets_count + 1)
        self.assertEqual(tweet_obj.user, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user, password='some_password')
        return client

    def test_tweet_list(self):
        client = self.get_client()
        response = client.get('/api/tweets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), self.initial_tweets_count)

    def test_tweet_action_like(self):
        client = self.get_client()
        response = client.post('/api/tweets/action/', {'id': 2, 'action': 'like'})
        self.assertEqual(response.json().get('likes'), 1)

    def test_tweet_action_unlike(self):
        client = self.get_client()
        response = client.post('/api/tweets/action/', {'id': 1, 'action': 'like'})
        self.assertEqual(response.json().get('likes'), 1)
        response = client.post('/api/tweets/action/', {'id': 1, 'action': 'unlike'})
        self.assertEqual(response.json().get('likes'), 0)

    def test_tweet_action_retweet(self):
        client = self.get_client()
        response = client.post('/api/tweets/action/', {'id': 3, 'action': 'retweet'})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_tweet_id = data.get('id')
        self.assertNotEqual(new_tweet_id, 3)
        self.assertEqual(new_tweet_id, self.initial_tweets_count + 1)

    def test_tweet_create_api_view(self):
        data = {'content': 'Test tweet content'}
        client = self.get_client()
        response = client.post('/api/tweets/create/', data)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_tweet_id = data.get('id')
        self.assertEqual(new_tweet_id, self.initial_tweets_count + 1)

    def test_tweet_detail_api_view(self):
        client = self.get_client()
        response = client.get('/api/tweets/1/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('id'), 1)

    def test_tweet_delete_api_view(self):
        client = self.get_client()
        response = client.delete('/api/tweets/1/delete')
        self.assertEqual(response.status_code, 200)
        response = client.delete('/api/tweets/1/delete')
        self.assertEqual(response.status_code, 404)
        incorrect_owner_response = client.delete('/api/tweets/3/delete')
        self.assertEqual(incorrect_owner_response.status_code, 401)

