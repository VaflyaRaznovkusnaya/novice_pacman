'''
Модуль-движок сеть pacman.py
Цель данного модуля: Это головной модуль, запуск которого является запуском самой игры.
Внутри данного модуля реализуются функции визуализатора для динамичной отрисовки игрового поля,
функция генерации рандомной карты при начальном запуске и переходе по уровням, создания противника на основе
сгенерированного игрового поля, функция "поднятия" предмета-точки (кристала), функция для динамично происходящих событий
как передвижение игрок и противника, их коллизии, функция вывода текста-баннера для пользователя, функция рандомного движения для противника,
функция, считывающая нажатие кнопок пользователем для определения движения игрока, а так же перехода на другой уровень,
две функции, считывающие нажатие и отпускание клавиш для перемещения игрока или противника на другую сторону
карты в случае выхода за её пределы, функция для корректного перемещения и коллизии со стенами, функция для считывания
наличия стен перед движением, функция для сбрасывания текущих позиций игрока и противника до их начальных,
функция реализующая критерий для прохождения текущего уровня и перехода на следующий, функция для определения альтернатив,
функция периода, релизующая переодическую проверку критериев и работы функций, связанных с ними.
В самом начале модуля задаются переменные и словарь для корректной работы, объявляется экземпляр класса нейронной сети,
проихводится его тренеровка. После объявления последней функции назначается время переодичности функции периода,
вызываются функции создания мира, с которой начинается игра для пользователя, и функция создания противников.
Функция обновления использует внутри себя метод экземпляра класса Нейронной сети для определения движеня противника,
предварительно проверяя наличие стен для предотвращения проблемы с коллизией.
'''

# libraries
import random
import math
import randomize
from neural import NeuralNetwork

TEST_MODE = True

world = [] #!!!!!!!!!!!!!!!!
enemies = []
enemies_start_position = []

SPEED = 2
ENEMY_SPEED = 1
# Resolutions
TITLE = "Pac-Man"
WORLD_SIZE = 20  #
BLOCK_SIZE = 32  #
WIDTH = WORLD_SIZE * BLOCK_SIZE
HEIGHT = WORLD_SIZE * BLOCK_SIZE

# Our sprites
pacman = Actor("pacman_o.png")

#pacman.x = pacman.y = 1.5 * BLOCK_SIZE ############################!!!!!!!!!!!!!!!
# 1 for down and right, -1 for up and left
pacman.dx, pacman.dy = 0, 0
pacman.shards_left = None
pacman.level = 1
pacman.banner = None
pacman.banner_counter = 0
pacman.score = 0
#pacman.lives = 3
pacman.powerup = 0

# images dictionaries
char_to_image = {
    ".": "dot.png",
    "=": "wall.png",
    "*": "power.png",
    "e": "enemy1.png",
    "E": "enemy2.png",
}

neural_network = NeuralNetwork()
neural_network.train(10000)

# code
def create_world():
    variants = ['e', '*', '.', '=', 'p']
    #variants = ['e', '*', '.', '=']
    pacman.shards_left = 0
    Enemy = True
    Player = True
    for i in range (WORLD_SIZE):
        row = []
        percentage_Shards = round((WORLD_SIZE/100)*50) #63
        percentage_Blocks = round((WORLD_SIZE/100)*40) #30
        percentage_PowerUp = round((WORLD_SIZE/100)*10) #5

        for j in range (WORLD_SIZE):
            what = random.choice(variants)
            if (i % 2) == 0:
                row.append(".")
                pacman.shards_left += 1
            else:
                while True: #go:
                    if what == "e":
                        if Enemy:
                            row.append(what)
                            Enemy = False
                            break
                            #go = False
                        else:
                            #Переброс
                            what = random.choice(variants)
                    elif what == "p":
                        if Player:
                            row.append('*')
                            global remember_x, remember_y
                            remember_x = j
                            remember_y = i
                            pacman.x = (remember_x + 0.5) * BLOCK_SIZE
                            pacman.y =  (remember_y + 0.5) * BLOCK_SIZE
                            Player = False
                            break
                        else:
                            what = random.choice(variants)
                    elif what == ".":
                        if percentage_Shards > 0:
                            row.append(what)
                            percentage_Shards -= 1
                            pacman.shards_left += 1
                            break
                            #go = False
                        else:
                            #Переброс
                            what = random.choice(variants)
                    elif what == "*":
                        if percentage_PowerUp > 0:
                            row.append("*")
                            percentage_PowerUp -= 1
                            break
                            #go = False
                        else:
                            #Переброс
                            what = random.choice(variants)
                    elif what == "=":
                        if percentage_Blocks > 0:
                            row.append(what)
                            percentage_Blocks -= 1
                            break
                            #go = False
                        else:
                            #Переброс
                            what = random.choice(variants)

        world.append(row)

