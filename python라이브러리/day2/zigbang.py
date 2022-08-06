import requests
import pandas as pd
import geohash2

# 함수 만들기
def oneroom(addr):
    # 위도, 경도 가져옴
    url = f"https://apis.zigbang.com/v2/search?leaseYn=N&q={addr}&serviceType=원룸"
    response = requests.get(url)
    data = response.json()["items"][0]
    lat, lng = data["lat"], data["lng"]
    # 영역 구분
    geohash = geohash2.encode(lat, lng, precision=5)
    # 영역 안 매물 탐색
    url = f"https://apis.zigbang.com/v2/items?deposit_gteq=0&domain=zigbang&\
geohash={geohash}&needHasNoFiltered=true&rent_gteq=0&sales_type_in=전세|월세&service_type_eq=원룸"
    response = requests.get(url)
    # 매물아이디 리스트 만들기
    items = response.json()['items']
    ids = [item["item_id"] for item in items]
    # 매물아이디로 매물조회 요청하기
    url = "https://apis.zigbang.com/v2/items/list"
    params = {
        "domain": "zigbang",
        "withCoalition": "true",
        "item_ids": ids[:900]
    }
    response = requests.post(url, params)
    # 지정칼럼에 대해서만 리스트 만들기
    items = response.json()["items"]
    columns = ["item_id", "sales_type", "deposit", "rent", "size_m2", "address1", "manage_cost"]
    return pd.DataFrame(items)[columns]
