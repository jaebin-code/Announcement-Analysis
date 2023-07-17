import requests
import re
from bs4 import BeautifulSoup
from konlpy.tag import Komoran

url = "https://www.skku.edu/skku/campus/skk_comm/notice01.do?mode=list&&articleLimit=10&srCategoryId1=19&article.offset=10"

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
res = requests.get(url)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")

items = soup.find_all("dl", attrs={"class":"board-list-content-wrap"})

dict={}

for item in items:
    url = "https://www.skku.edu/skku/campus/skk_comm/notice01.do"+item.find("a",attrs={"title":"자세히 보기"})["href"]
    
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    contents = soup.find("pre",attrs={"class":"pre"}).get_text()


    contents = contents.strip()  # 여러 줄 문자열의 양 끝 공백 제거
    contents = contents.replace('\n', ' ')  # 개행 문자를 공백으로 변환

    # 형태소 분석기 초기화
    komoran = Komoran()

    # 형태소 분석 수행
    pos_list = komoran.pos(contents)

    # 명사만 추출하여 출력
    nouns = [word for word, pos in pos_list if pos.startswith('N')]
    for noun in nouns:
        if noun in dict.keys():
            dict[noun]+=1
        else:
            dict[noun]=1
print(dict)
