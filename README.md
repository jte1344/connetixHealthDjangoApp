Run server:

cd into DjangoApp

python manage.py runserver

update models in database:

python manage.py makemigrations index

--if you get an error like: cannot find module: lxml

run pip install lxml    <- or which ever module it cannot find
