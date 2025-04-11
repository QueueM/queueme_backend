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
    # Optionally, to allow further updates later, you can reset the flag:
    # instance._ai_update_in_progress = False

def analyze_sentiment(text):
    """
    Analyzes the sentiment of the given text.
    Returns 0.75 if "good" (case-insensitive) is found, otherwise 0.25.
    """
    try:
        return 0.75 if "good" in text.lower() else 0.25
    except Exception as e:
        logger.error("Error analyzing sentiment: %s", e)
        return 0.0

def get_fraud_risk(instance):
    """
    Calculates a fraud risk score for the given instance using the check_booking function.
    If check_booking returns True (i.e. fraud is detected) then risk is 1.0, else 0.0.
    """
    try:
        from ai_features.fraud_detection import check_booking
        return 1.0 if check_booking(instance) else 0.0
    except Exception as e:
        logger.error("Error calculating fraud risk for instance %s: %s", instance.pk, e)
        return 0.0
