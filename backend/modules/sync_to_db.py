from pymongo import MongoClient
import json
import logging
import os
from dotenv import load_dotenv

from .getCurrentCarPrice import getCurrentPrice
from .getSheetData import hcs_current, raw_hc


MONGO_ID = os.getenv("MONGO_ID")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
URL = f"mongodb+srv://{MONGO_ID}:{MONGO_PASSWORD}@autoplanet.dmgz2.mongodb.net/?retryWrites=true&w=majority&appName=autoplanet"

JSON_PATH = "crawl data/datas"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def connect_to_mongo():
    client = MongoClient(URL)
    db = client["autoplanet"]

    return client, db

def sync_current_car_price():
    client, db = connect_to_mongo()
    data = getCurrentPrice()

    collection = db["current_car_price"]    
    for d in data:
        upsert_query = { "number" : d["number"]}
        update_result = collection.update_one(upsert_query, {"$set" : d}, upsert=True)
        logger.info(f"[CURRENT_CAR_PRICE Upsert] Modified Count {update_result.modified_count}, Matched count {update_result.matched_count}, ID : {update_result.upserted_id}")

    client.close()

def sync_hcs_current():
    client, db = connect_to_mongo()
    data = hcs_current()

    collection = db["hcs_current"]
    for d in data:
        upsert_query = { "변경전차량번호" : d["변경전차량번호"]}
        update_result = collection.update_one(upsert_query, {"$set" : d}, upsert=True)
        logger.info(f"[HCS_CURRENT Upsert] Modified Count {update_result.modified_count}, Matched count {update_result.matched_count}, ID : {update_result.upserted_id}")

    client.close()

def sync_raw_hc():
    client, db = connect_to_mongo()
    data = raw_hc()

    for d in data:
        if d["boaz95"] == "":
            try:
                d["boaz95"] = int(d['boaz환산가'] * 95 / 100)
            except Exception as e:
                logger.error(f"[ERR : {e}] FAIL TO LOAD BOAZ [HEADER : boaz95] [DATA : {d['boaz환산가']}")

    collection = db["raw_hc"]
    for d in data:
        upsert_query = { "차량번호" : d["차량번호"]}
        update_result = collection.update_one(upsert_query, {"$set" : d}, upsert=True)
        logger.info(f"[RAW_HC Upsert] Modified Count {update_result.modified_count}, Matched count {update_result.matched_count}, ID : {update_result.upserted_id}")

    client.close()


