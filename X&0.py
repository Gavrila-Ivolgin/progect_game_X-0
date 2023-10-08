#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from colorama import init
import time
from colorama import Fore, Style

init()

CHOICE_USER = '1'
SCORE_USERNAME = 0
SCORE_BOT_NAME = 0
COUNTER = 0  # Счётчик партий
FORK = 0  # Вилка

username = input('Введите ваше имя: ')
print('Hello,', Fore.LIGHTGREEN_EX + username.upper(), Style.RESET_ALL + '!')

view = [
    ["   * ", "1 ", "2 ", "3 "],
    ["   1 ", "  ", "  ", "  "],
    ["   2 ", "  ", "  ", "  "],
    ["   3 ", "  ", "  ", "  "],
]

view_1 = [
    ["   * ", "1 ", "2 ", "3 "],
    ["   1 ", "- ", "- ", "- "],
    ["   2 ", "- ", "- ", "- "],
    ["   3 ", "- ", "- ", "- "],
]

print('\nСтартовая позиция: ')
for row in view_1:
    for symbol in row:
        print(Fore.LIGHTGREEN_EX + symbol, Style.RESET_ALL, end='')
    print()
print()

view_2 = [
    ["   7 ", "8 ", "9 "],
    ["   4 ", "5 ", "6 "],
    ["   1 ", "2 ", "3 "],
]

print('Визуальная раскладка клавиатуры для ходов: ')
for row in view_2:
    for symbol in row:
        print(Fore.LIGHTCYAN_EX + symbol, Style.RESET_ALL, end='')
    print()
print()

description = "Чтобы сделать ход выберите координаты на поле:"

step = {
    7: (1, 1), 8: (1, 2), 9: (1, 3),
    4: (2, 1), 5: (2, 2), 6: (2, 3),
    1: (3, 1), 2: (3, 2), 3: (3, 3),
}

string = ""
count = 0

for key, value in step.items():
    string += f"Введите {key} для хода: {value} "
    count += 1
    if count % 3 == 0:
        string += "\n"
print(description)
print(string)

