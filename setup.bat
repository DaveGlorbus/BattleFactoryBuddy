set PYTHONPATH=%PYTHONPATH%;%cd%
py ./BattleFactoryBuddy/StaticDataGenerator.py
py -m venv .venv
.venv\Scripts\python manage.py migrate
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python manage.py collectstatic
.venv\Scripts\python manage.py runserver