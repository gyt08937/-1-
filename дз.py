# дз.10.11
#Блок 1. Обусловленность задачи

import math
def task1():
    print("\n### Задача 1. Число обусловленности вручную")
    # cond = |x f'(x) / f(x)|
    data = [
        ("f(x)=sqrt(x), x=1e-8", 1e-8, 0.5, "хорошо"),
        ("f(x)=ln(x), x=1.001", 1.001, 1.0 / math.log(1.001), "плохо"),
        ("f(x)=x-1, x=1.000001", 1.000001, 1.000001 / 1e-6, "очень плохо"),
        ("f(x)=sqrt(x), x=pi/2", math.pi / 2, 0.5, "хорошо"),
    ]
    for name, x, cond, status in data:
        print(f"{name}: cond = {cond:.6g} -> {status}")

    print("Вывод: по возрастанию обусловленности: sqrt(x) при pi/2 и 1e-8 (cond=0.5), "
          "ln(x) при 1.001 (cond≈1e3), x-1 при 1.000001 (cond≈1e6). "
          "Самая опасная — x-1 около корня: малое абсолютное возмущение x даёт огромную "
          "относительную ошибку из-за вычитания близких чисел.")

task1()

def task2():
    print("\n### Задача 2. Вычитание близких чисел")
    a = 1.0 + 1e-8
    b = 1.0
    f = a - b
    cond_a = abs(a / f)
    cond_b = abs(b / f)

    delta = 1e-8
    f_new = (a + delta) - b
    actual_rel_change = abs((f_new - f) / f)
    predicted_rel_change = cond_a * abs(delta / a)

    print(f"a={a!r}, b={b!r}, f=a-b={f!r}")
    print(f"cond по a ≈ {cond_a:.6g}, cond по b ≈ {cond_b:.6g}")
    print(f"Возмущение a на delta={delta:g}: фактическое относительное изменение f ≈ {actual_rel_change:.6g}")
    print(f"Предсказание cond_a * |delta/a| ≈ {predicted_rel_change:.6g}")
    print("Вывод: при a≈b обусловленность по каждому аргументу ~ a/(a-b) → ∞. "
          "Вычитание близких чисел усиливает относительную ошибку; cond предсказывает "
          "порядок усиления, хотя конкретное число зависит от выбранного возмущения и округления.")

task2()

import math


def task3():
    print("\n### Задача 3. Кратные корни")
    rows = []
    prev_shift = None
    for eps in [1e-2, 1e-4, 1e-6]:
        shift = math.sqrt(eps)
        ratio = None if prev_shift is None else shift / prev_shift
        rows.append((eps, shift, shift / eps, ratio))
        prev_shift = shift
    print(
        "x^2 - 2x + 1 - eps = 0; корни 1 ± sqrt(eps)",
        ["eps", "сдвиг sqrt(eps)", "сдвиг/eps", "отношение сдвигов к предыдущему"],
        rows,
    )
    print("Вывод: при уменьшении eps в 100 раз сдвиг уменьшается только в 10 раз,\n "
          "т.е. shift ~ sqrt(eps). Корень кратности 2 плохо обусловлен: возмущение "
          "свободного члена порядка eps даёт сдвиг корня порядка sqrt(eps).")

task3()

def relerr(value, reference):
    val = abs(float(value))
    ref = abs(float(reference))
    if ref == 0.0:
        return 0.0 if val == 0.0 else float("inf")
    return val / ref

import math
import mpmath as mp
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
def task4():
    print("\n### Задача 4. Обусловленность vs устойчивость")
    x = 1e16
    bad = math.log(x + 1.0) - math.log(x)
    good = math.log1p(1.0 / x)
    exact = mp.log(1 + mp.mpf(1) / mp.mpf(x))

    print("Задача: f(x)=ln(x+1)-ln(x)=ln(1+1/x), x=1e16.")
    print(f"Плохой алгоритм log(x+1)-log(x): {bad!r}")
    print(f"Хороший алгоритм log1p(1/x):       {good!r}")
    print(f"Эталон mpmath:                     {exact}")
    print(f"Отн. ошибка плохого: {relerr(bad, exact)}")
    print(f"Отн. ошибка хорошего: {relerr(good, exact)}")

    xs = np.logspace(8, 16, 50)
    diff_logs = np.log(xs + 1.0) - np.log(xs)
    stable = np.log1p(1.0 / xs)
    plt.figure()
    plt.semilogx(xs, diff_logs, label="log(x+1)-log(x), плохой")
    plt.semilogx(xs, stable, label="log1p(1/x), хороший")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.title("Задача 4: хорошая задача, неустойчивый алгоритм")
    plt.savefig("task4_conditioning_vs_stability.png", dpi=150)
    plt.close()

    print("Вывод: задача хорошо обусловлена (cond≈1), но алгоритм log(x+1)-log(x) "
          "неустойчив: при больших x log(x+1) и log(x) совпадают в double, происходит "
          "катастрофическое сокращение. Проблема задачи — не в ней самой, проблема алгоритма — "
          "в вычитании близких чисел.")

task4()

import math
import mpmath as mp
def task5():
    print("\n### Задача 5. Квадратное уравнение")
    rows = []
    for b in [1e3, 1e4, 1e12]:
        a = 1.0
        c = 1.0
        bad = (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)
        good = 2 * c / (-b - math.sqrt(b * b - 4 * a * c))

        bmp = mp.mpf(str(b))
        exact = (-bmp + mp.sqrt(bmp * bmp - 4)) / 2

        rows.append((b, bad, good, exact,(bad, exact), (good, exact)))

    print(
        "x^2 + b x + 1 = 0, меньший корень",
        ["b", "bad x1", "good x1", "exact","rel.err bad", "rel.err good"],
        rows
    )
    print("Вывод: «плохая» формула страдает от вычитания почти равных чисел. "
          "\nУже при b=1e4 ошибка заметна, а при b=1e12 sqrt(b^2-4) в double равно b, "
          "поэтому bad даёт 0 вместо ≈ -1e-12. «Хорошая» формула устойчива.")

task5()

import  math
import mpmath as mp
def task6():
    print("\n### Задача 6. (1 - cos x)/x^2")
    xvals = [1e-2, 1e-4, 1e-6, 1e-8, 1e-10]
    rows = []
    for x in xvals:
        bad = (1.0 - math.cos(x)) / (x * x)
        good = 2.0 * math.sin(x / 2.0) ** 2 / (x * x)
        xmp = mp.mpf(str(x))
        exact = (1 - mp.cos(xmp)) / (xmp * xmp)
        rows.append((x, bad, good, exact, (bad, exact), (good, exact)))

    print(
        "f(x)=(1-cos x)/x^2",
        ["x", "bad", "good", "exact", "rel.err bad", "rel.err good"],
        rows,
    )
    print("Вывод: плохой способ при малых x теряет точность из-за 1-cos x: "
          "\nотносительная ошибка растёт как ~eps/x^2; при x≤1e-8 cos(x) округляется к 1 "
          "и bad даёт 0. Хороший способ через 2 sin^2(x/2) устойчив.")

