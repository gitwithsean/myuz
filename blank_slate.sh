#!/bin/bash

set -e

help_message=$'
Usage: $(basename "$0") [OPTIONS]

Options:
  db:       Drop and recreate the myuz database. 
  db_init:  Depends on db being set - intits the db with agents and book
  pinecone: Delete and recreate the myuz pinecone index. 
  --help:   Display this help and exit. 

example: ./blank_slate.sh db venv pinecone'

REINIT_DB=false
REINIT_PINECONE=false
REINIT_DB_DATA=false
MYUZ_DIR=$(pwd)
SCRIPTS_DIR="${MYUZ_DIR}/scripts"

for arg in "$@"
do
    case $arg in
        all)
            REINIT_DB=true
            REINIT_PINECONE=true
            REINIT_DB_DATA=true
            ;;
        db)
            REINIT_DB=true
            ;;
        db_init)
            REINIT_DB_DATA=true
            ;;
        pinecone)
            REINIT_PINECONE=true
            ;;
        --help)
            REINIT_PINECONE=true
            ;;
        *)
            echo -e "$help_message"
            exit 1
            ;;
    esac
done

echo "REINIT_DB ${REINIT_DB}"
echo "REINIT_DB_DATA ${REINIT_DB_DATA}"
echo "REINIT_PINECONE ${REINIT_PINECONE}"
echo "MYUZ_DIR ${MYUZ_DIR}"

if [ $REINIT_PINECONE  == true ]; then

    cd $MYUZ_DIR
    INDEX='phusis'

    PINECONE_ENV=$(cat ${MYUZ_DIR}/.secrets/pinecone_api_region | tr -d '\n')
    PINECONE_API_KEY=$(cat ${MYUZ_DIR}/.secrets/pinecone_api_key | tr -d '\n')

    echo "Deleting pinecone index"
    echo "curl -i -X DELETE https://controller.${PINECONE_ENV}.pinecone.io/databases/${INDEX} \
    -H "Api-Key: ${PINECONE_API_KEY}""
    curl -i -X DELETE https://controller.${PINECONE_ENV}.pinecone.io/databases/${INDEX} \
    -H "Api-Key: ${PINECONE_API_KEY}"
    echo "PINECONE INDEX ${INDEX} DELETED" 
fi

if [ $REINIT_DB == true ]; then

    cd $SCRIPTS_DIR
    python drop_and_recreate_myuz_db.py
    cd $MYUZ_DIR

    echo "deleting existing migrations files"
    rm -rf **/migrations/*.py
    rm -rf **/migrations/__pycache__

    echo "making new migrations files"
    python manage.py check
    python manage.py makemigrations noveller --empty
    python manage.py makemigrations phusis --empty
    python manage.py makemigrations phusis
    python manage.py makemigrations noveller

    echo "migrating"
    python manage.py migrate 

    echo "REINIT_DB_DATA ${REINIT_DB_DATA}"

    if [ $REINIT_DB_DATA == true ]; then

        echo "initializing db data - agents"
        python manage.py init_agents noveller

        echo "initializing db data - project"
        python manage.py init_project noveller living_and_the_son_of_death
    fi
fi

