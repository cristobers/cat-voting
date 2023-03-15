#!/bin/sh

if [ ! -f cats.db ]; then
    python3 database.py
fi

python3 -m flask --app frontend run