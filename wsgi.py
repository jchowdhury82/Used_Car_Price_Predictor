## File: wsgi.py
## Author : Joyjit Chowdhury - Springboard MLE Jan2020
## Purpose: app file for wsgi endpoint. Flask app is called here.
## Note that wsgi uses "application" as the default application name to run the flask application
## "app" is the name of the flask application in app_cardata, hence imported with alias "application"

from app_cardata import app as application

if __name__ == "__main__":
    application.run()