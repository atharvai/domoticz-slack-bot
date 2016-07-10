# domoticz-slack-bot
Slack bot for interacting with Domoticz

## Overview
This bot is designed to retrieve data from Domoticz.

During initial development this bot will be simple as I learn about Domoticz API and also about Slack bots. There are still some things that are hardcoded that will be fixed soon.
I would appreciate any suggestions and feedback.

## Running the bot
The bot requires a configuration file that holds Bot ID & token and also Domoticz host location


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
All interactions with the bot must be after adding the bot to a channel. To interact send messages by mentioning the bot `@Domoticz: `

![demo](demo.png "sample")

## Bot ID
There is a handy script called [print_bot_id](print_bot_id.py) that will print the ID of your Slack bot. To use it, make sure you add token to it.