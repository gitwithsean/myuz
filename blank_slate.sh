
. venv/bin/activate

#delete the db and migrations
rm -rf db.sqlite3
rm -rf **/migrations/*.py
rm -rf requirements.txt

#delete the pinecone index
read -r PINECONE_ENV < ./secrets/pinecone_api_region
read -r PINECONE_API_KEY < ./secrets/pinecone_api_key
INDEX='phusis'
curl -i -X DELETE https://controller.${PINECONE_ENV}.pinecone.io/databases/${INDEX} \
  -H "Api-Key: ${PINECONE_API_KEY}"

#re-init base db
pip freeze > requirements.txt
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py check
