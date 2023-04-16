from django import forms
from django.apps import apps
from phusis.models import *
from phusis.models import AbstractAgent

all_phusis_model_form_tuples = []

class FormMaker:
    global all_phusis_model_form_tuples
    # for every model in the app, create a form and store it 
    # as a tuple with its model in a list of those tuples
    
    print(f"looping through the following list of models in phusis {apps.all_models['phusis']}")
    for agent_model_class in AbstractAgent.__subclasses__():
        # Omit relationship model classes and Singletons
        if '_' not in agent_model_class.__name__ and 'singleton' not in agent_model_class.__name__:
            
            # print(f"Creating form for {agent_model_class.__name__}")
            model = apps.get_model('phusis', agent_model_class.__name__)
                      
            print(f"Creating form class for {agent_model_class.__name__}")
            form_class = type(
                    f'{agent_model_class.__name__}Form', 
                    (forms.ModelForm,), 
                    {
                        'Meta': type(
                            'Meta', (), {
                                'model': model, 
                                'fields': '__all__'
                            }
                        )
                    }
                )
            
            # print(f"Creating tuple for {form_class}")
            form_tuple = {"model_class": model, "form_class": form_class}
            
            # print(f"Creating form for {form_tuple}")
            all_phusis_model_form_tuples.append(form_tuple)

def get_phusis_model_form_tuples_for(model_names):
    global all_phusis_model_form_tuples
    result = []
    for tuple in all_phusis_model_form_tuples:
        for model_name in model_names:
            if tuple['model_class'].__name__.lower() == model_name:
                result.append(tuple)
    return result
