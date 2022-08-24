def greet():
    print("________________________")
    print("    Приветствуем вас    ")
    print("         в игре         ")
    print("    крестики - нолики   ")
    print("    формат ввода: х у   ")
    print("    x - номер строки    ")
    print("    y - номер стобца    ")
    print("________________________")

def table_():
    print()
    print("  | 0 | 1 | 2 | ")
    print("--+---+---+----")
    for i, row in enumerate(field):
        row_str = f"{i} | {' | '.join(row)} | "
        print(row_str)
        print("--+---+---+----")
    print()

def ask_():
    while True:
        cords = input("      Ваш ход : ").split()

        if len(cords) != 2:
            print(" Введите только две координаты ")
            continue

        x, y = cords

        if not(x.isdigit()) or not (y.isdigit()):
            print(" Введите только числа")
            continue

        x, y = int(x), int(y)

        if 0 > x or x > 2 or 0 > y or y > 2:
            print(" Введите координаты в диапазоне от 0 до 2 ")
            continue

        if field[x][y] != " ":
            print(" Клетка занята ")
            continue

        return x, y

def check_win():
    win_cord = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)))
    for cord in win_cord:
        symbols = []
        for c in cord:
            symbols.append(field[c[0]][c[1]])
        if symbols == ["X", "X", "X"]:
            print(" Выйграл Х")
            return True
        if symbols == ["0", "0", "0"]:
             print(" Выйграл 0")
             return True
    return False

greet()
field = [[" "] * 3 for i in range(3)]
count = 0
while True:
    count += 1
    table_()
    if count % 2 == 1:
        print(" Ходят крестики")
    else:
        print(" Ходят нолики")

    x, y = ask_()

    if count % 2 == 1:
        field[x][y] = "X"
    else:
        field[x][y] = "0"

    if check_win():
        break

    if count == 9:
        print(" Ничья")
        break

