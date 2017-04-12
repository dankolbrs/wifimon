# Wifimon

Script to review available Wireless Access Points and report with signal and quality. Really just a wrapper around iwlist.

I wanted to monitor WAP availability for one that is a bit flakey, figured I'd overcomplicate it.

## Installation

* `git clone https://github.com/dankolbrs/wifimon.git`
* `cd wifimon`
* `python setup.py install`

## Running
`wifimon --config /path/to/config.yaml`

## Plugins

Admittedly not the best plugin interface around. To create a plugin:
* Create a python file in the `wifimon/plugins` directory
* Define the `WifimonPlugin` class
  * `WifimonPlugin.__init__` called on class creation
  * `WifimonPlugin.upload_results` gets a list of data from script

## TODO
* Add tests
* Utilize lib directory rather than scanwifi.py
* Python3
* Logger
* Utilize return from plugin `upload_results` function