def make_enemies_actors():
    for y, row in enumerate(world):
        for x, block in enumerate(row):
            if block == "e" or block == "E":
                e = Actor(
                    char_to_image[block],
                    (x * BLOCK_SIZE, y * BLOCK_SIZE),
                    anchor=("left", "top"),
                )
                e.orig_image = e.image
                # Random direction
                new_enemy_direction(e)
                enemies.append(e)
                enemies_start_position.append((x,y))
                # убираем спрайт с экрана, т.к. теперь есть актёр
                world[y][x] = None


def pick_up_shard():
    ix, iy = int(pacman.x / BLOCK_SIZE), int(pacman.y / BLOCK_SIZE)
    if world[iy][ix] == '.':
        world[iy][ix] = None
        pacman.shards_left -= 1
        pacman.score += 1
        #print("shards left: ", pacman.shards_left)
    elif world[iy][ix] == '*':
        world[iy][ix] = None
        pacman.score += 5
        pacman.powerup = 25
        set_banner("I HAVE POWER!", 5)
        for e in enemies: new_enemy_direction(e)



def draw():
    screen.clear()

    for y, row in enumerate(world):
        for x, block in enumerate(row):
            image = char_to_image.get(block, None)
            if image:
                screen.blit(char_to_image[block], (x * BLOCK_SIZE, y * BLOCK_SIZE))
    pacman.draw()
    for e in enemies:
        e.draw()

    if pacman.banner and pacman.banner_counter > 0:
        screen.draw.text(pacman.banner, center=(WIDTH/2, HEIGHT/2), fontsize=120)
    screen.draw.text("Score: %s" % pacman.score, topleft=(8, 4), fontsize=40)
    #screen.draw.text("Lives: %s" % pacman.lives, topright=(WIDTH-8,4), fontsize=40)


def update():  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!update here!!!!!!!!!!!!!
    # Проверяем, что нет стен
    move_ahead(pacman)
    pick_up_shard()
    if pacman.shards_left == 0:
        next_level()

    for e in enemies:
        if not move_ahead(e):
            #new_enemy_direction(e) # ДВИЖЕНИЕ МОНСТРА!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            #Получаем при помощи текущего
            my_out = list(neural_network.think(pacman.x, pacman.y, e.x, e.y))

            if my_out[0] == 1:
                if my_out[1] == 0: #Идём по х
                    if my_out[2] == 0:#идём влево <-
                        e.dx = math.copysign(ENEMY_SPEED*1.5, e.x - 1)
                    else:# идём вправо ->
                        e.dx = math.copysign(ENEMY_SPEED*1.5, e.x + 1)
                else: #Идём по y
                    if my_out[2] == 0:# идём вниз V
                        e.dy = math.copysign(ENEMY_SPEED*1.5, e.y - 1)
                    else:# идём вверх ^
                        e.dy = math.copysign(ENEMY_SPEED*1.5, e.y + 1)

        if e.colliderect(pacman):
            set_banner("YoU DiEd!", 5)
            #pacman.lives -= 1
            pacman.score -= 123
            reset_sprites()


def set_banner(message, count):
  pacman.banner = message
  pacman.banner_counter = count

def new_enemy_direction(e):
  if pacman.powerup:
      e.dx = math.copysign(ENEMY_SPEED*1.5, e.x - pacman.x)
      e.dy = math.copysign(ENEMY_SPEED*1.5, e.y - pacman.y)
  else:
      e.dx = random.choice([-ENEMY_SPEED, ENEMY_SPEED])
      e.dy = random.choice([-ENEMY_SPEED, ENEMY_SPEED])

