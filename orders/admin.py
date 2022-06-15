from django.contrib import admin
from .models import (Category, Regular_pizza, Topping, Sub,  Pasta, Salad, Dinner_platter, User_order, Order2, Oder_counter)

# Register your models here.

admin.site.register(Category)
admin.site.register(Regular_pizza)
admin.site.register(Topping)
admin.site.register(Sub)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Dinner_platter)
admin.site.register(User_order)
admin.site.register(Order2)
admin.site.register(Oder_counter)
