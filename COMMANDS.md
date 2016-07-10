# Commands

The commands are split in two parts, a command group and command itself. The interaction is as follows:
`@domoticz: <command-group> <command/keyword>`

The command group defines the type of information to pull such as `status`, `temp` etc. The command is either a command keyword or a device name. 
This will be illustrated for each command group and command below.

# Status

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

# Devices

These commands report back the status or data reported by a device. The command is usually partial or full name of the device.

## Command Group: `device`

These commands usually report metadata about devices rather than any readings.

#### Commands

| Command | Example | Description |
|---------|---------|-------------|
| list | `device list` | Returns a list of all used devices in alphabetical order |


## Command Group: `temp`

Specifically for temperature devices

#### Commands

| Command | Example | Description |
|---------|---------|-------------|
| all | `temp all` | Return Temperature reported by all devices |
| <blank> | `temp` | Same as `all` Return Temperature reported by all devices |
| \<device name\> | `temp thermostat` |  Return temperature reported by first matching device. Name is matched anywhere and is case insensitive |

