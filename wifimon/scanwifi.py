#! /usr/bin/env python
import subprocess
import re
import imp
import os
import time
import argparse
import socket
import yaml

def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', required=True, default="config.yml", help="Yaml config location")
    args = parser.parse_args()
    config = yaml.safe_load(open(args.config).read())
    return config

def get_plugins():
    plugin_folder = os.path.join(os.getcwd(), "wifimon/plugins")
    found_plugins = []
    plugins = os.listdir(plugin_folder)
    for pluginfile in plugins:
        if pluginfile in ["__init__.py", "base.py"] or pluginfile.endswith(".pyc"):
            pass
        else:
            filename = os.path.join(plugin_folder, pluginfile)
            plugin_info = imp.load_source(pluginfile.split('.')[0], filename)
            found_plugins.append({"plugin": pluginfile.split('.')[0], "info": plugin_info})
    return found_plugins

def get_waps():
    p = subprocess.check_output(['/sbin/iwlist', 'scan'], stderr=subprocess.PIPE)
    stdout_list = p.split('\n')
    found_waps = []
    line_num = 0
    for line in stdout_list:
        if "ESSID" in line:
            wap_name = line.split(':')[1].replace('"','')
            wap_data_line = stdout_list[line_num - 2]
            # Quality=44/70  Signal level=-66 dBm
            wap_data = re.match('.*=(?P<quality>\d{2}/\d{2}).*=(?P<signal>.*)\s\w+\s+', wap_data_line)
            if wap_data.groups():
                wap_quality = wap_data.group('quality')
                wap_percent = "{0:.1f}".format(float(wap_data.group('quality').split('/')[0]) /
                                        float(wap_data.group('quality').split('/')[1]) * 100)
                wap = {
                    "essid": wap_name,
                    "quality": wap_data.group('quality'),
                    "quality_percent": wap_percent,
                    "signal" : wap_data.group('signal')
                }
            found_waps.append(wap)
        line_num += 1

    cur_time = time.gmtime()
    time_conv = time.strftime("%Y-%m-%dT%H:%M:%SZ", cur_time)
    waps = []
    for found_wap in found_waps:
        data = {
            "measurement": "wapmonitor",
            "tags": {
                "host": socket.gethostname(),
                "essid": found_wap["essid"]
            },
            "fields": {
                "signal": found_wap["signal"],
                "quality": found_wap["quality"],
                "quality_percent": found_wap["quality_percent"]
            },
            "time": time_conv
        }
        waps.append(data)
    return waps


def main():
    plugins = get_plugins()
    config = get_config()
    found_waps = get_waps()
    for plugin in plugins:
        temp_plugin = plugin["info"].WifimonPlugin(config["plugins"][plugin["plugin"]])
        temp_plugin.upload_results(found_waps)

if __name__ == '__main__':
    main()