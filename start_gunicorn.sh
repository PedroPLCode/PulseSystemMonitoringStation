#!/bin/bash
cd /home/pedro/PulseSystemMonitoringStation
source /home/pedro/PulseSystemMonitoringStation/venv/bin/activate
exec gunicorn -c /home/pedro/PulseSystemMonitoringStation/gunicorn_config.py wsgi:app