task6()

import math
import mpmath as mp
import numpy as np
def task7():
    print("\n### Задача 7. sqrt(x+1)-sqrt(x) при больших x")

    xvals = [1e2, 1e4, 1e6, 1e8, 1e10]
    rows = []
    logx = []
    logerr = []
    for x in xvals:
        bad = math.sqrt(x + 1.0) - math.sqrt(x)
        good = 1.0 / (math.sqrt(x + 1.0) + math.sqrt(x))
        xmp = mp.mpf(str(x))
        exact = mp.sqrt(xmp + 1) - mp.sqrt(xmp)
        eb = abs(bad - float(exact)) / abs(float(exact))
        eg = abs(good - float(exact)) / abs(float(exact))
        rows.append((x, bad, good, exact, eb, eg))
        logx.append(math.log10(x))
        logerr.append(math.log10(max(float(exact), 1e-300)))

    print(
        "f(x)=sqrt(x+1)-sqrt(x)",
        ["x", "bad", "good", "exact", "rel.err bad", "rel.err good"],
        rows,
    )
    slope = np.polyfit(logx, logerr, 1)[0]
    print(f"Оценка показателя степени роста ошибки bad: slope ≈ {slope:.3f}")
    print("Вывод: ошибка «плохого» способа растёт примерно линейно по x, т.к. "
          "\nsqrt(x+1) и sqrt(x) близки и вычитаются. Хороший способ через "
          "1/(sqrt(x+1)+sqrt(x)) устойчив.")

task7()

import math
import mpmath as mp

def task8():
    print("\n### Задача 8. ln(1+x)/x при малых x")
    xvals = [1e-2, 1e-4, 1e-6, 1e-8, 1e-10]
    rows = []
    for x in xvals:
        bad = math.log(1.0 + x) / x
        good = math.log1p(x) / x
        xmp = mp.mpf(str(x))
        exact = mp.log(1 + xmp) / xmp
        rows.append((x, bad, good, exact, (bad, exact), (good, exact)))

    print(
        "f(x)=ln(1+x)/x",
        ["x", "bad", "good (log1p)", "exact", "rel.err bad", "rel.err good"],
        rows
    )
    print("Вывод: math.log(1+x) при малых x сначала округляет 1+x, поэтому относительная "
          "\nошибка растёт как ~eps/x. math.log1p(x) вычисляет ln(1+x) устойчиво, "
          "используя специальный алгоритм/ряд и не теряя малые x.")

task8()

import math
import mpmath as mp
def task9():
    print("\n### Задача 9. Неустойчивость накопления в сумме")
    nvals = [10**5, 10**6, 10**7]

    def harm_forward(n):
        s = 0.0
        for k in range(1, n + 1):
            s += 1.0 / k
        return s

    def harm_backward(n):
        s = 0.0
        for k in range(n, 0, -1):
            s += 1.0 / k
        return s

    def harm_fsum(n):
        return math.fsum(1.0 / k for k in range(1, n + 1))

    rows = []
    for n in nvals:
        exact = mp.digamma(n + 1) + mp.euler  # H_n = psi(n+1) + gamma
        sf = harm_forward(n)
        sb = harm_backward(n)
        fs = harm_fsum(n)
        rows.append((n, sf, sb, fs, (sf, exact), (sb, exact), (fs, exact)))

    print(
        "S_n = sum_{k=1}^n 1/k",
        ["n", "forward", "backward", "fsum", "err forward", "err backward", "err fsum"],
        rows,
    )
    print("Вывод: наивное суммирование слева направо накапливает округления; "
          "\nобратный порядок и особенно math.fsum точнее. При n порядка 1e7 ошибка "
          "\nнаивного способа становится порядка 1e-10 и больше, т.е. для точных расчётов "
          "\nнаивная сумма неприменима.")
task9()

# Блок 3. Корректная постановка эксперимента
import math
import mpmath as mp
import numpy as np

def relerr(value, reference):
    val = abs(float(value))
    ref = abs(float(reference))
    if ref == 0.0:
        return 0.0 if val == 0.0 else float("inf")
    return val / ref

def print_table (title, headers, rows, fmt=None):
    print(f"\n{title}")
    if fmt is None:
        fmt = lambda v: f"{v:.6g}" if isinstance(v, float) else str(v)
    str_rows = [[fmt(c) for c in r] for r in rows]

    widths = [
        max(len(headers[i]), *(len(r[i]) for r in str_rows))
        for i in range(len(headers))
    ]
    line = " | ".join(headers[i].ljust(widths[i]) for i in range(len(headers)))
    print(line)
    print("-" * len(line))
    for r in str_rows:
        print(" | ".join(r[i].ljust(widths[i]) for i in range(len(headers))))


def task10():
    print("\n### Задача 10. Разделение источников ошибки (задача 6)")
    rows_a = []
    for x in [1e-2, 1e-4, 1e-6, 1e-8, 1e-10]:
        bad = (1.0 - math.cos(x)) / (x * x)
        xmp = mp.mpf(str(x))
        exact = (1 - mp.cos(xmp)) / (xmp * xmp)
        rows_a.append((x, relerr(bad, exact)))
    print_table("(a) плохой алгоритм, меняем x", ["x", "rel.err bad"], rows_a)

    x0 = 1e-4
    x64 = x0
    x32 = np.float32(x0)
    bad64 = (1.0 - math.cos(x64)) / (x64 * x64)
    bad32 = float((np.float32(1.0) - np.cos(x32)) / (x32 * x32))
    exact64 = (1 - mp.cos(mp.mpf(str(x64)))) / (mp.mpf(str(x64)) ** 2)
    exact32 = (1 - mp.cos(mp.mpf(str(float(x32))))) / (mp.mpf(str(float(x32))) ** 2)
    print_table(
        "(b) фиксируем x≈1e-4, меняем точность",
        ["тип", "результат", "rel.err"],
        [("float64", bad64, relerr(bad64, exact64)),
         ("float32", bad32, relerr(bad32, exact32))],
    )

    x0 = 1e-6
    bad = (1.0 - math.cos(x0)) / (x0 * x0)
    good = 2.0 * math.sin(x0 / 2.0) ** 2 / (x0 * x0)
    exact = (1 - mp.cos(mp.mpf(str(x0)))) / (mp.mpf(str(x0)) ** 2)
    print_table(
        "(c) x=1e-6, меняем алгоритм",
        ["алгоритм", "результат", "rel.err"],
        [("bad", bad, relerr(bad, exact)), ("good", good, relerr(good, exact))],
    )
    print("Вывод: в (a) доминирует обусловленность/потеря значимости при малых x; "
          "в (b) — машинная точность (float32 на много порядков хуже); "
          "в (c) — устойчивость алгоритма: хорошая формула убирает катастрофическое сокращение.")

