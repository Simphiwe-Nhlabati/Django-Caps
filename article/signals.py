from django.db.models.signals import pre_save
from django.dispatch import receiver
from textblob import TextBlob
from .models import Article


@receiver(pre_save, sender=Article)
def analyze_sentiment(sender, instance, **kwargs):
    if instance.content:
        analysis = TextBlob(instance.content)
        polarity = analysis.sentiment.polarity  # ranges from -1 to 1

        if polarity > 0.1:
            instance.sentiment = "Positive"
        elif polarity < -0.1:
            instance.sentiment = "Negative"
        else:
            instance.sentiment = "Neutral"
    else:
        instance.sentiment = "Neutral"
