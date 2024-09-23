from pymongo import MongoClient
import json
import logging
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_ID = os.getenv("MONGO_ID")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_ATLAS_URL = os.getenv("MONGO_ATLAS_URL")
URL = f"mongodb+srv://{MONGO_ID}:{MONGO_PASSWORD}@{MONGO_ATLAS_URL}"

LOGS_PATH = "modules/logs"

def setup_loggers():
    # 로거 생성
    low_logger = logging.getLogger("LOW_PRICE")
    high_logger = logging.getLogger("HIGH_PRICE")
    debug_logger = logging.getLogger("DEBUGGER")

    low_logger.setLevel(logging.INFO)
    high_logger.setLevel(logging.INFO)
    debug_logger.setLevel(logging.DEBUG)

    # 핸들러 설정
    lowSellPrice = logging.FileHandler(LOGS_PATH+"low_sell_price.log")
    highSellPrice = logging.FileHandler(LOGS_PATH+"high_sell_price.log")
    debugHandler = logging.FileHandler(LOGS_PATH+"debug.log")

    # 포매터 설정
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')

    # 각 핸들러에 포매터 추가
    lowSellPrice.setFormatter(formatter)
    highSellPrice.setFormatter(formatter)
    debugHandler.setFormatter(formatter)

    # 로거에 핸들러 추가
    low_logger.addHandler(lowSellPrice)
    high_logger.addHandler(highSellPrice)
    debug_logger.addHandler(debugHandler)

    return low_logger, high_logger, debug_logger

low_logger, high_logger, debug_logger = setup_loggers()

def connect_to_mongo():
    client = MongoClient(URL)
    db = client["autoplanet"]

    return db

def compare_min_price():
    db = connect_to_mongo()
    raw_hc = db["raw_hc"]
    current_car_price = db["current_car_price"].find()
    compare_result = db["compare_result"]

    for current_data in current_car_price:
        current_data_number = current_data['number']
        try:
            raw_hc_data = raw_hc.find({"차량번호": current_data_number})[0]
        except Exception as e:
            debug_logger.warning(f"[ERR : {e}] 차량번호 : {current_data_number} cannot find query")
            continue
        current_data_price = current_data['price'] * 10000  # 만원 생략됨
        raw_hc_data_boaz95 = raw_hc_data['boaz95']          # 판매가격
        raw_hc_data_min_price = raw_hc_data['매입보장가']   # 최소소매가 

        # print(list(map(type, [current_data_price, raw_hc_data_boaz95, raw_hc_data_min_price])))
        insert_data = []
        try:
            if current_data_price < raw_hc_data_min_price: # 최소소매가 깨짐
                insert_data.append({"차량번호" : current_data_number, "최소소매가" : raw_hc_data_min_price, "판매가격" : current_data_price})
                low_logger.info(f"차량번호 : {current_data_number} 최소소매가 오류,"\
                                    + f"최소소매가 : {raw_hc_data_boaz95/10000} 판매가격 : {current_data_price/10000} ")
            
            elif current_data_price > raw_hc_data_boaz95: # 보아즈보다 가격 높음
                high_logger.info(f"판매가격 > 보아즈 | 차량번호 : {current_data_number}"\
                    + f"최소소매가 : {raw_hc_data_boaz95/10000} 판매가격 : {current_data_price/10000}")

            else: # 정상
                debug_logger.debug(f"차량번호 : {current_data_number} 최소소매가 : {raw_hc_data_min_price/10000} 판매가격 : {current_data_price/10000}")

        except Exception as e:
            debug_logger.warning(f"[ERR : {e}] 차량번호 : {current_data_number}")
            continue

    if insert_data: # 데이터가 있을 때만 insert
        compare_result.delete_many({})
        compare_result.insert_many(insert_data)
        debug_logger.warning(f"Inserted {len(insert_data)} data")
    else:
        debug_logger.warning("No data to insert")
