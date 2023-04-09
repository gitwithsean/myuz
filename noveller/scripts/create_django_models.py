import json, os, inspect, traceback
import django
from django.db import models
from django.apps import apps

try:
    project_name = 'living_and_the_son_of_death'

    def create_dynamic_model(json_data, model_name):
        fields = {'__module__': __name__}
        for key in json_data.keys():
            if isinstance(json_data[key], str):
                fields[key] = models.CharField(max_length=100)
            elif isinstance(json_data[key], int):
                fields[key] = models.IntegerField()
            elif isinstance(json_data[key], float):
                fields[key] = models.FloatField()
            elif isinstance(json_data[key], bool):
                fields[key] = models.BooleanField()
            elif isinstance(json_data[key], list):
                fields[key] = models.JSONField()
            else:
                fields[key] = models.CharField(max_length=100)
        return type(model_name, (models.Model,), fields)


    def create_model_from_json_file(filepath):
        # Load JSON data from a file
        with open(filepath, 'r') as json_file:
            json_data = json.load(json_file)
        
        # Create a dynamic model based on the JSON data
        MyDynamicModel = create_dynamic_model(json_data, 'NovelModel')
        
        return MyDynamicModel

    dynamic_models = []
        
    # loop through files in dir
    for filename in os.listdir(project_name):
        if filename.endswith('.json'):
            filepath = os.path.join(project_name, filename)
            dynamic_models.append(create_model_from_json_file(filepath))


        # loop through dynamic_models and write to file
        for model in dynamic_models:
            # get model source code
            source_code = inspect.getsource(model)

            # create filename from model name
            filename = model.__name__ + ".py"

            # write source code to file
            with open(os.path.join(project_name, "models", filename), "w") as f:
                f.write(source_code)
                
except Exception as e:
    print("error, here is the contents of the failing .py file")
    # print the contents of the file before the traceback
    with open("create_django_models.py", "r") as f:
        print(f.read())
    print("\n\n")
    # print the traceback as usual
    traceback.print_exc()
