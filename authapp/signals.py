import logging
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
from customClasses.ai_utils import get_fraud_risk  # Ensure this function is implemented in your ai_utils module
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model()

@receiver(user_logged_in)
def analyze_login_risk(sender, request, user, **kwargs):
    try:
        risk_score = get_fraud_risk(user)
        threshold = 0.7  # Customize threshold as needed
        if risk_score > threshold:
            logger.warning(f"High risk score ({risk_score}) detected for user {user.username}.")
            # Here you could trigger additional security measures (MFA, notifications, etc.)
    except Exception as e:
        logger.error(f"Error analyzing login risk for user {user.username}: {e}")

@receiver(user_login_failed)
def handle_failed_login(sender, credentials, request, **kwargs):
    try:
        username = credentials.get('username', 'Unknown')
        logger.warning(f"Login failed for username: {username}.")
        # Optionally, trigger further actions or log additional details
    except Exception as e:
        logger.error(f"Error handling failed login: {e}")
