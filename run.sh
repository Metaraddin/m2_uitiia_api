#!/bin/bash

if [ "$DEBUG" = "true" ]; then
  echo 'debug mode'
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
else
  echo 'production mode'
  uvicorn app.main:app --host 0.0.0.0 --port 8000
fi
