import sys
from influxdb import InfluxDBClient

class WifimonPlugin:
    def __init__(self, config):
        '''
        Plugin class
        :param config: dictionary from config
        '''
        # set per config, if not make defaults
        self.host = config.get("host", "localhost")
        self.port = config.get("port", 8086)
        self.user = config.get("username", "root")
        self.password = config.get("password", "root")
        self.database = config.get("database")
        self.ssl = config.get("ssl", False)
        self.verify_ssl = config.get("verify_ssl", False)
        self.timeout = config.get("timeout")
        self.use_udp = config.get("use_udp", False)
        self.udp_port = config.get("udp_port", 4444)
        self.proxies = config.get("proxies")

        try:
            self.client = InfluxDBClient(self.host,
                                         self.port,
                                         self.user,
                                         self.password,
                                         self.database,
                                         self.ssl,
                                         self.verify_ssl,
                                         self.timeout,
                                         self.use_udp,
                                         self.udp_port,
                                         self.proxies)
        except Exception as e:
            sys.stderr.write("Error creating InfluxDB client\n")
            sys.stderr.write(e.message)

    def upload_results(self, data):
        '''
        Method to use data from wifimon
        :param data: List of data
        :return: boolean of success, not implemented
        '''
        try:
            self.client.write_points(data)
        except Exception as e:
            sys.stderr.write("Error uploading data to InfluxDB\n")
            sys.stderr.write(e.message)
            return False

        return True
