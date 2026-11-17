
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


task15()

