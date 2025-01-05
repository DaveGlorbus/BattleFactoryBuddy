set PYTHONPATH=%PYTHONPATH%;%cd%
py ./BattleFactoryBuddy/StaticDataGenerator.py
py -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python manage.py runserver