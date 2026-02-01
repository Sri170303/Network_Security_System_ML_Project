import os
import sys
import json
import certifi
import pymongo
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from networksecurity.logging import logger
from networksecurity.exception.exceptions import NetworkSecurityError

load_dotenv()

MONGO_DB_URI = os.getenv("MONGO_DB_URI")

ca=certifi.where()

class NetworkDataPush:
    def __init__(self):
        try:
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URI)
        except Exception as e:
            raise NetworkSecurityError(e, sys)

    def csv_to_json(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityError(e, sys)

    def push_data_to_mongo_db(self, records, database, collection):
        try:
            self.records = records
            self.database = self.mongo_client[database]
            self.collection = self.database[collection]
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityError(e, sys)
        
if __name__=="__main__":
    FILE_PATH = "../Network_Data/phisingData.csv"
    DATABASE = "NetworkDataDB"
    COLLECTION = "NetworkData"
    NetworkDataPushObj = NetworkDataPush()
    records = NetworkDataPushObj.csv_to_json(file_path=FILE_PATH)

    no_of_records = NetworkDataPushObj.push_data_to_mongo_db(records, database=DATABASE, collection=COLLECTION)
    print(no_of_records)