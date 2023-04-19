cd ..

#re-init python env
rm -rf venv
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt

#delete the db and migrations
rm -rf db.sqlite3
rm -rf **/migrations/*.py

#delete the pinecone index
read -r PINECONE_ENV < ./secrets/pinecone_api_region
read -r PINECONE_API_KEY < ./secrets/pinecone_api_key
INDEX='phusis'
curl -i -X DELETE https://controller.${PINECONE_ENV}.pinecone.io/databases/${INDEX} \
  -H "Api-Key: ${PINECONE_API_KEY}"

if ${1} == 'init':
    #re-init base db and pinecone index
    pip freeze > requirements.txt
    python manage.py check
    python manage.py makemigrations noveller
    python manage.py migrate noveller
    python manage.py makemigrations phusis
    python manage.py migrate phusis
    python manage.py check
    python manage.py init_db phusis