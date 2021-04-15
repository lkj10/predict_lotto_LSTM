from get_num import get_last_num, get_ball_num
from save_to_csv import save_to_file
from num_to_ohcoding import numbers2ohbin, ohbin2numbers
import csv
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import models
import numpy as np

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


x_samples = List[0:get_last_num()-1]
y_samples = List[1:get_last_num()]

# 훈련셋: (1회 입력, 2회 출력)부터 (700회 입력, 701회)까지 700개 샘플
# 검증셋: (701회, 702회)부터 (800회, 801회)까지 100개 샘플
# 시험셋: (801회, 802회)부터 (893회, 894회)까지 93개 샘플

train_idx = (0, 800)
val_idx = (800, 900)
test_idx = (900, len(List))

print("train: {0}, val: {1}, test: {2}".format(train_idx, val_idx, test_idx))


# 모델을 정의합니다.
model = keras.Sequential([
    keras.layers.LSTM(128, batch_input_shape=(1, 1, 45),
                      return_sequences=False, stateful=True),
    keras.layers.Dense(45, activation='sigmoid')
])

# 모델을 컴파일합니다.
model.compile(loss='binary_crossentropy',
              optimizer='adam', metrics=['accuracy'])

# 매 에포크마다 훈련과 검증의 손실 및 정확도를 기록하기 위한 변수
train_loss = []
train_acc = []
val_loss = []
val_acc = []

# 최대 100번 에포크까지 수행
for epoch in range(100):

    model.reset_states()  # 중요! 매 에포크마다 1회부터 다시 훈련하므로 상태 초기화 필요

    batch_train_loss = []
    batch_train_acc = []

    for i in range(train_idx[0], train_idx[1]):

        xs = x_samples[i].reshape(1, 1, 45)
        ys = y_samples[i].reshape(1, 45)

        loss, acc = model.train_on_batch(xs, ys)  # 배치만큼 모델에 학습시킴

        batch_train_loss.append(loss)
        batch_train_acc.append(acc)

    train_loss.append(np.mean(batch_train_loss))
    train_acc.append(np.mean(batch_train_acc))

    batch_val_loss = []
    batch_val_acc = []

    for i in range(val_idx[0], val_idx[1]):
        xs = x_samples[i].reshape(1, 1, 45)
        ys = y_samples[i].reshape(1, 45)

        loss, acc = model.test_on_batch(xs, ys)  # 배치만큼 모델에 입력하여 나온 답을 정답과 비교함

        batch_val_loss.append(loss)
        batch_val_acc.append(acc)

    val_loss.append(np.mean(batch_val_loss))
    val_acc.append(np.mean(batch_val_acc))

    print('epoch {0:4d} train acc {1:0.3f} loss {2:0.3f} val acc {3:0.3f} loss {4:0.3f}'.format(
        epoch, np.mean(batch_train_acc), np.mean(batch_train_loss), np.mean(batch_val_acc), np.mean(batch_val_loss)))

    model.save('model_{0:04d}.h5'.format(epoch+1))


print('receive numbers')
xs = x_samples[-1].reshape(1, 1, 45)
ys_pred = model.predict_on_batch(xs)
list_numbers = []

for n in range(10):
    numbers = gen_numbers_from_probability(ys_pred[0])
    print('{0} : {1}'.format(n, numbers))
    list_numbers.append(numbers)
