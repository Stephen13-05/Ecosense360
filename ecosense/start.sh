#!/bin/bash
gunicorn ecosense.wsgi --bind 0.0.0.0:$PORT
