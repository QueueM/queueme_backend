# ai_features/churn_prediction.py
"""
This module provides a dummy implementation for churn risk prediction
for your subscriptionApp.
"""

def calculate_churn_risk(subscription_instance):
    """
    Calculates a churn risk score for a subscription instance.
    
    Returns:
      A float value between 0 and 1 representing the churn risk.
    
    Dummy implementation:
      - Returns 0.9 if the subscription has an attribute 'is_cancelled' set to True,
      - Otherwise, returns 0.3.
    """
    if hasattr(subscription_instance, 'is_cancelled') and subscription_instance.is_cancelled:
        return 0.9
    return 0.3
