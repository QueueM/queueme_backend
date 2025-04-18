from django.test import TestCase

class AiFeaturesTests(TestCase):
    def test_chatbot_response(self):
        from ai_features.chatbot import process_chat_message
        response = process_chat_message("Hello")
        self.assertIn("I received your message", response)

    def test_sentiment_analysis(self):
        from ai_features.sentiment import analyze_sentiment
        sentiment = analyze_sentiment("I love this product!")
        self.assertIn("polarity", sentiment)
