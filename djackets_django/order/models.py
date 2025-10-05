from django.db import models
from django.contrib.auth.models import User
from product.models import Product

class order(models.Model):
  user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
  last_name = models.CharField(max_length=100)
  first_name = models.CharField(max_length=100)
  email = models.CharField(max_length=100)
  address = models.CharField(max_length=100)
  zipcode = models.CharField(max_length=20)
  place = models.CharField(max_length=100)
  phone = models.CharField(max_length=20)
  created_at = models.DateTimeField(auto_now_add=True)
  paid_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
  stripe_token = models.CharField(max_length=100)

  class Meta:
    ordering = ('-created_at',)

  def __str__(self):
    return self.first_name


class orderItem(models.Model):
  order = models.ForeignKey(order, related_name='items', on_delete=models.CASCADE)
  product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
  price = models.DecimalField(max_digits=8, decimal_places=2)
  quantity = models.PositiveIntegerField(default=1)

  def __str__(self):
    return '%s' % self.id
