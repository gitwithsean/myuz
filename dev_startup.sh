
. venv/myuz/bin/activate
dateTime=$(date +"%y.%m.%d_%H:%M")
python manage.py makemigrations
python manage.py migrate
cp db.sqlite3 noveller/projects/living_and_the_son_of_death/db_backups/db${dateTime}.sqlite3
python manage.py runserver
