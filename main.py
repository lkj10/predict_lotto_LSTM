import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import os

# 마지막 회차를 얻기 위한 주소
main_url = "https://www.dhlottery.co.kr/gameResult.do?method=byWin" 

# 임의의 회차를 얻기 위한 주소
basic_url = "https://www.dhlottery.co.kr/gameResult.do?method=byWin&drwNo=" 

#마지막 회차 번호 가져오는 함수
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

#특정회차 로또 번호 알려주는 함수
def get_ball_num(num) :
    url = f"{basic_url}{num}"
    balls_list = []
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    balls = soup.find_all("span", {"class" : "ball_645"})
    if balls:
        for ball in balls :
            balls_list.append(int(ball.string))
    return balls_list

#회차랑 로또 번호 합쳐서 딕셔너리로 만드는 함수
def make_dic(num): 
    dic = {}
    for i in range(1, num + 1):
        dic[f"{i}"] = get_ball_num(i)
    return dic

#csv 파일로 변환해주는 함수
def save_to_file(dic):
    file = open("lotto.csv", mode="w", encoding='utf-8', newline='')
    writer = csv.writer(file)
    writer.writerow(["times", "num1", "num2", "num3", "num4", "num5", "num6", "bonus"])
    for key, val in dic.items():
        temp = [key] + val
        writer.writerow(list(temp))

save_to_file(make_dic(9))
    
