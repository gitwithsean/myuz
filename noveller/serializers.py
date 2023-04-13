from django.apps import apps
from rest_framework import serializers
from pprint import pprint

class ModelSerializer():

    all_serializers = []

    models = apps.all_models['noveller']

    for model_name in models:
        model = models[model_name]
        if '_' not in model_name and model.expose_rest == True: 
            class_name = model_name + 'Serializer'
            meta_attrs = {
                'model': model,
                'fields': '__all__'
            }
            serializer_class = type(class_name, (serializers.ModelSerializer,), {'Meta': type('Meta', (), meta_attrs)})
            globals()[class_name] = serializer_class
            all_serializers.append({"model":model, "serializer_class": serializer_class})