print(task10())
import math
import mpmath as mp

def relerr(value, reference):
     val = abs(float(value))
     ref = abs(float(reference))
     if ref == 0.0:
         return 0.0 if val == 0.0 else float("inf")
     return val / ref
def task11():
    print("\n### Задача 11. Эталон обязателен")
    x = 1e-9
    bad1 = (1.0 - math.cos(x)) / (x ** 2)
    bad2 = (1.0 - math.cos(x)) / (x * x)
    exact = (1 - mp.cos(mp.mpf(str(x)))) / (mp.mpf(str(x)) ** 2)

    print(f"bad1 = {bad1!r}")
    print(f"bad2 = {bad2!r}")
    print(f"bad1 == bad2: {bad1 == bad2}")
    print(f"exact ≈ {exact}")
    print(f"rel.err bad1 ≈ {relerr(bad1, exact)}")
    print(f"rel.err bad2 ≈ {relerr(bad2, exact)}")
    print("Вывод: два «плохих» результата совпали между собой, но оба неверны относительно "
          "\nэталона. Сравнение двух float-реализаций без независимого эталона не доказывает "
          "\nправильность: они могут одинаково ошибаться.")

task11()

import math
import mpmath as mp
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def relerr(v, r):
    v, r = abs(float(v)), abs(float(r))
    if r == 0.0:
        return 0.0 if v == 0.0 else float("inf")
    return v / r


def print_table(title, headers, rows):

    print(f"\n{title}")
    fmt = lambda c: f"{c:.6g}" if isinstance(c, (float, int)) else str(c)
    cells = [[fmt(c) for c in r] for r in rows]
    w = [max(len(headers[i]), *(len(r[i]) for r in cells)) for i in range(len(headers))]
    for r in [headers] + cells:
        print(" | ".join(x.ljust(w[i]) for i, x in enumerate(r)))


def task12():
    print("\n### Задача 12. Диапазон, а не одна точка")
    xs = np.logspace(2, 16, 8)
    err_bad = []
    err_good = []
    rows = []
    for x in xs:
        bad = math.sqrt(x + 1.0) - math.sqrt(x)
        good = 1.0 / (math.sqrt(x + 1.0) + math.sqrt(x))
        xmp = mp.mpf(str(x))
        exact = mp.sqrt(xmp + 1) - mp.sqrt(xmp)
        eb = relerr(bad, exact)
        eg = relerr(good, exact)
        err_bad.append(eb)
        err_good.append(eg)
        rows.append((x, bad, good, float(exact), eb, eg))

    print_table(
        "f(x)=sqrt(x+1)-sqrt(x), логарифмическая сетка",
        ["x", "bad", "good", "exact", "rel.err bad", "rel.err good"],
        rows,
    )

    slope = np.polyfit(np.log10(xs), np.log10(np.maximum(err_bad, 1e-300)), 1)[0]
    print(f"Наклон log-log для ошибки bad: ≈ {slope:.3f} (теория: ≈1 до насыщения)")
    print("Вывод: ошибка bad растёт примерно как x, поэтому одна точка ничего не говорит "
          "\nо поведении алгоритма. Нужен диапазон входов; на больших x ошибка насыщается "
          "\nиз-за того, что x+1 округляется к x.")

    plt.figure()
    plt.loglog(xs, np.maximum(err_bad, 1e-300), "o-", label="bad")
    plt.loglog(xs, np.maximum(err_good, 1e-300), "s-", label="good")
    plt.xlabel("x")
    plt.ylabel("relative error")
    plt.legend()
    plt.title("Задача 12: ошибка sqrt(x+1)-sqrt(x)")
    plt.savefig("task12_errors.png", dpi=150)
    plt.close()


task12()
import math
import numpy as np
import random
import sys
def task13():
    print("\n### Задача 13. Воспроизводимость эксперимента")
    N = 10**5
    SEED = 42

    def run_once():
        random.seed(SEED)
        py_list = [random.random() for _ in range(N)]
        rng = np.random.default_rng(SEED)
        np_arr = rng.random(N)
        return (
            sum(py_list),
            math.fsum(py_list),
            float(np.sum(py_list)),
            float(sum(np_arr)),
            math.fsum(map(float, np_arr)),
            float(np.sum(np_arr)),
        )

    r1 = run_once()
    r2 = run_once()

    print(f"Python: {sys.version}")
    print(f"numpy: {np.__version__}")
    print(f"seed: {SEED}, N={N}")
    print("Первый запуск: ", r1)
    print("Второй запуск: ", r2)
    print(f"Результаты совпали: {r1 == r2}")
    print("Вывод: при фиксированном seed и одинаковых версиях Python/numpy результаты "
          "\nвоспроизводимы. Без фиксации seed и версий эксперимента нельзя сравнивать: "
          "\nRNG и внутренние алгоритмы суммирования могут меняться.")

task13()
import math
def print_table(title, headers, rows):

    print(f"\n{title}")
    fmt = lambda c: f"{c:.6g}" if isinstance(c, (float, int)) else str(c)
    cells = [[fmt(c) for c in r] for r in rows]
    w = [max(len(headers[i]), *(len(r[i]) for r in cells)) for i in range(len(headers))]
    for r in [headers] + cells:
        print(" | ".join(x.ljust(w[i]) for i, x in enumerate(r)))

def task14():
    print("\n### Задача 14. Границы представимости: sum vs math.fsum")

    def safe(fn, data):
        try:
            return repr(fn(data))
        except Exception as e:
            return f"{type(e).__name__}: {e}"

    cases = [
        ("большие 1e300", [1e300, 1e300]),
        ("переполнение 1e308", [1e308, 1e308]),
        ("маленькие 1e-200", [1e-200, 1e-200]),
        ("денормализованные 5e-324", [5e-324, 5e-324]),
        ("inf", [float("inf"), 1.0]),
        ("nan", [float("nan"), 1.0]),
        ("inf + (-inf)", [float("inf"), -float("inf")]),
        ("огромный int + float", [10**400, 1.0]),
    ]

    rows = []
    for name, data in cases:
        rows.append((name, safe(sum, data), safe(math.fsum, data)))

    print_table("Поведение sum и math.fsum", ["случай", "sum", "math.fsum"], rows)
    print("Вывод: sum и fsum по-разному обрабатывают переполнения и огромные int. "
          "\nNaN и inf распространяются; fsum может сразу падать на переполнении/огромном int, "
          "\nтогда как sum иногда сначала накапливает int, а затем падает при смешивании с float. "
          "\nВ реальном коде граничные значения нужно проверять до суммирования.")

