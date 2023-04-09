from genson import SchemaBuilder
import os, json, genson

project_name = 'living_and_the_son_of_death'

#load json file
def read_file(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

#create schema from json
def create_schema(filepath):
    data_sample = read_file(filepath)
    builder = SchemaBuilder()
    builder.add_object(data_sample)
    schema_dict = builder.to_schema()
    return schema_dict
    
def write_schema_file(filename, schema_dict):
    schemaFile = os.path.join(
        'living_and_the_son_of_death', 
        "schemas",
        f"{filename}")
    os.makedirs(os.path.dirname(schemaFile), exist_ok=True)
    with open(schemaFile, "w") as f:
        json.dump(schema_dict, f, indent=2) 

def schema_file_from_json_file(filename, filepath):
    schema_dict = create_schema(filepath)
    write_schema_file(filename, schema_dict)
    
# loop through files in dir
for filename in os.listdir(project_name):
    if filename.endswith('.json'):
        filepath = os.path.join(project_name, filename)
        schema_file_from_json_file(filename, filepath)
