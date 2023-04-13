
. venv/myuz/bin/activate


python manage.py makemigrations
python manage.py migrate

dateTime=$(date +"%y.%m.%d_%H:%M")
cp db.sqlite3 noveller/migrations/db_backups/db${dateTime}.sqlite3.bckup
cp db.sqlite3 phusis/migrations/db_backups/db${dateTime}.sqlite3.bckup

# Delete db backups older than 10 days but always keep the last 10
while [ "$(find phusis/migrations/db_backups -type f -mtime +10 | wc -l)" -gt "10" ]; do find phusis/migrations/db_backups -type f -mtime +10 -exec rm {} \;; done

while [ "$(find noveller/migrations/db_backups -type f -mtime +10 | wc -l)" -gt "10" ]; do find noveller/migrations/db_backups -type f -mtime +10 -exec rm {} \;; done

cp db.sqlite3 noveller/migrations/db_backups/db${dateTime}.sqlite3
cp db.sqlite3 phusis/migrations/db_backups/db${dateTime}.sqlite3

python manage.py runserver
