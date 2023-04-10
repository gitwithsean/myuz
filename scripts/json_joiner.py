import os
import json

# Set the directory containing the JSON files
directory = '../projects/living_and_the_son_of_death'

# Initialize an empty dictionary to hold the merged data
data = {}

# Loop through each JSON file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        # Read in the JSON file and merge it with the existing data
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
            data.update(json.load(f))

# Write the merged data to a new JSON file
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)