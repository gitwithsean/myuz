from django.apps import apps
from rest_framework import serializers
from .noveller_models import *
# from pprint import pprint

all_noveller_model_serializer_tuples = []

class SerializerMaker:
    global all_noveller_model_serializer_tuples
    # for every model in the app, create a serializer and store it 
    # as a tuple with it's model in a list of those tuples
    for model_name in apps.all_models['noveller']:
        #Omit relationship model classes
        if '_' not in model_name:
            try:
                model_class = apps.get_model('noveller', model_name)
                class_name = model_name + 'Serializer'
                meta_attrs = {
                    'model': model_class,
                    'fields': '__all__'
                }
                
                serializer_class = type(
                    class_name, 
                    (serializers.ModelSerializer,), 
                    {
                        'Meta': type('Meta', (), meta_attrs)
                    }
                
                )
                globals()[class_name] = serializer_class
                all_noveller_model_serializer_tuples.append({"model_class":model_class, "serializer_class": serializer_class})
            except apps.exceptions.LookupError as e:
                print(f"Could not retrieve model {model_name} from the app. Error: {e}")
            
def get_noveller_model_serializer_tuples_for(model_names):
    global all_noveller_model_serializer_tuples
    list = []
    for tuple in all_noveller_model_serializer_tuples:
        for model_name in model_names:
            if tuple['model_class'].__name__.lower() == model_name:
                # print(f"checking {tuple['model_class'].__name__.lower()} against {model_name}")
                # print(f"it's a match!")
                # pprint(tuple)
                list.append(tuple)
                
    return list            