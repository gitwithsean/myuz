from django import forms
from django.apps import apps
from phusis.agent_attributes import *
from phusis.agent_models import AbstractAgent, OrchestrationAgent

all_phusis_model_form_tuples = []

class AgentFormMaker:
    global all_phusis_model_form_tuples
    # for every model in the app, create a form and store it 
    # as a tuple with its model in a list of those tuples
    
    agent_model_classes = AbstractAgent.__subclasses__()
    # agent_model_classes.append(AbstractAgent)
    # agent_model_classes.append(OrchestrationAgent) #OrchestrationAgent is not a subclass of abstract agent so needs to be added
    # print(f"phusis.forms.AgentFormMaker: looping through the following list of models in phusis {agent_model_classes}") 
    for agent_model_class in agent_model_classes:       
        # Omit relationship classes and Singletons
        if '_' not in agent_model_class.__name__ and 'Singleton' not in agent_model_class.__name__:          
            # print(f"phusis.forms.AgentFormMaker: Creating form class for {agent_model_class.__name__}")
            try:
                model_class = apps.get_model('phusis', agent_model_class.__name__)
            except:
                model_class = apps.get_model('noveller', agent_model_class.__name__)   
            # pprint(vars(model_class))
            
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
            
            # print(f"phusis.forms.AgentFormMaker: Creating tuple for {form_class}")
            form_tuple = {"model_class": agent_model_class, "form_class": form_class}
            
            # print(f"phusis.forms.AgentFormMaker: Creating form for {form_tuple}")
            all_phusis_model_form_tuples.append(form_tuple)
    # print(f"phusis.forms.AgentFormMaker: all_phusis_model_form_tuples  {all_phusis_model_form_tuples}")        

def get_phusis_model_form_tuples_for(model_names):
    global all_phusis_model_form_tuples
    # pprint(all_phusis_model_form_tuples)
    result = []
    for tuple in all_phusis_model_form_tuples:
        # print(f"phusis.forms.get_phusis_model_form_tuples_for: tuple {tuple}")
        for model_name in model_names:
            # print(f"phusis.forms.get_phusis_model_form_tuples_for:  tuple['model_class'].class_display_name: { tuple['model_class'].class_display_name} \nmodel_name: {model_name}")
            if tuple['model_class'].__name__ == model_name:
                # print(f"phusis.forms.get_phusis_model_form_tuples_for: tuple['model_class'].__name__.lower() {tuple['model_class'].__name__.lower()}")``
                result.append(tuple)
    # print(f"phusis.forms.get_phusis_model_form_tuples_for: {result}")            
    return result
