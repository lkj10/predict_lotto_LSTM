from get_num import get_last_num, get_ball_num
from save_to_csv import save_to_file
from num_to_ohcoding import numbers2ohbin, ohbin2numbers
import csv

# 회차랑 로또 번호 합쳐서 딕셔너리로 만드는 함수


def make_dic(num):
    dic = {}
    for i in range(1, num+1):
        dic[f"{i}"] = get_ball_num(i)
    return dic


# save_to_file(make_dic(get_last_num()))

# print(numbers2ohbin(get_ball_num(get_last_num())))


# 원핫코딩으로 변환 후 List에 저장
file = open("lotto.csv", mode="r", encoding='utf-8')
dr = csv.reader(file)
List = []
for i in dr:
    del i[0]  # 회차 수 제거
    try:
        List.append(numbers2ohbin(i))
    except:
        pass
# print(List)
print(123)
