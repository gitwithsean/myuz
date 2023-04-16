from django import forms
from django.apps import apps
from noveller.models import *

all_noveller_model_form_tuples = []

class FormMaker:
    global all_noveller_model_form_tuples
    # for every model in the app, create a form and store it 
    # as a tuple with its model in a list of those tuples
    for model_name in apps.all_models['noveller']:
        # Omit relationship model classes
        if '_' not in model_name:
            
            # print(f"Creating form for {model_name}")
            model = apps.get_model('noveller', model_name)
            
            # print(f"Creating form class for {model}")
            form_class = type(
                    f'{model_name}Form', 
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
            all_noveller_model_form_tuples.append(form_tuple)

def get_noveller_model_form_tuples_for(model_names):
    global all_noveller_model_form_tuples
    result = []
    for tuple in all_noveller_model_form_tuples:
        for model_name in model_names:
            if tuple['model_class'].__name__.lower() == model_name:
                result.append(tuple)
    return result