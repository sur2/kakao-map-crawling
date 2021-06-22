import time
import csv

from os import times
from typing import ClassVar
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# 이벤트 호출 후 약간의 시간(ex. 클릭 이벤트 후 페이지 변경에 소비되는 시간)
tick = 0.3
# 검색어
searchWord = "울산 초밥"

driver = webdriver.Chrome(executable_path='chromedriver')
driver.get("https://map.kakao.com/")

elem = driver.find_element_by_name("q")
elem.send_keys(searchWord)
elem.send_keys(Keys.RETURN)

place_tap = driver.find_element_by_class_name("option1")
driver.execute_script("arguments[0].click();", place_tap)

time.sleep(tick)

def parse(): 
    # CSV 준비
    f = open(searchWord+'.csv', 'a', newline='')
    wr = csv.writer(f)

    global count
    places = driver.find_elements_by_css_selector("ul.placelist > li.PlaceItem")
    # print(len(places))
    for place in places:
        name = place.find_element_by_class_name("link_name")
        # print("상 호 명: " + name.text)
        category = place.find_element_by_class_name("subcategory")
        # print("카테고리: " + category.text)
        reviews = place.find_element_by_css_selector("div.rating > a.review > em")
        # print("리뷰개수: " + reviews.text)
        addr = place.find_element_by_css_selector("div.info_item > div.addr > p")
        # print("주    소: " + addr.text)
        phone = place.find_element_by_css_selector("div.info_item > div.contact > span.phone")
        # print("전화번호: " + phone.text)
        count += 1
        # CSV 작성   
        wr.writerow([count, name.text, category.text, reviews.text, addr.text, phone.text]) 
    f.close()

max_cnt = driver.find_element_by_id("info.search.place.cnt").text
print("전체개수: " + max_cnt)
# 파싱한 가게 수
count = 0

# 다음 페이지가 있는가?
page_div = driver.find_element_by_id("info.search.page")
hiddenPage = page_div.get_attribute('class').find("HIDDEN")

# 페이지가 여러 개인 경우
if(hiddenPage == -1):
    # 전체 상점을 찾을 때 까지 반복
    while(int(max_cnt) > count):
        pages = page_div.find_elements_by_css_selector("div.pageWrap > a")
        # print(len(pages))
        for page in pages:
            # 숨겨지지 않은 번호 클릭
            if(page.get_attribute('class').find('HIDDEN') == -1):
                driver.execute_script("arguments[0].click();", page)
                time.sleep(tick)
                try:
                    parse()
                except:
                    print("\n\t\t검색 결과가 없습니다.")
                time.sleep(tick)

        # 5페이지 넘기기
        next_btn = page_div.find_element_by_css_selector("div.pageWrap > button.next")
        driver.execute_script("arguments[0].click();", next_btn)
        time.sleep(tick)

# 페이지가 하나 뿐인 경우            
else:
    try:
        parse()
    except:
        print("\n\t\t검색 결과가 없습니다.")

print("total: " + str(count))

# 코드 실행 후 브라우저 종료를 희망할 경우 아래 주석을 제거
# driver.close()