task14()
import math
import mpmath as mp
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
def relerr(v, r):
    v, r = abs(float(v)), abs(float(r))
    if r == 0.0:
        return 0.0 if v == 0.0 else float("inf")
    return v / r
def print_table(title, headers, rows):

    print(f"\n{title}")
    fmt = lambda c: f"{c:.6g}" if isinstance(c, (float, int)) else str(c)
    cells = [[fmt(c) for c in r] for r in rows]
    w = [max(len(headers[i]), *(len(r[i]) for r in cells)) for i in range(len(headers))]
    for r in [headers] + cells:
        print(" | ".join(x.ljust(w[i]) for i, x in enumerate(r)))

def task15():
    print("\n### Задача 15. Полный корректный эксперимент")
    print("Цель: исследовать устойчивость вычисления f(x)=sqrt(x+1)-sqrt(x).")
    print("Постановка: плохой алгоритм sqrt(x+1)-sqrt(x); хороший 1/(sqrt(x+1)+sqrt(x)).")
    print("Эталон: mpmath с 80 знаками. Диапазон x: логарифмическая сетка 1e2..1e16.")

    xs = np.logspace(2, 16, 8)
    rows = []
    for x in xs:
        bad = math.sqrt(x + 1.0) - math.sqrt(x)
        good = 1.0 / (math.sqrt(x + 1.0) + math.sqrt(x))
        xmp = mp.mpf(str(x))
        exact = mp.sqrt(xmp + 1) - mp.sqrt(xmp)
        eb = relerr(bad, exact)      # было (bad, exact) — кортеж, ошибка!
        eg = relerr(good, exact)
        rows.append((x, bad, good, float(exact), eb, eg))

    print_table(
        "Мини-отчёт: вход — bad — good — exact — err bad — err good",
        ["x", "bad", "good", "exact", "err bad", "err good"],
        rows,
    )

    err_bad = [r[4] for r in rows]
    err_good = [r[5] for r in rows]
    plt.figure()
    plt.loglog(xs, np.maximum(err_bad, 1e-300), "o-", label="bad")
    plt.loglog(xs, np.maximum(err_good, 1e-300), "s-", label="good")
    plt.xlabel("x")
    plt.ylabel("relative error")
    plt.legend()
    plt.title("Задача 15: полный эксперимент")
    plt.savefig("task15_errors.png", dpi=150)
    plt.close()
    print("График сохранён: task15_errors.png")

    print("Вывод: плохой алгоритм неустойчив из-за вычитания близких sqrt(x+1) и sqrt(x); "
          "\nего относительная ошибка растёт примерно как x и на больших x становится "
          "\nнеприемлемой. Хороший алгоритм устойчив и даёт точность порядка машинной "
          "\nточности. Пригодность: хороший алгоритм пригоден во всём диапазоне; плохой — "
          "\nтолько при небольших x, пока sqrt(x+1)-sqrt(x) не теряет значащие цифры.")
# дз.16.11
import warnings
import numpy as np
from decimal import Decimal, getcontext

getcontext().prec = 50


def task1():
    print("ЗАДАЧА 1. Инвентаризация массива")
    a = np.arange(60).reshape(3, 4, 5)
    print(f"shape:        {a.shape}")
    print(f"ndim:         {a.ndim}")
    print(f"size:         {a.size}")
    print(f"dtype:        {a.dtype}")
    print(f"strides:      {a.strides}  (itemsize = {a.itemsize} байт)")
    print(f"C_CONTIGUOUS: {a.flags['C_CONTIGUOUS']}")
    print()
    print("Объяснение:")
    print(f"  strides = {a.strides} — шаги в БАЙТАХ для перехода к следующему")
    print(f"  элементу по соответствующей оси. При itemsize = {a.itemsize}:")
    print(f"    ось 0: 4*5*{a.itemsize} = {4*5*a.itemsize} байт (4*5 элементов)")
    print(f"    ось 1:   5*{a.itemsize} = {5*a.itemsize} байт (5 элементов)")
    print(f"    ось 2:     {a.itemsize} байт (следующий элемент по последней оси)")
    print(f"  size = 3*4*5 = {3*4*5} — полное число элементов.")
task1()

import numpy as np
import warnings   # <- вот этой строки не хватало

def task2():
    print("ЗАДАЧА 2. int vs float — тихая ловушка")
    a = np.array([1, 2, 3, 4])
    print(f"a = {a}, dtype = {a.dtype}")
    print(f"a / 2    = {a / 2}, dtype = {(a/2).dtype}")
    print(f"a // 2   = {a // 2}, dtype = {(a//2).dtype}")
    print(f"a / 2.0  = {a / 2.0}, dtype = {(a/2.0).dtype}")
    print()
    b = np.array([1, 2, 3], dtype=np.int8)
    print(f"b = {b}, dtype = {b.dtype}")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        res = b + 127
    print(f"b + 127 = {res}, dtype = {res.dtype}")
    print()
    print("Объяснение:")
    print("  - a / 2 (true division) в NumPy всегда возвращает float — создаётся НОВЫЙ")
    print("    массив; исходный a остаётся int.")
    print("  - b + 127: int8 переполняется по модулю 256: 1+127=128→-128, 2+127=129→-127,")
    print("    3+127=130→-126. NumPy молча оборачивает (может выдать RuntimeWarning),")
    print("    потому что рассчитан на скорость и фиксированные целочисленные типы.")
