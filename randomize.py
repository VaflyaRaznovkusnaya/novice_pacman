'''
Модуль-генератор под названием: randomize.py
Цель данного модуля: Генерация готовых ситуаций и их решений или иначе прецидентов для нейронной сети модуля neural.py
Функция make_up_stuff является главной и на данный момент единственной функцией, на выходе она выдаёт:
начальные координаты врага, игрока, а так же три переменные, составленные по подобию сигмоиды, однозначно описывающие решение.
Функция генерирует 4 значения координат, а потом на их основе составляет решение.
'''

import random

def make_up_stuff():
    pack_x, pack_y = random.randint(-20, 20) , random.randint(-20, 20)
    enem_x, enem_y = random.randint(-20, 20) , random.randint(-20, 20)

    dx = pack_x - enem_x
    dy = pack_y - enem_y

    if abs(dx) == abs(dy):
        should_go = 0 # стоим на месте
        dir_as = 0.5 #чтоб было
        dit_way = 0.5 # чтоб было
    elif abs(dx) < abs(dy):
        should_go = 1 # идём куда-то
        dir_as = 0  # пойдём по х
        if dx < 0:
            dit_way = 0 # идём влево <-
        else:
            dit_way = 1 # идём вправо ->
    else:
        should_go = 1  # идём куда-то
        dir_as = 1  # пойдём по y
        if dy < 0:
            dit_way = 0 # идём вниз V
        else:
            dit_way = 1 # идём вверх ^

    return (pack_x, pack_y, enem_x, enem_y, should_go, dir_as, dit_way)# Write your code here :-)

#neural_network = NeuralNetwork()
#neural_network.train(10000)
#from neural import NeuralNetwork
#import randomize
