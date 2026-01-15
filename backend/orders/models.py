from django.db import models
from users.models import User
from products.models import Product
import uuid
# Create your models here.

class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'pending'
        PROCESSING = 'processing'
        SHIPPED = 'shipped'
        DELIVERED = 'delivered'
        CANCELLED = 'cancelled'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status= models.CharField(choices=StatusChoices.choices, default=StatusChoices.PENDING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
    
  
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)