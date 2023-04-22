from django import forms
from django.apps import apps
from phusis.agent_models import *
from noveller.models import *
from django.db.models import Q

all_noveller_model_form_tuples = []

class BookForm(forms.ModelForm):
    
    # print(colored(f"Creating specific form class for BookForm as it has references from another app", "green"))  
    
    class Meta:
        model = Book
        fields = [
           #'id', #AbstractPhusisProject
           #'name', #AbstractPhusisProject
           'elaboration',
           'expose_rest',
           'elaboration',
           'settings',
           'plot',
           'chapters',
           'characters',
           'themes',
           'genre',
           'target_audiences'
        ]
        
    # # Fields from the AbstractPhusisProject class
    # project_agents = forms.ModelMultipleChoiceField(
    #     queryset=AbstractAgent.__subclasses__(),
    #     required=False,
    # )

    # project_script = forms.ModelChoiceField(
    #     queryset=PhusisScript.objects.all(),
    #     required=False,
    # )

class FormMaker:
    global all_noveller_model_form_tuples
    # for every model in the app, create a form and store it 
    # as a tuple with its model in a list of those tuples
    for model_name in apps.all_models['noveller']:
        # Omit relationship model classes
        if '_' not in model_name:
            
            # print(f"Creating form for {model_name}")
            model = apps.get_model('noveller', model_name)
                         
            if model.__name__ == 'Book':
                # print(colored(f"Creating specific form class for {model} as it has references from another app", "green"))
                
                agent_models = [model for model in AbstractAgent.__subclasses__()]

                for agent_model in agent_models:
                    field_name = agent_model.__name__.lower()
                    form_field = forms.ModelChoiceField(queryset=agent_model.objects.all())
                    BookForm.base_fields[field_name] = form_field
                    BookForm.Meta.fields.append(field_name)
                    
                    form_class = BookForm
                    
            else:           
                # print(colored(f"Creating form class for {model}", "green"))  
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