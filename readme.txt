# Goal: Small python web app utilizing modern web dev features such as MVC, ORM, 
# routes, templates, sessions, flash messages and migrations while introducing tensorflow for ML.
# Usage: Created for use in rapid prototyping by dev team in MTSU Hackathon 2019
# Requires Python 3.6.8 (64 bit), Flask 1.0

# Useful commands before running app

pip install Flask flask_sqlalchemy Flask-Migrate tensorflow

#On Windows
set FLASK_APP=run.py
set FLASK_ENV=development

#On Linux/Mac
export FLASK_APP=run.py
export FLASK_ENV=development

flask db init 		#Sets up migration environment
flask db migrate	#Creates migrations to sync models & db
flask db upgrade	#Runs the migrations to apply an un-run migrations (after git checkout, etc)

flask run