import sys
from pymongo import MongoClient

class WifimonPlugin:
    def __init__(self, config):

        self.database = ""
        if "database" in config:
            self.database = config.get("database")
        else:
            sys.stderr.write("MongoDB requires database in config\n")

        self.collection = ""
        if "collection" in config:
            self.collection = config.get("collection")
        else:
            self.collection = self.database

        # can use either full uri, or specify host/port
        self.client = ""
        if "uri" in config:
            self.client = MongoClient(config["uri"])
        else:
            self.host = config.get("host", "localhost")
            self.port = config.get("port", 27017)
            self.client = MongoClient(config["host"], config["port"])


    def upload_results(self, data):

        db = self.client[self.database]
        collect = db[self.collection]
        if len(data) == 0:
            pass
        if len(data) == 1:
            try:
                collect.insert_one(data[0])
            except Exception as e:
                sys.stderr.write("Error uploading MongoDB data\n")
                sys.stderr.write(e.message)
        else:
            try:
                collect.insert_many(data)
            except Exception as e:
                sys.stderr.write("Error uploading multiple MongoDB data\n")
                sys.stderr.write(e.message)

        return True
