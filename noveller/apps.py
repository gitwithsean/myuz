from django.apps import AppConfig
from django.db.models import ManyToManyField
from django.apps import apps

class NovellerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "noveller"
    
    def ready(self):
        from phusis.models import Agent
        for model in apps.get_models():
            if model.__module__ == self.name+'.models':
                field_name = 'responsibilities'
                field = ManyToManyField(Agent, blank=True)
                setattr(model, field_name, field)