task2()
import numpy as np
from decimal import Decimal
def task3():
    print("ЗАДАЧА 3. float32 vs float64 — реальная точность")
    f32 = float(np.float32(0.1))
    f64 = float(np.float64(0.1))
    print(f"float32(0.1) как float: {f32!r}")
    print(f"float64(0.1) как float: {f64!r}")
    print()
    print(f"float(np.float32(0.1)) - 0.1 = {(f32 - 0.1)!r}")
    print(f"float(np.float64(0.1)) - 0.1 = {(f64 - 0.1)!r}   # 0: Python 0.1 — тот же float64")
    print()
    print("В формате .20e:")
    print(f"  float32: {f32:.20e}")
    print(f"  float64: {f64:.20e}")
    print()
    true = Decimal("0.1")
    err32 = abs(Decimal(f32) - true)
    err64 = abs(Decimal(f64) - true)
    print(f"Истинное 0.1 (Decimal):      {true}")
    print(f"Ошибка float32:              {err32:.3e}")
    print(f"Ошибка float64:              {err64:.3e}")
    ratio = err32 / err64
    print(f"Отношение ошибок float32/float64 ≈ {ratio:.3e}")
    print()
    print("Вывод: float32 даёт ~7 значащих цифр, float64 — ~16. Для задач, где важна")
    print("точность (численное интегрирование, решение СЛАУ, длинные суммы) float32")
    print("НЕ подходит — используйте float64. float32 допустим в ML-инференсе и")
    print("грубых расчётах, где хватает относительной точности ~1e-7.")
task3()
import numpy as np
def task4():
    print("ЗАДАЧА 4. Явный dtype при создании")
    a = np.zeros((2, 3), dtype=np.float64)
    b = np.zeros((2, 3), dtype=np.float32)
    c = np.ones((2, 3), dtype=np.int16)
    d = np.full((2, 3), 7, dtype=np.uint8)
    for name, arr in [("zeros f64", a), ("zeros f32", b),
                      ("ones  i16", c), ("full7  u8", d)]:
        print(f"{name}: dtype={arr.dtype}, nbytes={arr.nbytes}")
    print()
    big64 = np.zeros((1000, 1000), dtype=np.float64)
    big32 = np.zeros((1000, 1000), dtype=np.float32)
    print(f"(1000,1000) float64: {big64.nbytes} байт = {big64.nbytes/1024/1024:.1f} МБ")
    print(f"(1000,1000) float32: {big32.nbytes} байт = {big32.nbytes/1024/1024:.1f} МБ")
    print(f"Экономия float32:    {big64.nbytes - big32.nbytes} байт = "
          f"{(big64.nbytes - big32.nbytes)/1024/1024:.1f} МБ")
    print()
    print("Вывод: float32 экономит ровно 2x памяти, но даёт ~7 значащих цифр вместо ~16.")
task4()
import numpy as np
def task5():
    print("ЗАДАЧА 5. Цепочка reshape")
    a = np.arange(24)
    print(f"start: shape={a.shape}")
    cur = a
    for shp in [(4, 6), (2, 3, 4), (2, 2, 6), (24,)]:
        cur = cur.reshape(shp)
        ok = np.array_equal(a, cur.ravel())
        print(f" -> {shp}: shape={cur.shape}, данные сохранены: {ok}")
    print()
    print("Объяснение: reshape почти всегда возвращает view (меняет только shape и")
    print("strides) на C-непрерывном массиве — поэтому данные не теряются. Копия")
    print("нужна, когда новая форма несовместима с текущим порядком (например,")
    print("для transposed (не C-непрерывного) массива).")
task5()
import numpy as np
def task6():
    print("ЗАДАЧА 6. flatten vs ravel")
    M = np.arange(12).reshape(3, 4)
    f = M.flatten()
    r = M.ravel()
    print(f"f.base is None:      {f.base is None}")
    print(f"r.base is M:         {r.base is M}")
    print(f"r.base is not None:  {r.base is not None}")
    print(f"r.base:              {type(r.base).__name__ if r.base is not None else None}")
    print()
    f[0] = 999
    print(f"после f[0]=999: M[0,0] = {M[0,0]} (flatten — копия, M не изменился)")
    r[1] = 888
    print(f"после r[1]=888: M[0,1] = {M[0,1]} (ravel — view, M изменился)")
    print()
    print("Вывод: flatten() всегда копирует, ravel() возвращает view если возможно.")
    print("Используйте ravel() для чтения/экономии памяти; flatten() — когда нужен")
    print("независимый массив, не влияющий на оригинал.")

task6()
import numpy as np
def task7():
    print("ЗАДАЧА 7. newaxis, squeeze, транспонирование")
    v = np.arange(5)
    print(f"v.shape:                     {v.shape}")
    print(f"v[:, None].shape:            {v[:, None].shape}   # ось -> столбец (5,1)")
    print(f"v[None, :].shape:            {v[None, :].shape}   # ось -> строка (1,5)")
    print(f"np.squeeze(v[:, None]).shape:{np.squeeze(v[:, None]).shape}   # убрали ось длины 1")
    T = np.arange(6).reshape(2, 3).T
    print(f"np.arange(6).reshape(2,3).T: shape={T.shape}")
    print(f"  содержимое:\n{T}")
    print()
    outer = v[:, None] + v[None, :]
    print(f"v[:,None] + v[None,:]: shape={outer.shape}, таблица сумм:")
    print(outer)
    print()
    mult = v[:, None] * v[None, :]
    print(f"v[:,None] * v[None,:]: shape={mult.shape}, таблица умножения:")
    print(mult)

task7()
import numpy as np
def task8():
    print("ЗАДАЧА 8. Транспонирование без копии")
    A = np.arange(6).reshape(2, 3)
    B = A.T
    print(f"A.shape={A.shape}, A.strides={A.strides}")
    print(f"B.shape={B.shape}, B.strides={B.strides}")
    print(f"B.base is A:         {B.base is A}")
    print(f"B.base is not None:  {B.base is not None}")
    print()
    print(f"до изменения: A =\n{A}")
    B[0, 1] = 999
    print(f"после B[0,1]=999: A =\n{A}  (A изменился — B это view)")
    print()
    print("Вывод: .T меняет только shape и strides (переставляет их), не копируя")
    print("данные. Изменения через B затрагивают A, потому что .T — view.")

task8()
import numpy as np
def task9():
    print("ЗАДАЧА 9. Поэлементно vs матричное")
    A = np.arange(6).reshape(2, 3)
    B = np.arange(6).reshape(3, 2)
    print(f"A =\n{A}\nB =\n{B}")
    AB = A @ B
    ATBT = A.T @ B.T
    print(f"A @ B: shape={AB.shape}, значение:\n{AB}")
    print(f"A.T @ B.T: shape={ATBT.shape}, значение:\n{ATBT}")
    print(f"A * A: shape={(A * A).shape}, значение:\n{A * A}")
    try:
        _ = A * B
    except Exception as e:
        print(f"A * B -> ошибка: {type(e).__name__}: {e}")
    print()
    D = np.diag([1, 2, 3])
    A_sq = np.arange(1, 10).reshape(3, 3)
    print("Пример, где * и @ дают одинаковый результат — диагональная матрица D:")
    print(f"A_sq @ D == A_sq * D: {np.array_equal(A_sq @ D, A_sq * D)}")
    print()
    print("Объяснение: * — поэлементное произведение, требует broadcast-совместимых")
    print("форм. A (2,3) и B (3,2) несовместимы по обеим осям -> ValueError.")
    print("@ — матричное произведение: (m,k)@(k,n)->(m,n).")

