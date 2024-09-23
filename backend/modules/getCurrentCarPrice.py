from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from dotenv import load_dotenv
import os
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()
ID = os.getenv("ENCAR_HCS_ID")
PASSWORD = os.getenv("ENCAR_HCS_PASSWORD")

def getCurrentPrice():
    # WebDriver 초기화
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # 페이지 로드 대기
    driver.implicitly_wait(10)

    RESULT_PATH = "modules/datas"

    URL = "https://fem.encar.com/encar-login"
    driver.get(URL)


    # 로그인
    id_field = driver.find_element(By.XPATH, '//*[@id="id"]')
    id_field.send_keys(ID)  # ID를 적절한 값으로 대체

    pw_field = driver.find_element(By.XPATH, '//*[@id="password"]')
    pw_field.send_keys(PASSWORD)  # PASSWORD를 적절한 값으로 대체

    login_button = driver.find_element(By.XPATH, '//*[@id="wrap"]/div/div[2]/div/div/form/div/button')
    login_button.click()

    # 로그인 후 대기
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrapLogin"]/ul[2]/li[1]/a'))).click()

    # 리스트뷰 설정
    listview_dropdown = Select(driver.find_element(By.XPATH, '//*[@id="pagerow"]'))
    listview_dropdown.select_by_value('50')

    # 페이지네이션 요소 찾기

    results = []

    # ToDO : 캡챠가 뜨면, source를 찾을 수 없으므로 error handling이 필요함.

    # 페이지 로드 후 요소 대기
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="adCarSearch"]')))

    car_numbers = driver.find_elements(By.XPATH, '//*[@id="adCarSearch"]/div[2]/ul/li/div[2]/div[1]/div/ul/li[1]/span')
    car_prices = driver.find_elements(By.XPATH, '//*[@id="adCarSearch"]/div[2]/ul/li/div[2]/div[1]/div/span[2]/dl/dd/strong')

    car_names = []
    car_info_elements = driver.find_elements(By.CSS_SELECTOR, 'a.carinf_title')
    for car_info_element in car_info_elements:
        brand_model = car_info_element.find_element(By.CSS_SELECTOR, 'span.cls').text
        details = car_info_element.find_element(By.CSS_SELECTOR, 'span.dtl').text
        car_names.append(f"{brand_model} {details}")

    for name, num, price in zip(car_names, car_numbers, car_prices):
        price = price.text
        price = int(price.replace(",", ""))
        results.append({
        "model" : name,
        "number" : num.text,
        "price" : price
        }
    )

    current_selected_element = driver.find_element(By.CSS_SELECTOR, "a.nom.on")

    while True:
        try:
            # 다음 요소 찾기 (다음 형제 노드)
            next_element = current_selected_element.find_element(By.XPATH, "following-sibling::a")
            next_element.click()

            car_numbers = driver.find_elements(By.XPATH, '//*[@id="adCarSearch"]/div[2]/ul/li/div[2]/div[1]/div/ul/li[1]/span')
            car_prices = driver.find_elements(By.XPATH, '//*[@id="adCarSearch"]/div[2]/ul/li/div[2]/div[1]/div/span[2]/dl/dd/strong')

            car_names = []
            car_info_elements = driver.find_elements(By.CSS_SELECTOR, 'a.carinf_title')
            for car_info_element in car_info_elements:
                brand_model = car_info_element.find_element(By.CSS_SELECTOR, 'span.cls').text
                details = car_info_element.find_element(By.CSS_SELECTOR, 'span.dtl').text
                car_names.append(f"{brand_model} {details}")

            for name, num, price in zip(car_names, car_numbers, car_prices):
                price = price.text
                price = int(price.replace(",", ""))
                results.append({
                            "model" : name,
                            "number" : num.text,
                            "price" : price
                        }
                )

        except NoSuchElementException:
            logger.info("다음 요소가 없습니다.")
            break
            
        except StaleElementReferenceException:
            logger.warning("StaleElementReferenceException Occured.")
            break
        
        except Exception as e:
            logger.error(f"Exception Occured: {e}")
            break


    return results

