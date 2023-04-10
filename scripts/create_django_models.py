import json, os, inspect, traceback
from django.db import models
from django.conf import settings
import django
django.setup()

def main(project_name='living_and_the_son_of_death'):
    print(f"BEGIN: project_name='{project_name}'")
    settings.configure()
    try:
        project_location = f'projects/{project_name}'
        schemas_location = f'{project_location}/schemas'
        model_file_target_dir = f'models/{project_name}'
        
        json_file_location=schemas_location

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


        def create_model_from_json_file(filepath, filename):
            print(f"loading json from {filepath}\n")
            with open(filepath, 'r') as json_file:
                json_data = json.load(json_file)
            
            camel_case_filename = ''.join(word.capitalize() for word in filename[:-3].split('_')).replace(".py", "")
            
            camel_case_filename='NovelModel'
            print(f"creating dynamic model {camel_case_filename} based on json in {filename}\n\n")
            return create_dynamic_model(json_data, f'{camel_case_filename}')

        dynamic_models = []
        filename='output.json'
        json_file_location=f'{project_location}'
        print(f"loop through files in dir {json_file_location}\n")
        # for filename in os.listdir(json_file_location):
        # if filename.endswith('.json'):
        filepath = os.path.join(json_file_location, filename)
        dynamic_models.append(create_model_from_json_file(filepath, filename))


        print("looping dynamic_models and writing to file\n")
        for model in dynamic_models:
            
            print("getting model source codee\n")
            source_code = inspect.getsource(model)

            print("creating filename from model name {model.__name__}\n")
            filename = model.__name__ + ".py"

            print(f"writing source code for {model.__name__} to file {model_file_target_dir}{filename}\n")
            with open(os.path.join(model_file_target_dir, filename), "w") as f:
                f.write(source_code)
                    
    except Exception as e:
        print("=====================ERROR=====================\n\n here is the contents of the failing .py file:\n\n")
        # print the contents of the file before the traceback
        with open("create_django_models.py", "r") as f:
            print(f.read())
        print("\n\n")
        # print the traceback as usual
        traceback.print_exc()

if __name__ == "__main__":
    main("living_and_the_son_of_death")