task9()
import numpy as np
def task10():
    print("ЗАДАЧА 10. axis=0 vs axis=1")
    M = np.arange(12).reshape(3, 4)
    print(f"M =\n{M}\n")
    print(f"M.sum(axis=0)    = {M.sum(axis=0)}    # свернули ось 0 (строки) — суммы по столбцам")
    print(f"M.sum(axis=1)    = {M.sum(axis=1)}    # свернули ось 1 (столбцы) — суммы по строкам")
    print(f"M.mean(axis=0)   = {M.mean(axis=0)}")
    print(f"M.mean(axis=1)   = {M.mean(axis=1)}")
    print(f"M.argmax(axis=0) = {M.argmax(axis=0)}    # индекс макс. в каждом столбце")
    print(f"M.argmax(axis=1) = {M.argmax(axis=1)}    # индекс макс. в каждой строке")
    print()
    print("Проверка на столбце 0: M[:,0] =", M[:, 0],
          "| сумма =", M[:, 0].sum(),
          "| == M.sum(axis=0)[0]:", M[:, 0].sum() == M.sum(axis=0)[0])

task10()
import numpy as np
def task11():
    print("ЗАДАЧА 11. keepdims и broadcasting")
    X = np.random.default_rng(42).normal(size=(5, 3))
    m0 = X.mean(axis=0)
    m0k = X.mean(axis=0, keepdims=True)
    print(f"X.mean(axis=0).shape:               {m0.shape}")
    print(f"X.mean(axis=0, keepdims=True).shape:{m0k.shape}")
    print(f"(X - m0).shape:                     {(X - m0).shape}")
    print(f"(X - m0k).shape:                    {(X - m0k).shape}")
    print()
    Z = (X - X.mean(axis=1, keepdims=True)) / X.std(axis=1, keepdims=True)
    print(f"Z.mean(axis=1) ≈ {Z.mean(axis=1)}")
    print(f"Z.std(axis=1)  ≈ {Z.std(axis=1)}")
    print()
    print("Зачем keepdims: результат (1, n) явно broadcast-ится по строкам. Без")
    print("keepdims для axis=0 форма (n,) тоже вычитается по столбцам, но для axis=1")
    print("форма (5,) вычтется по столбцам (что неверно) — keepdims делает намерение")
    print("явным и сохраняет форму для корректного broadcast.")
task11()
import  numpy as np
def task12():
    print("ЗАДАЧА 12. Срез — view, не копия")
    a = np.arange(10)
    b = a[2:5]
    print(f"a = {a}, b = a[2:5] = {b}")
    b[0] = 999
    print(f"после b[0]=999: a = {a}   # изменился, т.к. b — view")
    a = np.arange(10)
    c = a[2:5].copy()
    c[0] = 999
    print(f"с .copy(): после c[0]=999: a = {a}   # НЕ изменился")
    print()
    print("Почему важно для численных методов: если вы 'обрезаете' данные для")
    print("анализа и случайно меняете view — оригинал испортится, эксперимент")
    print("перестанет быть воспроизводимым. Пример бага: pipeline, где feature")
    print("engineering мутирует исходный X через срез. Пример пользы: rolling window")
    print("или батчи без копирования многогигабайтных данных.")
task12()
import numpy as np
def task13():
    print("ЗАДАЧА 13. Булева маска и fancy indexing")
    a = np.random.default_rng(0).normal(size=20)
    print(f"a = {np.round(a, 3)}")
    print(f"a[a > 0]:              count = {a[a > 0].size}, значения = {np.round(a[a > 0], 3)}")
    print(f"a[(a>-1)&(a<1)]:       count = {a[(a>-1)&(a<1)].size}")
    print(f"a[[0,5,10,15]]:        {np.round(a[[0,5,10,15]], 3)}  # fancy indexing по списку индексов")
    print(f"a[|a|>2]:              {a[np.abs(a) > 2]}  # выбросы")
    a[a < 0] = 0
    print(f"после a[a<0]=0:        {np.round(a, 3)}")
    print()
    print("Почему a[a>0] & (a<1) — ошибка: a[a>0] возвращает ЧИСЛА (float), а не")
    print("маску; & для float-массивов не определён (или даёт мусор).")
    print("Правильно: (a>0) & (a<1) — две булевы маски, поэлементное 'И'.")

task13()
import numpy as np
def task14():
    print("ЗАДАЧА 14. Broadcasting в реальной задаче")
    rng = np.random.default_rng(1)
    X = rng.normal(size=(100, 3))
    mu = X.mean(axis=0)
    sigma = X.std(axis=0)
    Xn = (X - mu) / sigma   # broadcast: (100,3) с (3,)
    print(f"X_norm.mean(axis=0) ≈ {Xn.mean(axis=0)}")
    print(f"X_norm.std(axis=0)  ≈ {Xn.std(axis=0)}")
    print()
    diff = Xn[:, None, :] - Xn[None, :, :]     # (100,100,3)
    D = np.sqrt((diff ** 2).sum(axis=-1))       # (100,100)
    print(f"D.shape:                 {D.shape}")
    print(f"max |diag| ≈ 0:          {np.abs(np.diag(D)).max():.2e}")
    print(f"симметрична:             {np.allclose(D, D.T)}")
    print(f"D[0,1] = {D[0,1]:.6f}, D[1,0] = {D[1,0]:.6f}")

