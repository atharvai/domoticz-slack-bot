#!/bin/bash

if [ ! -d venv ]; then
    virtualenv venv
fi

source venv/bin/activate

pip install -r requirements.txt
python domoticz_bot.py
