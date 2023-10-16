from django.db import models
from django.contrib.auth.models import User  # Import User model if not already imported


class Product(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)


    def save(self, *args, **kwargs):
        # Calculate the total price for this cart item when saving
        self.total = self.product.price * self.quantity
        super(CartItem, self).save(*args, **kwargs)