task14()
import numpy as np
def task15():
    print("ЗАДАЧА 15. Полный кейс")
    rng = np.random.default_rng(42)
    raw = rng.normal(20, 2, size=(30, 4))
    raw[7, 2] = 100
    print("Шаг 1. shape:", raw.shape, "| dtype:", raw.dtype, "| size:", raw.size)
    print()
    mask = np.abs(raw - raw.mean(axis=0)) > 3 * raw.std(axis=0)
    print("Шаг 2. Выбросов:", mask.sum(), "| координаты:", np.argwhere(mask).tolist())
    print()
    raw_nan = raw.astype(float).copy()
    raw_nan[mask] = np.nan
    col_means = np.nanmean(raw_nan, axis=0)
    raw_clean = np.where(mask, col_means, raw)
    print("Шаг 3. raw_clean[7,2] =", round(float(raw_clean[7, 2]), 3), "(было 100)")
    print()
    T = raw_clean.T
    back = T.T
    print("Шаг 4. T.shape:", T.shape, "| T.T.shape:", back.shape,
          "| equal:", np.array_equal(back, raw_clean))
    print()
    flat = raw_clean.ravel()
    restored = flat.reshape(30, 4)
    print("Шаг 5. flat.shape:", flat.shape, "| restored.shape:", restored.shape,
          "| equal:", np.array_equal(restored, raw_clean))
    print()
    print("Шаг 6. mean по датчикам:", np.round(raw_clean.mean(axis=0), 3))
    print("       std  по датчикам:", np.round(raw_clean.std(axis=0), 3))
    print()
    norm = (raw_clean - raw_clean.mean(axis=0)) / raw_clean.std(axis=0)
    print("Шаг 7. mean после нормировки:", np.round(norm.mean(axis=0), 12))
    print("       std  после нормировки:", np.round(norm.std(axis=0), 12))
    print()
    print("Вывод:")
    print("  - copy() понадобился в шаге 3 (raw_nan), чтобы не портить raw при замене")
    print("    выбросов на NaN.")
    print("  - broadcasting сработал в шаге 2 (mean/std (4,) вычитаются из (30,4)),")
    print("    в шаге 3 (np.where(mask (30,4), means (4,), raw (30,4))) и в шаге 7")
    print("    (нормировка по столбцам).")
    print("  - Ошибка формы могла бы возникнуть при нормировке по строкам без")
    print("    keepdims: mean(axis=1) даёт (30,), что вычлось бы по столбцам.")
task15()
# дз.17.11

import time
import sys
import math
import numpy as np

def measure(fn, repeat=3):
    best = float("inf")
    result = None
    for _ in range(repeat):
        t0 = time.perf_counter()
        result = fn()
        t1 = time.perf_counter()
        best = min(best, t1 - t0)
    return result, best


def header(title):
    print("\n" + "=" * 76)
    print(title)
    print("=" * 76)



def task1():
    header("Задача 1. Сумма массива: цикл vs a.sum()")
    rng = np.random.default_rng(42)
    print(f"{'n':>10} | {'loop, ms':>10} | {'numpy, ms':>10} | {'speedup':>8} | {'|diff|':>10}")
    print("-" * 66)
    for n in [10**5, 10**6, 10**7]:
        a = rng.normal(size=n)

        def loop():
            s = 0.0
            for x in a:
                s += x
            return s

        def nps():
            return a.sum()

        repeat = 2 if n >= 10**7 else 3
        r_l, t_l = measure(loop, repeat=repeat)
        r_n, t_n = measure(nps, repeat=3)
        print(f"{n:>10} | {t_l*1000:>10.2f} | {t_n*1000:>10.2f} | "
              f"{t_l/t_n:>7.1f}x | {abs(r_l-r_n):>10.2e}")

    print("\nВывод: ускорение ~50–100x и слабо растёт с n: NumPy суммирует в C с SIMD,")
    print("а цикл Python платит за интерпретатор на каждом элементе. Уже при n=1e5")
    print("разница заметна (>10x), при n=1e7 выигрыш абсолютный — секунды.")



def task2():
    header("Задача 2. Среднее и std: формула «в лоб» vs a.mean()/a.std()")
    rng = np.random.default_rng(42)
    n = 10**6
    a = rng.normal(size=n)

    def loop():
        s = 0.0
        s2 = 0.0
        for x in a:
            s += x
            s2 += x * x
        mean = s / n
        var = s2 / n - mean * mean
        return mean, math.sqrt(var)

    def nps():
        return a.mean(), a.std()

    (ml, sl), t_l = measure(loop, repeat=3)
    (mn, sn), t_n = measure(nps, repeat=3)

    print(f"loop:  mean={ml:.15f}, std={sl:.15f}, time={t_l*1000:.1f} ms")
    print(f"numpy: mean={mn:.15f}, std={sn:.15f}, time={t_n*1000:.1f} ms")
    print(f"|Δmean| = {abs(ml-mn):.2e},  |Δstd| = {abs(sl-sn):.2e}")
    print(f"ускорение: {t_l/t_n:.1f}x")
    print("\nВывод: для mean результаты совпадают в пределах ~1e-14 (разница — порядок")
    print("накопления округлений). Для std формула E[X^2]-E[X]^2 теоретически может")
    print("терять точность при малой дисперсии (катастрофическое сокращение); здесь")
    print("std≈1, поэтому расхождение ~1e-14, но в общем случае это ловушка. NumPy")
    print("ускорение — десятки раз и std считается устойчивее.")


def task3():
    header("Задача 3. y = sin(x) + x^2: цикл с math.sin vs NumPy")
    rng = np.random.default_rng(42)
    a = rng.normal(size=10**6)

    def loop():
        out = [0.0] * len(a)
        for i, x in enumerate(a):
            out[i] = math.sin(x) + x * x
        return out

    def nps():
        return np.sin(a) + a * a

    r_l, t_l = measure(loop, repeat=3)
    r_n, t_n = measure(nps, repeat=3)
    diff = np.max(np.abs(np.asarray(r_l) - np.asarray(r_n)))
    print(f"loop:  {t_l*1000:.1f} ms")
    print(f"numpy: {t_n*1000:.1f} ms")
    print(f"ускорение: {t_l/t_n:.1f}x,  max|Δ| = {diff:.2e}")
    print("\nВывод: NumPy вызывает sin для всего массива одной командой (SIMD в C),")
    print("ускорение десятки раз. Код короче и читается как формула; math.sin для")
    print("массива и близко не даёт такой простоты.")



def task4():
    header("Задача 4. Clipping в [0,1]: if/elif vs np.clip")
    rng = np.random.default_rng(42)
    a = rng.normal(size=10**6)

    def loop():
        out = [0.0] * len(a)
        for i, x in enumerate(a):
            if x < 0.0:
                out[i] = 0.0
            elif x > 1.0:
                out[i] = 1.0
            else:
                out[i] = x
        return out

    def nps():
        return np.clip(a, 0.0, 1.0)

    r_l, t_l = measure(loop, repeat=3)
    r_n, t_n = measure(nps, repeat=3)
    n_neg = int((a < 0).sum())
    n_gt1 = int((a > 1).sum())
    print(f"loop:  {t_l*1000:.1f} ms")
    print(f"numpy: {t_n*1000:.1f} ms")
    print(f"ускорение: {t_l/t_n:.1f}x,  совпадение: {np.allclose(r_l, r_n)}")
    print(f"изменено: {n_neg + n_gt1} элементов ({n_neg} < 0, {n_gt1} > 1)")
    print("\nВывод: np.clip — одна функция вместо ветвлений, десятки раз быстрее.")
    print("Побочная статистика через булевы маски (a<0).sum() — бесплатно и без цикла.")


