import logging

logger = logging.getLogger(__name__)

def get_ai_recommendations(instance):
    """
    Calculates AI recommendations for the given instance using the recommendations module.
    """
    try:
        from ai_features import recommendations
        recommendations_data = recommendations.calculate_for_shop(instance)
        return recommendations_data
    except Exception as e:
        logger.error("Error calculating AI recommendations for instance %s: %s", instance.pk, e)
        return None

def get_ai_personalization(instance):
    """
    Calculates AI personalization data for the given instance using the personalization module.
    """
    try:
        from ai_features import personalization
        personalization_data = personalization.calculate_for_shop(instance)
        return personalization_data
    except Exception as e:
        logger.error("Error calculating AI personalization for instance %s: %s", instance.pk, e)
        return None

def update_ai_fields(instance):
    """
    Updates the instance with the latest AI recommendations and personalization data.
    Prevents infinite recursion by using a temporary flag.
    """
    if getattr(instance, '_ai_update_in_progress', False):
        return

    instance._ai_update_in_progress = True

    recs = get_ai_recommendations(instance)
    pers = get_ai_personalization(instance)
    instance.ai_recommendations = recs
    instance.ai_personalization = pers

    instance.save(update_fields=['ai_recommendations', 'ai_personalization'])
    # Optionally, clear the flag if future independent updates are desired:
    # instance._ai_update_in_progress = False

def analyze_sentiment(text):
    """
    Analyzes the sentiment of the given text.
    Returns 0.75 if "good" is found (case-insensitive), otherwise 0.25.
    """
    try:
        return 0.75 if "good" in text.lower() else 0.25
    except Exception as e:
        logger.error("Error analyzing sentiment: %s", e)
        return 0.0

def get_fraud_risk(instance):
    """
    Calculates a fraud risk score for the given instance.
    Replace this stub with your actual fraud detection logic.
    """
    try:
        from ai_features import fraud_detection
        risk_score = fraud_detection.calculate_risk(instance)
        return risk_score
    except Exception as e:
        logger.error("Error calculating fraud risk for instance %s: %s", instance.pk, e)
        return 0.0
