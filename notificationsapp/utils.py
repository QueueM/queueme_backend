# notificationsapp/utils.py
from notificationsapp.models import NotificationModel

def create_notification(user, title, message):
    """
    Creates a notification for a given user.
    """
    return NotificationModel.objects.create(user=user, title=title, message=message)

def notify_followers(shop, title, message):
    """
    Notifies every customer who follows the shop.
    Assumes that followApp.ShopFollow exists and each follow has a customer linked to a User.
    """
    from followApp.models import ShopFollow
    follows = ShopFollow.objects.filter(shop=shop)
    for follow in follows:
        create_notification(follow.customer.user, title, message)
