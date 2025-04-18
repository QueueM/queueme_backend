# followApp/models.py
from django.db import models
from shopApp.models import ShopDetailsModel
from customersApp.models import CustomersDetailsModel

class ShopFollow(models.Model):
    """
    Records that a customer (CustomersDetailsModel) follows a shop (ShopDetailsModel).
    Each (customer, shop) pair is unique.
    """
    customer = models.ForeignKey(
        CustomersDetailsModel,
        on_delete=models.CASCADE,
        related_name="shop_follows"
    )
    shop = models.ForeignKey(
        ShopDetailsModel,
        on_delete=models.CASCADE,
        related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'shop')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer} follows {self.shop}"