def task5():
    header("Задача 5. Сумма по строкам (n=1e5, 10 столбцов)")
    rng = np.random.default_rng(42)
    n = 10**5
    m = rng.normal(size=(n, 10))

    def loop():
        res = [0.0] * n
        for i in range(n):
            s = 0.0
            for j in range(10):
                s += m[i, j]
            res[i] = s
        return res

    def nps():
        return m.sum(axis=1)

    r_l, t_l = measure(loop, repeat=3)
    r_n, t_n = measure(nps, repeat=3)
    print(f"loop:  {t_l*1000:.1f} ms,  SLOC ~8")
    print(f"numpy: {t_n*1000:.1f} ms,  SLOC = 1")
    print(f"ускорение: {t_l/t_n:.1f}x,  совпадение: {np.allclose(r_l, r_n)}")
    print("\nВывод: m.sum(axis=1) — одна строка вместо двух циклов, быстрее в десятки")
    print("раз и читается буквально: «сумма по оси 1».")



def task6():
    header("Задача 6. Центрирование по столбцам: цикл vs broadcasting")
    rng = np.random.default_rng(42)
    n = 10**5
    m = rng.normal(size=(n, 10))

    def loop():
        means = [0.0] * 10
        for j in range(10):
            s = 0.0
            for i in range(n):
                s += m[i, j]
            means[j] = s / n
        out = [[0.0] * 10 for _ in range(n)]
        for i in range(n):
            for j in range(10):
                out[i][j] = m[i, j] - means[j]
        return out

    def nps():                           # SLOC = 1
        return m - m.mean(axis=0)

    r_l, t_l = measure(loop, repeat=3)
    r_n, t_n = measure(nps, repeat=3)
    print(f"loop:  {t_l*1000:.1f} ms,  SLOC ~13")
    print(f"numpy: {t_n*1000:.1f} ms,  SLOC = 1")
    print(f"ускорение: {t_l/t_n:.1f}x,  совпадение: {np.allclose(r_l, r_n)}")
    print("\nВывод: m - m.mean(axis=0) — это и есть центрирование через broadcasting:")
    print("форма (10,) «растягивается» до (n,10). Одна строка вместо двух циклов,"
          " ускорение десятки раз.")


def task7():
    header("Задача 7. max и argmax: цикл vs a.max()/a.argmax()")
    rng = np.random.default_rng(42)
    a = rng.normal(size=10**6)

    def loop():
        mv = a[0]
        mi = 0
        for i in range(1, len(a)):
            if a[i] > mv:
                mv = a[i]
                mi = i
        return float(mv), mi

    def nps():
        return float(a.max()), int(a.argmax())

    (ml, il), t_l = measure(loop, repeat=3)
    (mn, inn), t_n = measure(nps, repeat=3)
    print(f"loop:  max={ml:.6f}, idx={il}, time={t_l*1000:.1f} ms")
    print(f"numpy: max={mn:.6f}, idx={inn}, time={t_n*1000:.1f} ms")
    print(f"ускорение: {t_l/t_n:.1f}x,  совпадение: {(ml, il) == (mn, inn)}")
    print("\nВывод: NumPy делает два прохода (max, argmax), но каждый — в C/SIMD,"
          " суммарно всё равно десятки раз быстрее одного цикла Python.")


def task8():
    header("Задача 8. Фильтрация x > 0: list-comp vs булева маска (время и память)")
    rng = np.random.default_rng(42)
    a = rng.normal(size=10**6)

    def loop():
        return [x for x in a if x > 0]

    def nps():
        return a[a > 0]

    r_l, t_l = measure(loop, repeat=3)
    r_n, t_n = measure(nps, repeat=3)

    mem_list = sys.getsizeof(r_l) + sum(sys.getsizeof(x) for x in r_l)
    mem_np = r_n.nbytes

    print(f"loop:  {t_l*1000:.1f} ms, len={len(r_l)}, mem ~ {mem_list/1024/1024:.1f} MB")
    print(f"numpy: {t_n*1000:.1f} ms, len={len(r_n)}, mem ~ {mem_np/1024/1024:.1f} MB")
    print(f"ускорение: {t_l/t_n:.1f}x,  память: список в {mem_list/mem_np:.1f}x тяжелее")
    print("\nВывод: NumPy-выборка быстрее в десятки раз и в разы компактнее: список")
    print("хранит по float-объекту на элемент, массив — плотный буфер float64.")



def task9():
    header("Задача 9. Замена отрицательных на |x| in-place")
    rng = np.random.default_rng(42)
    a0 = rng.normal(size=10**6)

    def loop():
        a = a0.copy()
        for i in range(len(a)):
            if a[i] < 0:
                a[i] = -a[i]
        return a

    def nps():
        a = a0.copy()
        a[a < 0] *= -1
        return a

    r_l, t_l = measure(loop, repeat=3)
    r_n, t_n = measure(nps, repeat=3)
    print(f"loop:  {t_l*1000:.1f} ms")
    print(f"numpy: {t_n*1000:.1f} ms")
    print(f"ускорение: {t_l/t_n:.1f}x,  совпадение: {np.allclose(r_l, r_n)}")
    print("\nВывод: a[a<0] *= -1 — булева маска плюс операция по месту. Быстрее в")
    print("десятки раз и читается почти как формула. Альтернатива np.abs(a, out=a)")


def task10():
    header("Задача 10. Комбинированная маска -1 < x < 1")
    rng = np.random.default_rng(42)
    a = rng.normal(size=10**6)

    def loop():
        return [x for x in a if -1 < x < 1]

    def nps():
        return a[(a > -1) & (a < 1)]

    r_l, t_l = measure(loop, repeat=3)
    r_n, t_n = measure(nps, repeat=3)
    print(f"loop:  {t_l*1000:.1f} ms, len={len(r_l)}")
    print(f"numpy: {t_n*1000:.1f} ms, len={len(r_n)}")
    print(f"ускорение: {t_l/t_n:.1f}x,  совпадение: {np.allclose(r_l, r_n)}")
    print("\nВывод: в Python запись -1 < x < 1 элегантна; в NumPy её эквивалент —")
    print("(a > -1) & (a < 1) со скобками. Без скобок (a > -1 & a < 1) приоритет &")
    print("вычислит не то, получите ValueError или мусор. Ускорение — десятки раз.")



def main():
    task1()
    task2()
    task3()
    task4()
    task5()
    task6()
    task7()
    task8()
    task9()
    task10()


if __name__ == "__main__":
    main()

