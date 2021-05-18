import numpy
import randomize

#training_set_inputs = numpy.array([[3, 0, 2], [0, 4, 4], [5, 4, 4], [4, 8, 2]])

class NeuralNetwork():
    def __init__(self):
        #random.seed(1)
        # We model a single neuron, with 3 input connections and 1 output connection.
        # We assign random weights to a 3 x 1 matrix, with values in the range -1 to 1
        # and mean 0.
        self.synaptic_weights = 2 * numpy.random.random((4, 1)) - 1 #!!!

    # нормализация от 0 до 1
    def __sigmoid(self, x):
        return 1 / (1 + numpy.exp(-x))

    # производная
    def __sigmoid_derivative(self, x):
        return x * (1 - x)

    # Тренируем и подправляем
    def train(self, number_of_training_iterations):
        for i in range(number_of_training_iterations):

            training_array_output = []
            training_array_input = list(randomize.make_up_stuff())
            for j in range (3):
                training_array_output.append(training_array_input.pop())
            training_array_output.reverse() # получаем массив координат и массив ответов

            # прокидываем в предсказание
            output = list(self.think(training_array_input[0],training_array_input[1],training_array_input[2],training_array_input[3]))

            error = 0
            for j in range (3):
                error += training_array_output[j] - output[j]
            error = error/3

            help_pls = (self.__sigmoid_derivative(output[0]+ output[1]+ output[2]))/3

            for j in range(4):
                training_array_input[j] = numpy.dot(training_array_input[j], error * help_pls)
                self.synaptic_weights[j] += training_array_input[j]

    # Послетренировочное
    def think(self, pack_x, pack_y, enemy_x, enemy_y):
        # Pass inputs through our neural network (our single neuron).
        dx = pack_x * self.synaptic_weights[0] - enemy_x * self.synaptic_weights[2]
        dx = self.__sigmoid(dx)
        dy = pack_y * self.synaptic_weights[1] - enemy_y * self.synaptic_weights[3]
        dy = self.__sigmoid(dy)

        if dx == dy:
            if_go = 0 # идём куда-то
            i_go_here = 0.5
            i_go_where = 0.5
            dx = 0.5
            dy = 0.5
        elif dx > dy:
            if_go = 1 # идём куда-то
            i_go_here = 0 # пойдём по х
            if dx < 0.5:
                i_go_where = 0 #идём влево <-
            else:
                i_go_where = 1 # идём вправо ->
            '''dy = 0.5
            if dx > 0.5:
                dx = 1
            else:
                dx = 0'''
        else:
            if_go = 1  # идём куда-то
            i_go_here = 1  # пойдём по y
            if dy < 0.5:
                i_go_where = 0  # идём вниз V
            else:
                i_go_where = 1  # идём вверх ^

        return (if_go, i_go_here, i_go_where)
        #!!!return self.__sigmoid(numpy.dot(inputs, self.synaptic_weights))
