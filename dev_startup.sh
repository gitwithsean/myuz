
. venv/bin/activate

python manage.py check
python manage.py makemigrations
python manage.py migrate

dateTime=$(date +"%y.%m.%d_%H:%M")
cp db.sqlite3 phusis/migrations/db_backups/db${dateTime}.sqlite3.bckup

# Delete db backups older than 5 days but always keep the last 10
while [ "$(find phusis/migrations/db_backups -type f -mtime +5 | wc -l)" -gt "10" ]; do find noveller/migrations/db_backups -type f -mtime +5 -exec rm {} \;; done

cp db.sqlite3 phusis/migrations/db_backups/db${dateTime}.sqlite3

python manage.py runserver
