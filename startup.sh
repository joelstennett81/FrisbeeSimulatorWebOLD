#!/bin/bash
python manage.py collectstatic && gunicorn --workers 2 frisbee_simulator_web.wsgi