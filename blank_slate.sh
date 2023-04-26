#!/bin/bash

help_message=$'
Usage: $(basename "$0") [OPTIONS]

Options:
  db:       Drop and recreate the myuz database. 
  db_init:  Depends on db being set - intits the db with agents and book
  venv:     Delete and recreate the Python virtual environment. 
  pinecone: Delete and recreate the myuz pinecone index. 
  --help:   Display this help and exit. 

example: ./blank_slate.sh db venv pinecone'

REINIT_DB=false
REINIT_VENV=false
REINIT_PINECONE=false
REINIT_DB_DATA=false
MYUZ_DIR=$(pwd)
SCRIPTS_DIR="${MYUZ_DIR}/scripts"

echo "MYUZ_DIR ${MYUZ_DIR}"
echo "SCRIPTS_DIR ${SCRIPTS_DIR}"

for arg in "$@"
do
    case $arg in
        all)
            echo 'all detected'
            REINIT_DB=true
            REINIT_PINECONE=true
            REINIT_VENV=true
            REINIT_DB_DATA=true
            ;;
        db)
            echo 'db detected'
            REINIT_DB=true
            ;;
        db_init)
            echo 'db_init detected'
            REINIT_DB_DATA=true
            ;;
        venv)
            echo 'venv detected'
            REINIT_VENV=true
            ;;
        pinecone)
            echo 'pinecone detected'
            REINIT_PINECONE=true
            ;;
        --help)
            echo '--help detected'
            REINIT_PINECONE=true
            ;;
        *)
            echo "Unknown argument: $arg"
            echo -e "$help_message"
            exit 1
            ;;
    esac
done

echo "REINIT_PINECONE ${REINIT_PINECONE}"

if [ $REINIT_PINECONE  == true ]; then
    cd $MYUZ_DIR
    INDEX='phusis'
    read -r PINECONE_ENV < $MYUZ_DIR/.secrets/pinecone_api_region
    read -r PINECONE_API_KEY < $MYUZ_DIR/.secrets/pinecone_api_key
    echo "DELETING PINECONE INDEX"
    curl -i -X DELETE https://controller.${PINECONE_ENV}.pinecone.io/databases/${INDEX} \
    -H "Api-Key: ${PINECONE_API_KEY}"
    echo "PINECONE INDEX ${INDEX} DELETED" 
fi

echo "REINIT_PINECONE ${REINIT_PINECONE}"

if [ $REINIT_DB == true ]; then
    cd $SCRIPTS_DIR
    python3 drop_and_recreate_myuz_db.py
    cd $MYUZ_DIR
    #delete migrations
    rm -rf **/migrations/*.py
    rm -rf **/migrations/__pycache__
    # python manage.py check
    python manage.py makemigrations noveller --empty
    python manage.py makemigrations phusis --empty
    python manage.py makemigrations phusis
    python manage.py makemigrations noveller
    python manage.py migrate 

    echo "REINIT_DB_DATA ${REINIT_DB_DATA}"

    if [ $REINIT_DB_DATA == true ]; then
        python manage init_agents phusis
        python manage init_book noveller
    fi
fi

echo "REINIT_VENV ${REINIT_VENV}"

if [ $REINIT_VENV == true ]; then
    cd $MYUZ_DIR
    pip freeze > requirements.txt
    #re-init python env
    rm -rf venv
    python -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt
fi

