from django import forms
from django.apps import apps
from phusis.models import *
from phusis.models import AbstractAgent, OrchestrationAgent, Script

all_phusis_model_form_tuples = []

class FormMaker:
    global all_phusis_model_form_tuples
    # for every model in the app, create a form and store it 
    # as a tuple with its model in a list of those tuples
    
    agent_model_classes = AbstractAgent.__subclasses__()
    # print(f"FORMS: looping through the following list of models in phusis {agent_model_classes}")  
    # agent_model_classes.append(AbstractAgent)
    # agent_model_classes.append(Script)
    agent_model_classes.append(OrchestrationAgent) #OrchestrationAgent is not a subclass of abstract agent so needs to be added
    # print(f"FORMS: looping through the following list of models in phusis {agent_model_classes}") 
    # print(f"FORMS: looping through the following list of models in phusis {apps.all_models['phusis']}")
    for agent_model_class in agent_model_classes:
        # Omit relationship model classes and Singletons
        if '_' not in agent_model_class.__name__ and 'singleton' not in agent_model_class.__name__:
                      
            # print(f"FORMS: Creating form class for {agent_model_class.__name__}")
            form_class = type(
                    f'{agent_model_class.__name__}Form', 
                    (forms.ModelForm,), 
                    {
                        'Meta': type(
                            'Meta', (), {
                                'model': agent_model_class, 
                                'fields': '__all__'
                            }
                        )
                    }
                )
            
            # print(f"FORMS Creating tuple for {form_class}")
            form_tuple = {"model_class": agent_model_class, "form_class": form_class}
            
            # print(f"FORMS Creating form for {form_tuple}")
            all_phusis_model_form_tuples.append(form_tuple)
    # print(f"all_phusis_model_form_tuples  {all_phusis_model_form_tuples}")        

def get_phusis_model_form_tuples_for(model_names):
    global all_phusis_model_form_tuples
    
    result = []
    for tuple in all_phusis_model_form_tuples:
        # print(f"FORMS: tuple {tuple}")
        for model_name in model_names:
            # print(f"FORMS: model_name: {model_name}")
            if tuple['model_class'].class_display_name == model_name:
                # print(f"FORMS: if {tuple['model_class']} == {model_name}:")
                # print(f"FORMS: tuple['model_class'].__name__.lower() {tuple['model_class'].__name__.lower()}")
                result.append(tuple)
    # print(f"FORMS: get_phusis_model_form_tuples_for.result {result}")            
    return result
