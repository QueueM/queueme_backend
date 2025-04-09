# authApp/signals.py
import logging
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
from customClasses.ai_utils import get_fraud_risk  # Ensure this function is defined for risk analysis
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model()

@receiver(user_logged_in)
def analyze_login_risk(sender, request, user, **kwargs):
    """
    When a user successfully logs in, analyze the login risk.
    If the risk score is high, log a warning or trigger additional security measures.
    """
    try:
        # Here, we pass the user instance to our risk evaluation function.
        risk_score = get_fraud_risk(user)
        threshold = 0.7  # Define an appropriate threshold for your application
        if risk_score > threshold:
            logger.warning(f"High risk score ({risk_score}) detected for user {user.username}.")
            # Optionally, take extra action: e.g., flag the account for review or require MFA.
    except Exception as e:
        logger.error(f"Error analyzing login risk for user {user.username}: {e}")

@receiver(user_login_failed)
def handle_failed_login(sender, credentials, request, **kwargs):
    """
    When a login attempt fails, handle the event.
    You can also use AI functions to track or evaluate failed login attempts.
    """
    try:
        username = credentials.get('username', 'Unknown')
        logger.warning(f"Login failed for username: {username}.")
        # Optionally, add AI-driven logic here, for example:
        # risk_score = get_fraud_risk_for_failed_attempt(credentials, request)
        # logger.debug(f"Risk score for failed login attempt for username {username} is {risk_score}")
    except Exception as e:
        logger.error(f"Error handling failed login: {e}")
