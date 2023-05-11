from django.contrib import admin
from django.db import models

for model in dir():
    try:
        if issubclass(eval(model), models.Model):
            admin.site.register(eval(model))
    except:
        pass