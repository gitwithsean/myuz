from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .agent_attributes import *
from .agent_models import *
# from pprint import pprint

all_phusis_model_serializer_tuples = []

class SerializerMaker:
    global all_phusis_model_serializer_tuples
    # for every model in the app, create a serializer and store it 
    # as a tuple with it's model in a list of those tuples
    
    
    agent_model_classes = AbstractAgent.__subclasses__()    
    # agent_model_classes.append(AbstractAgent)
    # agent_model_classes.append(Script)
    agent_model_classes.append(OrchestrationAgent) #OrchestrationAgent is not a subclass of abstract agent so needs to be added
    # print(f"looping through the following list of models in phusis {apps.all_models['phusis']}")
    for agent_model_class in agent_model_classes:
        # Omit relationship model classes and Singletons
        if '_' not in agent_model_class.__name__ and 'singleton' not in agent_model_class.__name__:
            try:
                # print(f"{agent_model_class.__name__ }")
                # print(f"{agent_model_class}")
                class_name = agent_model_class.__name__ + 'Serializer'
                meta_attrs = {
                    'model': agent_model_class,
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
                all_phusis_model_serializer_tuples.append({"model_class":agent_model_class, "serializer_class": serializer_class})
            except ObjectDoesNotExist as e:
                print(f"Could not retrieve model {agent_model_class.__name__} from the app. Error: {e}")
            
def get_phusis_model_serializer_tuples_for(model_names):
    global all_phusis_model_serializer_tuples
    list = []
    for tuple in all_phusis_model_serializer_tuples:
        for model_name in model_names:
            if tuple['model_class'].__name__.lower() == model_name:
                # print(f"checking {tuple['model_class'].__name__.lower()} against {model_name}")
                # print(f"it's a match!")
                # pprint(tuple)
                list.append(tuple)
                
    return list            