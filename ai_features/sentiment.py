from textblob import TextBlob

def analyze_sentiment(review_text):
    analysis = TextBlob(review_text)
    return {
        "polarity": analysis.sentiment.polarity,
        "subjectivity": analysis.sentiment.subjectivity
    }
