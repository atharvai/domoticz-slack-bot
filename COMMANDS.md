# Commands

The commands are split in two parts, a command group and command itself. The interaction is as follows:
`@domoticz: <command-group> <command/keyword>`

The command group defines the type of information to pull such as `status`, `temp` etc. The command is either a command keyword or a device name. 
This will be illustrated for each command group and command below.

# <a name='cgStatus'></a>Status

This returns cards for each device matching the keyword. These commands mirror the Domoticz [Get All Devices of type](https://www.domoticz.com/wiki/Domoticz_API/JSON_URL%27s#Get_all_devices_of_a_certain_type) API.

## Command Group: `status`

#### Commands

| Command | Example | Description |
|---------|---------|-------------|
| all | `status all` | Return status of all devices that are used |
| temp | `status temp` |  Return status of devices of type Temp (temperature) that are used |
| light| `status light` |  Return status of devices of type light (Light and Switches) that are used |
| weather | `status weather` |  Return status of devices of type Weather that are used |
| utility | `status utility` |  Return status of devices of type Utility that are used |
| \<device name\> | `status thermostat` |  Return status reported by first matching device. Name is partially matched and is case insensitive |

# Devices

These commands report back the status or data reported by a device. The command is usually partial or full name of the device.

## Command Group: `device`

#### Commands

| Command | Example | Description |
|---------|---------|-------------|
| list | `device list` | Returns a list of all used devices in alphabetical order |
| \<name\> (on\|off) | `device light1 on`, `device switch2 off` | Turn light/switch device On/Off. for dimmable lights/switched see `dim` command. Setting values for other types of devices is not yet implemented |
| dim \<name\> <level> | `device dim light2 4`, `device dim light3 100` | Set dim level for light/switch. Level should be between `1` and `16`. Not yet functional|
| toggle \<name\> | `device toggle switch3` | Toggles on/off a light/switch. |
| status \<name\> | `device status switch3` | Returns status of device. Same as the [Status command group](#cgStatus) | 

Device names containing spaces must be enclosed in single or double quotes. E.g. `'virtual switch'` or `"virtual switch"`.

# Sunrise & Sunset

This consists of one command only which returns the Sunrise and Sunset times in UTC. This maps directly to Domoticz's [SunRiseSet API](https://www.domoticz.com/wiki/Domoticz_API/JSON_URL%27s#Get_sunrise_and_sunset_times)

## Command Group: `sunriseset`

#### Commands

| Command | Example | Description |
|---------|---------|-------------|
| sunriseset | `sunriseset` | Returns the Sunrise and Sunset times in 24hr and UTC |

# User Variables

This consists of three commands to set, get and delete user variables. 

## Commad Group: `uservar`

#### Commands

| Command | Example | Description |
|---------|---------|-------------|
| get (all\|\<idx\>\|\<name\>) | `uservar get all`, `uservar get 1`, `uservar get myvar` | Returns either list of all user variables or value of requested variable. Can request using IDX or variable name (case insensitive) |
| set \<type\> \<name\> \<value\> | `uservar set int var_int 1` | Creates or updates variable called `name` with `value` as `type`. `type` can be one of the following:<ul><li>int / integer</li><li>float</li><li>str / string</li><li>date</li><li>time</li> </ul> Strings can only be single word values |
| delete (\<idx\>\|\<name\>) | `uservar delete 1`, `uservar delete var_int` | Deletes user variable by name or IDX |
