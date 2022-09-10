from numpy import arange
import math
import Service


def hello():
    print("Лабораторная №3: \"Численное интегрирование\"")
    print("Вариант: метод Симпсона (метод парабол)")
    print("Автор: Неграш А.В., P3230\n")


def get_data():
    print("""Выберите уравнение:
    1: sin(x)
    2: x^3
    3: sin(x) / x
    4: 1 / x""")

    match input("> "):
        case "1":
            func = lambda x: math.sin(x)
            d_func = lambda x: math.sin(x)
            print("Вы выбрали функцию sin(x)")
        case "2":
            func = lambda x: x * x * x
            d_func = lambda x: 0 * x
            print("Вы выбрали функцию x^3")
        case "3":
            func = lambda x: math.sin(x) / x
            d_func = lambda x: x * math.pow(x, -4) * (
                    4 * x * math.cos(x) - 12 * math.sin(x) + 24 * math.sin(x) * math.pow(x, -2) - 24 * math.cos(
                x) * math.pow(x, -1) + math.sin(x) * math.pow(x, 2))
            print("Вы выбрали функцию sin(x)/x")
        case "4":
            func = lambda x: 1 / x
            d_func = lambda x: 24 * math.pow(x, -5)
            print("Вы выбрали функцию 1/x")
        case _:
            print("Вы ввели некорректное значение")
            return get_data()
    left_border, right_border = Service.get_interval()
    return func, left_border, right_border, Service.get_sigma(), d_func


def get_r(left_border, right_border, n, d_func, h):
    r = 0
    for i in arange(left_border, right_border, h):
        try:
            cur_r = d_func(i)
            cur_r *= math.pow((right_border - left_border), 5)
            cur_r /= (180 * math.pow(n, 4))
        except ValueError:
            cur_r = 0
        if abs(cur_r) > r:
            r = abs(cur_r)
    return r


def print_gap(x):
    print("Был найден разрыв функции в точке: " + str(x) +
          "\nВыполняется расчёт левой и правой от разрыва частей интеграла")


def simpson(func, a, b, eps, d_func):
    integral = 0
    n = int((b - a) / eps)
    h = (b - a) / n

    try:
        integral += func(a)
    except ZeroDivisionError:
        print_gap(a)

    try:
        integral += func(b)
    except ZeroDivisionError:
        print_gap(b)

    for i in range(1, n):
        k = 2 + 2 * (i % 2)
        try:
            integral += k * func(a + i * h)
        except ZeroDivisionError:
            print_gap(a + i * h)
    integral *= h / 3

    if get_r(a, b, n, d_func, h) >= abs(integral):
        print("Был найден разрыв второго рода")
        return
    else:
        return integral


hello()
func, left_border, right_border, eps, d_func = get_data()
result = simpson(func, left_border, right_border, eps, d_func)
if result is not None:
    print("Подсчитанный интеграл на интервале [" + str(left_border) + "; " + str(right_border) + "] равен: " + str(result))
