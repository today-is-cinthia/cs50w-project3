from django.contrib import admin
from .models import (Menu, Size, PizzaStyle, Topping, Ingredient, Extra, PastaStyle, SaladStyle, DinnerPlatterStyle, Pizza, Sub, Pasta, Salad, DinnerPlatter,CartItem, OrderItem)

# Register your models here.




class PizzaAdmin(admin.ModelAdmin):
    list_display = ('id', 'style', 'size', 'num_toppings', 'price', 'is_special', 'toppings_list')


class SubAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredients', 'size', 'price', 'extras_list')


class PastaAdmin(admin.ModelAdmin):
    list_display = ('id', 'style', 'price')


class SaladAdmin(admin.ModelAdmin):
    list_display = ('id', 'style', 'price')


class DinnerPlatterAdmin(admin.ModelAdmin):
    list_display = ('id', 'style', 'size', 'price')


admin.site.register(Menu)
admin.site.register(Size)
admin.site.register(PizzaStyle)
admin.site.register(Topping)
admin.site.register(Ingredient)
admin.site.register(Extra)
admin.site.register(PastaStyle)
admin.site.register(SaladStyle)
admin.site.register(DinnerPlatterStyle)
admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Sub, SubAdmin)
admin.site.register(Pasta, PastaAdmin)
admin.site.register(Salad, SaladAdmin)
admin.site.register(DinnerPlatter, DinnerPlatterAdmin)



class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'is_complete', 'menu', 'size', 'style', 'additional', 'is_special', 'price', 'user_id')
    list_editable = ['is_complete']


admin.site.register(CartItem)
admin.site.register(OrderItem, OrderItemAdmin)