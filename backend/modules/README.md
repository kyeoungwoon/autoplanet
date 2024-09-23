### Column Names

hcs_current :
변경전차량번호, 입고지역, 입고일, 상품화시작일, 상품화종료일, 광고일

raw_hc :
차량번호, boaz환산가, boaz95, 매입보장가

---

### File Roles

getCurrentCarPrice :
selenium을 통해 Encar에서 Data Crawl, autoplanet1 계정에 판매중인 차량의
차량명, 차량가격, 차량번호를 가져옴. (화물 제외)

getSheetData :
gspread을 이용해서 A/P Dev 시트에 있는 정보들을 긁어옴
현재 시트 : raw_HC, [거래중] 상품화\_HC

TODO:

1. getCurrentCarPrice를 server file 에서 실행시키는 것
2. 상품화\_RC 가져와서 데이터 정제하기
3.
