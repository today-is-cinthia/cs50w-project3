from django.forms import ModelForm, CheckboxSelectMultiple
from .models import Pizza, Sub, Pasta, Salad, DinnerPlatter

class PizzaForm(ModelForm):
    class Meta:
        model = Pizza
        exclude = ['menu', 'price']
        widgets = {
            'toppings' : CheckboxSelectMultiple,
        }
        labels = {
            'num_toppings': 'Number of toppings',
            'is_special': 'Special Pizza' 
        }

class SubForm(ModelForm):
    class Meta:
        model = Sub
        exclude = ['menu', 'price']
        widgets = {
            'extras': CheckboxSelectMultiple,
        }
        labels = {
            'ingredients': 'Ingredients'
        }

class PastaForm(ModelForm):
    class Meta:
        model = Pasta
        exclude = ['menu', 'price']

class SaladForm(ModelForm):
    class Meta:
        model = Salad
        exclude = ['menu', 'price']


class DinnerPlatterForm(ModelForm):
    class Meta:
        model = DinnerPlatter
        exclude = ['menu', 'price']