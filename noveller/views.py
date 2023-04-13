from django.http import HttpResponse
from django.apps import apps
from rest_framework import generics
from .models import *
from .serializers import ModelSerializer
from pprint import pprint
  
def index(request):
    return HttpResponse("Hello, world. You're at the noveller index.")


class NovellerModelListCreateViewMaker(generics.ListCreateAPIView):
    all_noveller_create_views = []
    
    models = apps.all_models['noveller']
    for model_name in models:
        model = models[model_name]
        for entry in ModelSerializer.all_serializers:
            if '_' not in model_name and model.expose_rest == True and entry['model'] == model:
                serializer_class = entry["serializer_class"]
                class_name = model_name + 'ListCreateView'
                meta_attrs = {
                    'model': model
                }
                noveller_create_view_class = type(class_name, (generics.ListCreateAPIView,), {'Meta': type('Meta', (), meta_attrs)})
                all_noveller_create_views.append({"model":model, "view_class": noveller_create_view_class})
                

class NovellerModelRUDViewMaker(generics.RetrieveUpdateDestroyAPIView):
    all_noveller_rud_views = []
    
    models = apps.all_models['noveller']
    for model_name in models:
        model = models[model_name]
        for entry in ModelSerializer.all_serializers:
            if '_' not in model_name and model.expose_rest == True and entry['model'] == model:
                serializer_class = entry["serializer_class"]
                class_name = model_name + 'ListCreateView'
                meta_attrs = {
                    'model': model
                }
                noveller_rud_view_class = type(class_name, (generics.RetrieveUpdateDestroyAPIView,), {'Meta': type('Meta', (), meta_attrs)})
                all_noveller_rud_views.append({"model":model, "view_class": noveller_rud_view_class})
