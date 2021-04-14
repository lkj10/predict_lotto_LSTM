import numpy as np

#로또 리스트 원핫코딩으로 바꾸는 함수
def numbers2ohbin(numbers):
    ohbin = np.zeros(45)
    for i in range(7):
        ohbin[int(numbers[i])-1] = 1
    return ohbin

#원핫코딩한거 다시 로또 리스트로 바꾸는 함수
def ohbin2numbers(ohbin):
    numbers = []
    for i in range(len(ohbin)):
        if ohbin[i] == 1.0:
            numbers.append(i+1)
    return numbers
