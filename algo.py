import math
import numpy as np


def f(x, y):
    return y - math.tan(x)


def g(x, y):
    return x * y - 1.5


def stri(x1, y1, x2, y2, x3, y3):
    return 0.5 * abs((x2 - x1) * (y3 - y1) * (x3 - x1) * (y2 - y1))


def initial_point_choice(xm, ym, xp, yp, area):
    dl = 0.1
    cur_min = 1_000_000
    point = [0, 0]
    x = xm
    y = ym
    while cur_min > 999_999:
        for x in np.arange(xm, xp, 0.1):
            for y in np.arange(ym, yp, 0.1):
                fc = f(x, y)
                gc = g(x, y)
                if area == 1:
                    if fc <= 0 or gc <= 0:
                        continue
                if area == 2:
                    if fc >= 0 or gc >= 0:
                        continue
                if area == 3:
                    if fc <= 0 or gc >= 0:
                        continue
                if area == 4:
                    if fc >= 0 or gc <= 0:
                        continue
                dv = abs(fc) + abs(gc)
                if dv > cur_min:
                    continue
                x0 = x
                y0 = y
                point[0] = x0
                point[1] = y0
                cur_min = dv
        if cur_min < 999_999:
            break
        dl = dl / 2
    return point


# x0 = 0
# y0 = 0
# x1 = 0
# y1 = 0
# x2 = 0
# y2 = 0


def two_dimensional_linear_interpolation(x0, y0, x1, y1, x2, y2):
    x = 10
    y = 10
    xls = 1_000_000
    yls = 1_000_000
    dv = abs(x - xls) + abs(y - yls)
    while dv > 0.000005:
        zf0 = f(x0, y0)
        zg0 = g(x0, y0)
        zf1 = f(x1, y1)
        zg1 = g(x1, y1)
        zf2 = f(x2, y2)
        zg2 = g(x2, y2)

        af = (y1 - y0) * (zf2 - zf0) - (y2 - y0) * (zf1 - zf0)
        bf = (x2 - x0) * (zf1 - zf0) - (x1 - x0) * (zf2 - zf0)
        cf = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
        df = -x0 * af - y0 * bf - zf0 * cf

        ag = (y1 - y0) * (zg2 - zg0) - (y2 - y0) * (zg1 - zg0)
        bg = (x2 - x0) * (zg1 - zg0) - (x1 - x0) * (zg2 - zg0)
        cg = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
        dg = -x0 * ag - y0 * bg - zg0 * cg

        dt = af * bg - ag * bf
        if abs(dt) < 0.000001:
            break
        x = (-df * bg + dg * bf) / dt
        y = (-af * dg + ag * df) / dt

        zfc = f(x, y)
        zgc = g(x, y)

        dv = abs(x - xls) + abs(y - yls)

        xls = x
        yls = y

        s0 = stri(x1, y1, x2, y2, x, y)
        s1 = stri(x0, y0, x2, y2, x, y)
        s2 = stri(x0, y0, x1, x2, x, y)

        if s0 >= s1 and s0 >= s2:
            x0 = x1
            y0 = y1
            x1 = x2
            y1 = y2
            x2 = x
            y2 = y
            continue
        if s1 >= s0 and s1 >= s2:
            x1 = x2
            y1 = y2
            x2 = x
            y2 = y
            continue
        if s2 >= s0 and s2 >= s1:
            x2 = x
            y2 = y
            continue


def min_values_f_and_g():
    val0 = abs(f(x0, y0)) + abs(g(x0, y0))
    val1 = abs(f(x1, y1)) + abs(g(x1, y1))
    val2 = abs(f(x2, y2)) + abs(g(x2, y2))

    if val0 < val1 and val0 < val2:
        return [x0, y0]
    if val1 < val2:
        return [x1, y1]
    else:
        return [x2, y2]

if __name__ == "__main__":
    xp0 = 0
    xp1 = 0
    xp2 = math.pi / 2
    xp3 = math.pi / 2

    yp1 = 0
    yp2 = 5
    yp3 = 5
    yp4 = 0

    point1 = initial_point_choice(xp0, yp1, xp2, yp3, 1)
    point2 = initial_point_choice(xp0, yp1, xp2, yp3, 2)
    point3 = initial_point_choice(xp0, yp1, xp2, yp3, 3)
    x0 = point1[0]
    y0 = point1[1]
    x1 = point1[0]
    y1 = point1[1]
    x2 = point1[0]
    y2 = point1[1]

    for i in range(5):
        two_dimensional_linear_interpolation(x0, y0, x1, y1, x2, y2)
        point = min_values_f_and_g()
        print(f'x: {point[0]}, y: {point[1]}, f(x,y): {f(point[0], point[1])}, g(x,y): {g(point[0], point[1])}')
