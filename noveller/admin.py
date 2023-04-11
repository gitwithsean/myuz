from django.contrib import admin
from django.forms import inlineformset_factory
from .models import *

noveller_models = []

print("LOG: noveller.admin loading models for admin view")
for model in dir():
    try:
        if issubclass(eval(model), models.Model):
            admin.site.register(eval(model))
            noveller_models.append(model)
    except:
        pass