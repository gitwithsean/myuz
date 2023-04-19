ENDPOINT=worldbuildingagent
CLASS_NAME=WorldBuildingAgent
JSON_DATA_ARRAY=$(cat ./data_to_load/phusis-secret-sauce/noveller_data/${ENDPOINT}s.json | jq -c '.[]')

for data in "${JSON_DATA_ARRAY[@]}"
echo $data
do
    curl -X POST -H "Content-Type: application/json" -d "$data" -u 'user:password' "http://127.0.0.1:8000/api/${agent_class_name}"
done