# domoticz-slack-bot
Slack bot for interacting with Domoticz

## Overview
This bot is designed to retrieve data from Domoticz.

During initial development this bot will be simple as I learn about Domoticz API and also about Slack bots. There are still some things that are hardcoded that will be fixed soon.
I would appreciate any suggestions and feedback.

## Running the bot
The bot requires a configuration file that holds Bot ID & token and also Domoticz host location. 

1. Clone the repository
`git clone git@github.com:atharvai/domoticz-slack-bot.git --depth 1`
2. Change directory
`cd domoticz-slack-bot`
3. Execute: Shell script OR Supervisor
  a. shell script
    `./run.sh`
  b. Supervisor
    1. Create virtualenv
    
    ```bash
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
    
    2. Setup Supervisor config
    
    ```
    [program:domoticz_slack_bot]
    command=/home/pi/Documents/domoticz-slack-bot/venv/bin/python domoticz_bot.py
    directory=/home/pi/Documents/domoticz-slack-bot/
    startsecs=30
    redirect_stderr=true
    stdout_logfile=/var/log/domoticz_slack_bot.log
    stdout_logfile_maxbytes=10MB
    stdout_logfile_backups=2
    numprocs=1
    ```
    
    3. Start Supervisor
      `sudo supervisord`

### Configuration
Configuration file should be named `bot.config` and reside in the same directory as the bot script.

A sample configuration file is provided in the root of this repository called [bot.config.example](bot.config.example)

```yaml
[slack]
bot_id = XXXXXXXX
token = xoxb-123456789-Ex4Mp13

[domoticz]
url = mydomoticz
```

### Interactions
All interactions with the bot must be after adding the bot to a channel. To interact send messages by mentioning the bot `@domoticz: `

![demo](demo.png "sample")

## Bot ID
There is a handy script called [print_bot_id](print_bot_id.py) that will print the ID of your Slack bot. To use it, make sure you add token to it.