while CHOICE_USER == '1':

    heroes = ['Крокодил Гена', 'Старуха Шапокляк', 'Чебурашка', 'Сторож зоопарка',
              'Трубадур', 'Осёл', 'Принцесса', 'Петух', 'Кот', 'Пёс', 'Король']

    bot_name = random.choice(heroes)
    print('Против вас играет -', Fore.LIGHTBLUE_EX + bot_name, Style.RESET_ALL, end=' ')
    print('')

    if bot_name == 'Чебурашка':
        print(
            """
            ------.-""-.------
           |     /|     \\    |
           |    || o   o |   |
            ----||   /\  |----    
                 \\  __  /
                  '.___.'
            """
        )

    # Случайный выбор первого хода: 1 - user, 2 - bot
    element = [username, bot_name]
    first_step = random.choice(element)
    if first_step == username:
        print('В этот раз право первого хода "X" получает игрок:', Fore.LIGHTGREEN_EX + username, Style.RESET_ALL,
              end='!')
        print('')
    else:
        print('В этот раз право первого хода "X" получает игрок:', Fore.LIGHTBLUE_EX + bot_name, Style.RESET_ALL,
              end='!\n')
        print('')


    def print_view(val, sim):
        ind = list(val)
        # Сделать ход
        view[ind[0]][ind[1]] = sim

        for row in view:
            for symbol in row:
                if symbol == '0':
                    print(Fore.GREEN + symbol + '  ', Style.RESET_ALL, end='')
                elif symbol == 'x':
                    print(Fore.BLUE + symbol + '  ', Style.RESET_ALL, end='')
                else:
                    print(Fore.LIGHTYELLOW_EX + symbol + ' ', Style.RESET_ALL, end='')
            print()
        print()


    def print_step(fun):
        def wrapper(*args, **kwargs):
            result = fun(*args, **kwargs)

            print(f'Доступные ходы (№ клавиш): {sorted([x for x in step])}' if len(step) >= 1 else '')
            print(f'Осталось ходов: {len(step)}' if len(step) >= 1 else 'Ходов больше нет!\n')
            print('')

            return result

        return wrapper


    @print_step
    def coordinates(num):
        symbol = '0' if len(step) % 2 == 0 else 'x'
        deleted_item = step.pop(num)
        print_view(deleted_item, symbol)
        return step


    def check_win(view):
        # Проверка по горизонтали
        for row in view:
            if row[1] == row[2] == row[3] and all(cell.strip() != "" for cell in row[1:]):
                return True

        # Проверка по вертикали
        for col in range(4):
            if view[1][col] == view[2][col] == view[3][col] and all(
                    cell.strip() != "" for cell in [view[1][col], view[2][col], view[3][col]]):
                return True

        # Проверка по диагоналям
        if (view[1][1] == view[2][2] == view[3][3] and view[2][2].strip() != "") or (
                view[1][3] == view[2][2] == view[3][1] and view[2][2].strip() != ""):
            return True

        all_truthy = all(all(cell.strip() for cell in row) for row in view)
        if all_truthy:
            print(Fore.LIGHTYELLOW_EX + 'В партии ничья!'.upper() + Style.RESET_ALL)
            print('')

        return False


    # Эта функция выбирает из списка ходов наиболее оптимальный и возвращает ход
    # в цикл while
    def choosing_bot_move(view):
        global FORK
        keys_list = list(step.keys())
        if FORK == 2 and 2 in step:
            print(Fore.MAGENTA + 'От вилки не уйти! {2}' + Style.RESET_ALL)
            return 2

        if FORK == 6 and 6 in step:
            print(Fore.MAGENTA + 'От вилки не уйти! {6}' + Style.RESET_ALL)
            return 6


        if 7 < len(keys_list) <= 9 and 5 in keys_list: return 5  # 1-ый ход - занять центр поля
        if 6 <= len(keys_list) <= 9 and view[1][3].strip() != "" and view[2][2].strip() != "" and view[3][
            1].strip() != "" and 2 in step:
            print(Fore.LIGHTBLUE_EX + 'Делаю стратегический ход! {2}' + Style.RESET_ALL)
            return 2
        if 6 <= len(keys_list) <= 9 and view[1][1].strip() != "" and view[2][2].strip() != "" and view[3][
            3].strip() != "" and 8 in step:
            print(Fore.LIGHTBLUE_EX + 'Делаю стратегический ход! {8}' + Style.RESET_ALL)
            return 8

        if len(keys_list) == 5 and view[1][1].strip() != "" and view[2][2].strip() != "" and view[3][
                3].strip() != "" and view[1][2].strip() != "" and 9 in step:
            print(Fore.MAGENTA + 'Ловлю на ошибках: Вам вилка! {3}' + Style.RESET_ALL)
            FORK = 6  # Следующий победный ход на вилке
            return 9  # Вилка за x {8}

        if len(keys_list) == 5 and view[1][1].strip() != "" and view[2][2].strip() != "" and view[3][
                3].strip() != "" and view[2][3].strip() != "" and 1 in step:
            print(Fore.MAGENTA + 'Ловлю на ошибках: Вам вилка! {1}' + Style.RESET_ALL)
            FORK = 2  # Следующий победный ход на вилке
            return 1  # Вилка за x {6}

        if len(keys_list) == 5 and view[1][1].strip() != "" and view[2][2].strip() != "" and view[3][
                3].strip() != "" and view[2][1].strip() != "" and 1 in step:
            print(Fore.MAGENTA + 'Ловлю на ошибках: Вам вилка! {1}' + Style.RESET_ALL)
            FORK = 2  # Следующий победный ход на вилке
            return 1  # Вилка за x {4}

        if len(keys_list) == 5 and view[1][1].strip() != "" and view[2][2].strip() != "" and view[3][
                3].strip() != "" and view[3][2].strip() != "" and 9 in step:
            print(Fore.MAGENTA + 'Ловлю на ошибках: Вам вилка! {9}' + Style.RESET_ALL)
            FORK = 6  # Следующий победный ход на вилке
            return 9  # Вилка за x {2}

        # Проверка по горизонтали (ряд 1-3)
        if view[1][1] == 'x' and view[1][2] == 'x' and 9 in step or view[1][1] == '0' and view[1][
            2] == '0' and 9 in step:
            print(Fore.LIGHTGREEN_EX + 'Делаю умный ход по горизонтали! {9}' + Style.RESET_ALL)
            return 9
        if view[1][1] == 'x' and view[1][3] == 'x' and 8 in step or view[1][1] == '0' and view[1][
            3] == '0' and 8 in step:
            print(Fore.LIGHTGREEN_EX + 'Делаю умный ход по горизонтали! {8}' + Style.RESET_ALL)
            return 8
        if view[1][2] == 'x' and view[1][3] == 'x' and 7 in step or view[1][2] == '0' and view[1][
            3] == '0' and 7 in step:
            print(Fore.LIGHTGREEN_EX + 'Делаю умный ход по горизонтали! {7}' + Style.RESET_ALL)
            return 7
        if view[2][1] == 'x' and view[2][2] == 'x' and 6 in step or view[2][1] == '0' and view[2][
            2] == '0' and 6 in step:
            print(Fore.LIGHTGREEN_EX + 'Делаю умный ход по горизонтали! {6}' + Style.RESET_ALL)
            return 6
        if view[2][2] == 'x' and view[2][3] == 'x' and 4 in step or view[2][2] == '0' and view[2][
            3] == '0' and 4 in step:
            print(Fore.LIGHTGREEN_EX + 'Делаю умный ход по горизонтали! {4}' + Style.RESET_ALL)
            return 4
        if view[3][1] == 'x' and view[3][2] == 'x' and 3 in step or view[3][1] == '0' and view[3][
            2] == '0' and 3 in step:
            print(Fore.LIGHTGREEN_EX + 'Делаю умный ход по горизонтали! {3}' + Style.RESET_ALL)
            return 3
        if view[3][1] == 'x' and view[3][3] == 'x' and 2 in step or view[3][1] == '0' and view[3][
            3] == '0' and 2 in step:
            print(Fore.LIGHTGREEN_EX + 'Делаю умный ход по горизонтали! {2}' + Style.RESET_ALL)
            return 2
        if view[3][2] == 'x' and view[3][3] == 'x' and 1 in step or view[3][2] == '0' and view[3][
            3] == '0' and 1 in step:
            print(Fore.LIGHTGREEN_EX + 'Делаю умный ход по горизонтали! {1}' + Style.RESET_ALL)
            return 1

        # Проверка по вертикали (колонки 1-3)
        if view[1][1] == 'x' and view[2][1] == 'x' and 1 in step or view[1][1] == '0' and view[2][
            1] == '0' and 1 in step:
            print(Fore.LIGHTGREEN_EX + 'Делаю умный ход по вертикали! {1}' + Style.RESET_ALL)
            return 1
        if view[1][1] == 'x' and view[3][1] == 'x' and 4 in step or view[1][1] == '0' and view[3][
            1] == '0' and 4 in step:
            print(Fore.LIGHTGREEN_EX + 'Делаю умный ход по вертикали! {4}' + Style.RESET_ALL)
            return 4
        if view[2][1] == 'x' and view[3][1] == 'x' and 7 in step or view[2][1] == '0' and view[3][
            1] == '0' and 7 in step:
            print(Fore.LIGHTGREEN_EX + 'Делаю умный ход по вертикали! {7}' + Style.RESET_ALL)
            return 7

        if view[1][2] == 'x' and view[2][2] == 'x' and 2 in step or view[1][2] == '0' and view[2][
            2] == '0' and 2 in step:
            print(Fore.LIGHTGREEN_EX + 'Делаю умный ход по вертикали! {2}' + Style.RESET_ALL)
            return 2
        if view[2][2] == 'x' and view[3][2] == 'x' and 8 in step or view[2][2] == '0' and view[3][
            2] == '0' and 8 in step:
            print(Fore.LIGHTGREEN_EX + 'Делаю умный ход по вертикали! {8}' + Style.RESET_ALL)
            return 8

        if view[1][3] == 'x' and view[2][3] == 'x' and 3 in step or view[1][3] == '0' and view[2][
            3] == '0' and 3 in step:
            print(Fore.LIGHTGREEN_EX + 'Делаю умный ход по вертикали! {3}' + Style.RESET_ALL)
            return 3
        if view[1][3] == 'x' and view[3][3] == 'x' and 6 in step or view[1][3] == '0' and view[3][
            3] == '0' and 6 in step:
            print(Fore.LIGHTGREEN_EX + 'Делаю умный ход по вертикали! {6}' + Style.RESET_ALL)
            return 6
        if view[2][3] == 'x' and view[3][3] == 'x' and 9 in step or view[2][3] == '0' and view[3][
            3] == '0' and 9 in step:
            print(Fore.LIGHTGREEN_EX + 'Делаю умный ход по вертикали! {9}' + Style.RESET_ALL)
            return 9

        # Проверка по диагоналям
        if view[1][1] == 'x' and view[2][2] == 'x' and 3 in step or view[1][1] == '0' and view[2][
            2] == '0' and 3 in step:
            print(Fore.LIGHTGREEN_EX + 'Делаю умный ход по диагонали! {3}' + Style.RESET_ALL)
            return 3

        if view[3][3] == 'x' and view[2][2] == 'x' and 7 in step or view[3][3] == '0' and view[2][
            2] == '0' and 7 in step:
            print(Fore.LIGHTGREEN_EX + 'Делаю умный ход по диагонали! {7}' + Style.RESET_ALL)
            return 7

        if view[3][1] == 'x' and view[2][2] == 'x' and 9 in step or view[3][1] == '0' and view[2][
            2] == '0' and 9 in step:
            print(Fore.LIGHTGREEN_EX + 'Делаю умный ход по диагонали! {9}' + Style.RESET_ALL)
            return 9

        if view[1][3] == 'x' and view[2][2] == 'x' and 1 in step or view[1][3] == '0' and view[2][
            2] == '0' and 1 in step:
            print(Fore.LIGHTGREEN_EX + 'Делаю умный ход по диагонали! {1}' + Style.RESET_ALL)
            return 1

        else:
            if view[3][3].strip() == "" and 3 in step:
                print(Fore.LIGHTCYAN_EX + 'Мне подсказали этот ход! {3}' + Style.RESET_ALL)
                return 3
            if view[1][3].strip() == "" and 9 in step:
                print(Fore.LIGHTCYAN_EX + 'Мне подсказали этот ход! {9}' + Style.RESET_ALL)
                return 9

            print(Fore.LIGHTRED_EX + 'Хожу закрытыми глазами :-)' + Style.RESET_ALL)
            return random.choice(keys_list)


    print('')
    print("{0:=^90}".format("START_GAME"))

    while step:
        if first_step == username:
            try:
                symbol = '0' if len(step) % 2 == 0 else 'x'
                if symbol == '0':
                    print('Вы играете знаком => ', Fore.LIGHTGREEN_EX + symbol + Style.RESET_ALL)
                else:
                    print('Вы играете знаком => ', Fore.LIGHTBLUE_EX + symbol + Style.RESET_ALL)
                step_user = int(input('Сделайте Ваш ход: '))
                print('')
                if not step_user in step.keys():
                    print('Вы сделали недопустимый ход!')
                    continue
            except ValueError:
                print('Вы ввели недопустимое значение! Пожалуйста, введите' + Fore.LIGHTMAGENTA_EX + ' число!',
                      Style.RESET_ALL)
                continue

            coordinates(step_user)
            winner = username
            first_step = bot_name

        else:
            keys_list = list(step.keys())
            step_bot = choosing_bot_move(view)
            print('Игрок', Fore.LIGHTBLUE_EX + bot_name + Style.RESET_ALL, 'сделал свой ход', end='!\n')
            print('')
            coordinates(step_bot)
            winner = bot_name
            first_step = username

        win = check_win(view)
        if win:
            print('')
            print(Fore.LIGHTRED_EX + 'Игра закончена!'.upper() + Style.RESET_ALL)
            time.sleep(2)
            if winner == username:
                print('Поздравляем!')
                print('Вы победитель в партии,', Fore.LIGHTGREEN_EX + winner + Style.RESET_ALL, end='!\n')
                SCORE_USERNAME += 1
            elif winner == bot_name:
                print('Победитель в партии:', Fore.LIGHTBLUE_EX + winner + Style.RESET_ALL, end='!\n')
                print('Ваш соперник оказался достойным!')
                SCORE_BOT_NAME += 1
            break

    COUNTER += 1

    print("{0:=^90}".format("***"))
    print()
    print(Fore.LIGHTBLUE_EX + 'Сыграно партий: ', COUNTER)
    print('Одержано побед:' + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.LIGHTGREEN_EX + username.upper(), '= ' + str(SCORE_USERNAME) + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.LIGHTBLUE_EX + 'Чебурашка и его друзья = ' + str(SCORE_BOT_NAME) + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.LIGHTYELLOW_EX + 'Количество партий, сыгранных вничью: ' + str(
        COUNTER - (SCORE_USERNAME + SCORE_BOT_NAME)) + Style.RESET_ALL)
    print('')

    feedback = (
        f"Уважаемый пользователь!\n"
        f"Отзывы и предложения по работе программы\n"
        f"ожидаются на {Fore.BLUE}Nebosst@yandex.ru{Style.RESET_ALL}\n"
    )
    print(feedback)
    print('')

    CHOICE_USER = input(
        Fore.LIGHTBLUE_EX + 'Чтобы сыграть ещё раз, введите 1, для выхода нажмите Enter: ' + Style.RESET_ALL)

    if CHOICE_USER == '1':
        FORK = 0  # Обновляем счётчик вилки
        print('')
        print('Играем ещё раз! Удачи!')
        print('')

        # Обновляем поле и список ходов
        view = [
            ["   * ", "1 ", "2 ", "3 "],
            ["   1 ", "  ", "  ", "  "],
            ["   2 ", "  ", "  ", "  "],
            ["   3 ", "  ", "  ", "  "],
        ]

        step = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
        }
    else:
        print(
            'Вы вышли из программы. До новых встреч, ' + Fore.LIGHTGREEN_EX + username.upper() + Style.RESET_ALL + '!')
        time.sleep(3)
