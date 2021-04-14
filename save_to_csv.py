import csv

#csv 파일로 변환해주는 함수
def save_to_file(dic):
    file = open("lotto.csv", mode="w", encoding='utf-8', newline='')
    writer = csv.writer(file)
    writer.writerow(["times", "num1", "num2", "num3", "num4", "num5", "num6", "bonus"])
    for key, val in dic.items():
        temp = [key] + val
        writer.writerow(list(temp))
    return