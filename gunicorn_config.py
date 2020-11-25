## File: gunicorn_config.py
## Author : Joyjit Chowdhury - Springboard MLE Jan2020
## Purpose: configuration file for the gunicorn web server
## configure web server with 2 workers, 2 threads and 120 seconds of process timeout
## bind to ip 0.0.0.0 (local) at port 5000
bind = "0.0.0.0:5000"
workers = 2
threads = 2
timeout = 120