def on_key_down(key):  # движение игрока, зажата кнопка
    if key == keys.LEFT:
        pacman.dx = -SPEED
    if key == keys.RIGHT:
        pacman.dx = SPEED
    if key == keys.UP:
        pacman.dy = -SPEED
    if key == keys.DOWN:
        pacman.dy = SPEED


def on_key_up(key):  # движение игрока, кнопка отпущена
    if key in (keys.LEFT, keys.RIGHT):
        pacman.dx = 0
    if key in (keys.UP, keys.DOWN):
        pacman.dy = 0
    if TEST_MODE:
        if key == key.Q:
            next_level()


def move_around(minum, val, maxum):  #  телепортация при выходе за пределы массива
    if val < minum:
        return maxum
    elif val > maxum:
        return minum
    else:
        return val


def move_ahead(sprite):  # Спрайт не может проходить сквозь стены
    oldx, oldy = sprite.x, sprite.y
    if "=" not in blocks_ahead_of(sprite, sprite.dx, 0):
        sprite.x += sprite.dx
    if "=" not in blocks_ahead_of(sprite, 0, sprite.dy):
        sprite.y += sprite.dy
    # спрайты телепортируются на др. сторону, если вышли за границу
    sprite.x = move_around(0, sprite.x, WIDTH - BLOCK_SIZE)
    sprite.y = move_around(0, sprite.y, HEIGHT - BLOCK_SIZE)
    # return сдвинулись ли мы с места?
    moved = (oldx != sprite.x or oldy != sprite.y)
    # changing sprites
    if moved and sprite == pacman:
        a = 0
        if oldx < sprite.x : a = 0
        elif oldy > sprite.y: a = 90
        elif oldx > sprite.x: a = 180
        elif oldy < sprite.y: a = 270
        sprite.angle = a
    return moved


def blocks_ahead_of(sprite, dx, dy):
    """возвращает лист блоков в тек. позиции + координаты dx, dy"""
    # Куда мы идём
    x = int(round(sprite.left)) + dx
    y = int(round(sprite.top)) + dy

    # Находим координаты блока (4.7 -> 4)
    ix, iy = int(x // BLOCK_SIZE), int(y // BLOCK_SIZE)
    # проверяем соседние блоки
    rx, ry = x % BLOCK_SIZE, y % BLOCK_SIZE
    if ix == WORLD_SIZE - 1:
        rx = 0
    if iy == WORLD_SIZE - 1:
        ry = 0

    blocks = [world[iy][ix]]
    if rx:
        blocks.append(world[iy][ix + 1])
    if ry:
        blocks.append(world[iy + 1][ix])
    if rx and ry:
        blocks.append(world[iy + 1][ix + 1])

    return blocks

def reset_sprites():
    # Перемещаем героя
    #pacman.x = pacman.y = 1.5 * BLOCK_SIZE
    pacman.x = (remember_x + 0.5)* BLOCK_SIZE
    pacman.y =  (remember_y + 0.5)* BLOCK_SIZE
    # Перемещаем монстров
    for e, (x, y) in zip(enemies, enemies_start_position):
        e.x = x* BLOCK_SIZE
        e.y = y* BLOCK_SIZE

def next_level():
    global world, enemies, enemies_start_position
    world = []
    enemies = []
    enemies_start_position = []

    #pacman.level += 1
    #load_level(pacman.level)
    create_world()

    make_enemies_actors()

    reset_sprites()

def alternate(value, option1, option2):
  if value == option1: return option2
  else: return option1

def periodic():
    if pacman.banner_counter > 0:
        pacman.banner_counter -= 1
    if pacman.powerup > 0:
        pacman.powerup -= 1
    if pacman.powerup > 10:
       # The blue version for fleeing ghosts
        for e in enemies: e.image = 'enemy3.png'
    else:
       # Flash for the last few seconds
        for e in enemies:
            e.image = alternate(e.image, 'enemy3.png', 'enemy4.png')

    if pacman.powerup == 0:
        for e in enemies: e.image = e.orig_image


clock.schedule_interval(periodic, 0.2)


# testing
#load_level(1)
create_world()
make_enemies_actors()

# print(world)
