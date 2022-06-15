
from cgitb import small
from pyexpat import model
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.name}"

class Regular_pizza(models.Model):
    name = models.CharField(max_length=64)
    small = models.DecimalField(max_digits=4, decimal_places=2)
    large = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.small} - {self.large}"

class Topping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Sub(models.Model):
    name=models.CharField(max_length=64)
    small = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    large=models.DecimalField(max_digits=4, decimal_places=2)
    def __str__(self):
        return f"{self.name} - {self.small} - {self.large}"

class Pasta(models.Model):
    name=models.CharField(max_length=64)
    price= models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price}"

class Salad(models.Model):
    name=models.CharField(max_length=64)
    price= models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price}"

class Dinner_platter(models.Model):
    name=models.CharField(max_length=64)
    small=models.DecimalField(max_digits=4, decimal_places=2)
    large=models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.small} - {self.large}"

class User_order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.IntegerField()
    topping_allowance = models.IntegerField(default=0)
    status= models.CharField(max_length=64, default='initiated')

    def __str__(self):
        return f"{self.user} - {self.order_number}- {self.status} topping_allowance: - {self.topping_allowance}"

class Order2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.IntegerField()
    category = models.CharField(max_length=64, null=True)
    name = models.CharField(max_length=64)
    price=models.DecimalField(max_digits=64, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price}"

class Oder_counter(models.Model):
    counter=models.IntegerField()
    def __str__(self):
        return f" Order no. {self.counter}"
    

