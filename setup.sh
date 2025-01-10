#!/usr/bin/env bash

# Create python virtual environment, can fail if python3 or python3-venv are missing
python3 -m venv .venv
if [ $? -ne 0 ]; then
    exit 126
fi

# Install requirements to the virtual env
.venv/bin/pip install -r requirements.txt

# Add BattleFactoryBuddy to the Python path
export PYTHONPATH="${PYTHONPATH}:./"

# Generate required data files for calcs, & teambuilder
.venv/bin/python ./BattleFactoryBuddy/StaticDataGenerator.py

# Perform initial django migration (https://docs.djangoproject.com/en/5.1/topics/migrations/)
.venv/bin/python manage.py migrate

# Collect static files (https://docs.djangoproject.com/en/5.1/ref/contrib/staticfiles/)
# Uncommenting this will prepare the static files, as set in quickstartproject/settings.py
# this is required as part of preparation for use in production
#.venv/bin/python manage.py collectstatic