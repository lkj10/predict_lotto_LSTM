import pandas as pd
import requests
from bs4 import BeautifulSoup

# 마지막 회차를 얻기 위한 주소
main_url = "https://www.dhlottery.co.kr/gameResult.do?method=byWin"

# 임의의 회차를 얻기 위한 주소
basic_url = "https://www.dhlottery.co.kr/gameResult.do?method=byWin&drwNo="

# 마지막 회차 번호 가져오는 함수


def get_last_num():
    num_list = []
    request = requests.get(main_url)
    soup = BeautifulSoup(request.text, 'html.parser')
    num = soup.find("h4").text
    for i in num:
        try:
            if(int(i)):
                num_list.append(i)
        except:
            pass
    lotto_num = ''.join(num_list)
    return int(lotto_num)

# 특정회차 로또 번호 알려주는 함수


def get_ball_num(num):
    url = f"{basic_url}{num}"
    balls_list = []
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    balls = soup.find_all("span", {"class": "ball_645"})
    if balls:
        for ball in balls:
            balls_list.append(int(ball.string))
    return balls_list
