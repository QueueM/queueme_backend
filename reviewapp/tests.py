# reviewapp/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Review
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class ReviewAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='reviewer', password='testpass')
        self.client.force_authenticate(user=self.user)
        # For testing, we use the User model's content type.
        self.content_type = ContentType.objects.get_for_model(User)

    def test_create_review_with_sentiment(self):
        data = {
            'title': 'Great product',
            'rating': 5,
            'comment': 'This product is excellent and works perfectly!',
            'content_type': self.content_type.model,
            'object_id': self.user.id  # Using the user's id as a dummy reference.
        }
        response = self.client.post('/reviewapp/reviews/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('sentiment_score', response.data)
        self.assertIsNotNone(response.data['sentiment_score'])
