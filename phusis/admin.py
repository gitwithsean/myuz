from django.contrib import admin
from django.db import models
from django.forms import inlineformset_factory
from .agent_models import *

for model in dir():
    try:
        if issubclass(eval(model), models.Model):
            admin.site.register(eval(model))
    except:
        pass