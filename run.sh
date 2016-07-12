#!/bin/bash

virtualenv venv
source venv/bin/activate

pip install -r requirements.txt
python domoticz_bot.py
