from django import forms
from django.apps import apps
from phusis.agent_models import *
from noveller.noveller_models import *
from noveller.noveller_engines import *
from noveller.noveller_agents import *

all_noveller_model_form_tuples = []

class BookForm(forms.ModelForm):
    
    # print(colored(f"Creating specific form class for BookForm as it has references from another app", "green"))  
    
    class Meta:
        model = Book
        fields = [
            'name',
            'settings',
            'plots',
            'chapters',
            'characters',
            'themes',
            'genres',
            'target_audiences',
            'elaboration',
        ]

class FormMaker:
    global all_noveller_model_form_tuples
    # for every model in the app, create a form and store it 
    # as a tuple with its model in a list of those tuples
    
    for model_name in apps.all_models['noveller']:
        # Omit relationship model classes
        if '_' not in model_name:
            
            # print(f"\nCreating form for {model_name}")
            model = apps.get_model('noveller', model_name)
            
            # print(colored(f"FormMaker: model: {model} fields:", "yellow"))
            # pprint(model._meta.get_fields()) 
             
            included_fields = [f.name for f in model._meta.get_fields() if f.name not in ['content_type', 'id', 'useragentsingleton'] and not isinstance(f, (GenericRelation)) and isinstance(f, (models.Field, models.ManyToManyField, models.ForeignKey))]

            # print(colored(f"FormMaker: {model_name} included_fields: {included_fields}", "yellow"))
               
            # print(colored(f"Creating form class for {model}", "green")) 
            
            if model.__name__ == 'Book':
                # print(colored(f"Creating specific form class for {model} as it has references from another app", "green"))
                
                # agent_models = [model for model in AbstractAgent.__subclasses__()]

                # for agent_model in agent_models:
                #     field_name = agent_model.__name__.lower()
                #     form_field = forms.ModelChoiceField(queryset=agent_model.objects.all())
                #     BookForm.base_fields[field_name] = form_field
                #     BookForm.Meta.fields.append(field_name)
                    
                    form_class = BookForm
            else:            
                
                # print(colored(f"\n\nFormMaker: Data going into making the form for {model}\nmodel: {model}\nmodel.__name__: {model.__name__}\nincluded_fields: {included_fields}\n\n", "yellow"))
                
                # pprint(vars(model))
                
                form_class = type(
                    f'{model.__name__}Form',
                    (forms.ModelForm,),
                    {
                        'Meta': type(
                            'Meta', (), {
                                'model': model,
                                'fields': included_fields,
                            }
                        )
                    }
                )
             
            
            # print(f"Creating tuple for {form_class}")
            form_tuple = {"model_class": model, "form_class": form_class}
            all_noveller_model_form_tuples.append(form_tuple)


def get_noveller_model_form_tuples_for(model_names):
    global all_noveller_model_form_tuples
    result = []
    for tuple in all_noveller_model_form_tuples:
        # pprint(tuple)
        for model_name in model_names:
            if tuple['model_class'].__name__.lower() == model_name:
                result.append(tuple)
    return result