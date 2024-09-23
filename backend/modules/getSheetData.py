import gspread
import json
from datetime import datetime
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

JSON_PATH = "modules/datas"
CREDENTIAL_PATH = "modules/credentials"

CREDENTIAL_FILE = CREDENTIAL_PATH + "/autoplanet-dev-f71e3776ac0d.json"

gc = gspread.service_account(filename=CREDENTIAL_FILE)

SHEET_NAMES = {
    "raw_hc" : "raw_HC",
    "raw_rc" : "raw_RC",
    "hcs_current" : "[거래중]상품화_HC",
    "rc_current" : "[거래중]상품화_RC",
    "hcs_closed" : "[마감완료]상품화_HC",
    "rc_closed" : "[마감완료]상품화_RC",
    "yongin" : "import_용인(상품화)",
    "yangsan" : "import_양산(상품화)"
}

SHEET_URLS = {
    "ap_dev" : "https://docs.google.com/spreadsheets/d/1nRLtjIrqYhqtgk-yE0-qcYYSZ6UipHulDeWZQqpsXEs/",

}

ap_dev = gc.open_by_url(SHEET_URLS["ap_dev"])

def hcs_current():
    HCS_CURRENT_HEADERS = [
                            "차수",
                            "차량명",
                            "변경전차량번호",
                            "변경후차량번호",
                            "입고지역",
                            "입고일",
                            "상품화시작일",
                            "상품화종료일",
                            "강서탁송일",
                            "풍동탁송일",
                            "판매지역",
                            "광고일",
                            "판매일",
                            "매입일",
                            "반납일",
                            "판매채널",
                            "비고",
                            "판매가",
                            "수리비총액",
                            "판금도색내역",
                            "판금도색비용",
                            "광택내역",
                            "광택비용",
                            "세차내역",
                            "세차비용",
                            "덴트내역",
                            "덴트비용",
                            "타이어내역",
                            "타이어비용",
                            "휠복원내역",
                            "휠복원비용",
                            "실내복원내역",
                            "실내복원비용",
                            "유리복원내역",
                            "유리복원비용",
                            "썬팅내역",
                            "썬팅비용",
                            "정비내역",
                            "정비비용",
                            "유류비내역",
                            "유류비비용",
                            "풍동비용",
                            "용인비용",
                            "비고",
                            "판매가",
                            "공급가액",
                            "세액",
                            "판매세금계산서발급일",
                            "매도비",
                            "공급가액",
                            "세액",
                            "매도비세금계산서발급일",
                            "매입가",
                            "공급가액",
                            "세액",
                            "매입세금계산서발급일",
                            "이전비없이고객바로명의이전",
                            "비고1매입가판매가차액",
                            "비고2",
                            "비고3",
                            "비고4",
                            "비고5"
                        ]

    hcs_current = ap_dev.worksheet(SHEET_NAMES["hcs_current"]).get_all_values()
    hcs_current = hcs_current[3:]

    to_db = []
    to_datetime = [
                "입고일",
                "상품화시작일",
                "상품화종료일",
                "강서탁송일",
                "풍동탁송일",
                "광고일",
                "판매일",
                "매입일",
                "반납일",
                "판매세금계산서발급일",
                "매도비세금계산서발급일",
                "매입세금계산서발급일"
            ]
    to_int = [
                "판매가",
                "수리비총액",
                "판금도색비용",
                "광택비용",
                "세차비용",
                "덴트비용",
                "타이어비용",
                "휠복원비용",
                "실내복원비용",
                "유리복원비용",
                "썬팅비용",
                "정비비용",
                "유류비비용",
                "풍동비용",
                "용인비용",
                "판매가",
                "공급가액",
                "세액",
                "매도비",
                "공급가액",
                "세액",
                "매입가",
                "공급가액",
                "세액"
            ]


    for hcs_data in hcs_current:
        if hcs_data[0] == "":
            break

        temp = {}
        # 오류 발생 시 int, datetime 변환하는 header에 data가 이상한게 들어있지는 않은지 참고 필요
        for header, data in zip(HCS_CURRENT_HEADERS, hcs_data):
            try: # ToDo : 예외처리는 해두었음
                if header in to_datetime:
                    date_format = "%Y-%m-%d" # datetime 객체로 변환하면 알아서 잘 들어간대
                    data = datetime.strptime(data, date_format).isoformat()
                elif header in to_int:
                    data = data.replace(",", "") # 1,000 형식으로 되있는거 변환
                    data = int(data)
            except Exception as e:
                logger.error(f"[ERR : {e}] [HEADER : {header}] [DATA : {data}]")
            temp[header] = data
        to_db.append(temp)

    return to_db


def raw_hc():
    RAW_HC_HEADERS = [
                    "차수",
                    "접수일",
                    "선정일",
                    "차수구분",
                    "차량번호",
                    "제조사",
                    "대표차종",
                    "차종등급",
                    "옵션",
                    "차량상태",
                    "연료",
                    "차량색상",
                    "최초등록일",
                    "경과개월",
                    "신차가",
                    "평가주행거리",
                    "재고위치",
                    "외관",
                    "단순",
                    "골격",
                    "내비",
                    "선루프",
                    "차대번호",
                    "연식",
                    "추가옵션가격",
                    "평균판매기간",
                    "판매등록율",
                    "단기판매율",
                    "장기재고율",
                    "문의소요일",
                    "boaz환산가",
                    "boaz95",
                    "boaz93",
                    "마진율",
                    "적정매입가",
                    "최종예상소매가",
                    "blank",
                    "엔카판매예상가",
                    "매입보장가",
                    "광고확정가",
                    "확정매입가",
                    "비고미선정사유",
                    "광고가변경1",
                    "광고가변경1변경일",
                    "광고가변경2",
                    "광고가변경2변경일",
                    "광고가변경3",
                    "광고가변경3변경일"
                ]
    
    raw_hc = ap_dev.worksheet(SHEET_NAMES["raw_hc"]).get_all_values()
    raw_hc = raw_hc[2:]
    
    to_db = []

    to_datetime = [
                    "접수일",
                    "선정일"
                ]
    to_int = [
                "boaz환산가",
                "boaz95",
                "boaz93",
                "매입보장가",
            ]
    blank_limit = 1
    for raw_hc_data in raw_hc:
        if raw_hc_data[0] == "":
            if blank_limit == 0:
                break
            blank_limit -= 1

        temp = {}
        for header, data in zip(RAW_HC_HEADERS, raw_hc_data[:48]): # header를 48개만 가져왔음, 변경시 수정 필요
            try: # ToDo : 예외처리는 해두었음
                if header in to_datetime:
                    date_format = "%Y-%m-%d" # datetime 객체로 변환하면 알아서 잘 들어간대
                    data = datetime.strptime(data, date_format).isoformat()
                elif header in to_int:
                    data = data.replace(",", "") # 1,000 형식으로 되있는거 변환
                    data = int(data)
            except Exception as e:
                logger.error(f"[ERR : {e}] [HEADER : {header}] [DATA : {data}]")
            temp[header] = data
        to_db.append(temp)
    
    return to_db