from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import models

class Command(BaseCommand):
    help = "Return dictionary of schema related to the Book model."

    def return_dict_of_schema(self):
        print("LOG: return_dict_of_schema Creating dictionary of model")
        book_model = apps.get_model("noveller", "Book")
        related_models = {}
        
        
        print(f"LOG: return_dict_of_schema Looping through models in {apps}")
        for model in apps.get_models():
            
            print(f"LOG: return_dict_of_schema looping thropugh fields of {model}")
            for field in model._meta.get_fields():
                print(f"LOG: return_dict_of_schema Working with {field} of {model}")
        
                if isinstance(field, (models.OneToOneField, models.ForeignKey, models.ManyToManyField)):
                    print(f"LOG: return_dict_of_schema {field} is a an instance of a relationship")
                    
                    if field.related_model == book_model:
                        relationship_type = "OneToOne" if isinstance(field, models.OneToOneField) else \
                                            "ForeignKey" if isinstance(field, models.ForeignKey) else "ManyToMany"
                        related_models[model.__name__] = {"model": model, "relationship": relationship_type}
        
        print(f"LOG {related_models}")
        return related_models
        
        
        
        # print(f"LOG: return_dict_of_schema Looping through {apps.get_models()}")
        # for model in apps.get_models():
        #     print(f"LOG: return_dict_of_schema Working with {model}")
        #     if issubclass(model, book_model.__class__):
        #         print(f"LOG: return_dict_of_schema {model} is subclass of {book_model}")
        #         related_models[model.__name__] = model
        # print(f"LOG: return_dict_of_schema Dictionary created: {related_models}")
        # return related_models

    def handle(self, *args, **options):
        self.return_dict_of_schema()