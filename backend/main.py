from modules.sync_to_db import sync_current_car_price, sync_hcs_current, sync_raw_hc
from modules.compare_min_price import compare_min_price


sync_current_car_price()
sync_hcs_current()
sync_raw_hc()

compare_min_price()