from django.contrib import admin
from django.forms import inlineformset_factory
from .noveller_models import *
from .noveller_agents import *

for model in dir():
    try:
        if issubclass(eval(model), models.Model):
            admin.site.register(eval(model))
    except:
        pass