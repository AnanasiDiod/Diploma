import numpy as np
from constants import *

#вводятся координаты четырёх точек, после чего производится их исследование на пересечение путём векторного перемножения.
#возвращает True, если пересечение есть.
def intersection_2d(a1 = [0, 0, 0], a2 = [0, 0, 0], b1 = [0, 0, 0], b2 = [0, 0, 0]):
    va1 = np.array(a1, dtype=np.float64)
    va2 = np.array(a2, dtype=np.float64)
    vb1 = np.array(b1, dtype=np.float64)
    vb2 = np.array(b2, dtype=np.float64)
    return np.cross(vb1-va1, vb2-va1)[2] * np.cross(vb1-va2, vb2-va2)[2] <= 0 and np.cross(va1-vb1, va2-vb1)[2] * np.cross(va1-vb2, va2-vb2)[2] <= 0


#вводятся координаты точки наблюдения, затем координаты светящей лампы, затем - закрывающей.
#возвращает список точек и коэффициенты их прохождения
def intersect_lamp(x = (0, 0, 0), l_shi = (0, 0, 0, 0), l_bor = (0, 0, 0, 0)):
    center = (intersection_2d(x, [l_shi[0], l_shi[1], 0], [l_bor[0] - l_bor[2], l_bor[1], 0], [l_bor[0] + l_bor[2], l_bor[1], 0]) or
                intersection_2d(x, [l_shi[0], l_shi[1], 0], [l_bor[0], l_bor[1] - l_bor[2], 0], [l_bor[0], l_bor[1] + l_bor[2], 0]))
    right = int(intersection_2d(x, [l_shi[0] + l_shi[2], l_shi[1], 0], [l_bor[0] - l_bor[2], l_bor[1], 0], [l_bor[0] + l_bor[2], l_bor[1], 0]) or
                intersection_2d(x, [l_shi[0] + l_shi[2], l_shi[1], 0], [l_bor[0], l_bor[1] - l_bor[2], 0], [l_bor[0], l_bor[1] + l_bor[2], 0]))
    left = int(intersection_2d(x, [l_shi[0] - l_shi[2], l_shi[1], 0], [l_bor[0] - l_bor[2], l_bor[1], 0], [l_bor[0] + l_bor[2], l_bor[1], 0]) or
               intersection_2d(x, [l_shi[0] - l_shi[2], l_shi[1], 0], [l_bor[0], l_bor[1] - l_bor[2], 0], [l_bor[0], l_bor[1] + l_bor[2], 0]))
    up = int(intersection_2d(x, [l_shi[0], l_shi[1] + l_shi[2], 0], [l_bor[0] - l_bor[2], l_bor[1], 0], [l_bor[0] + l_bor[2], l_bor[1], 0]) or
             intersection_2d(x, [l_shi[0], l_shi[1] + l_shi[2], 0], [l_bor[0], l_bor[1] - l_bor[2], 0], [l_bor[0], l_bor[1] + l_bor[2], 0]))
    down = int(intersection_2d(x, [l_shi[0], l_shi[1] - l_shi[2], 0], [l_bor[0] - l_bor[2], l_bor[1], 0], [l_bor[0] + l_bor[2], l_bor[1], 0]) or
               intersection_2d(x, [l_shi[0], l_shi[1] - l_shi[2], 0], [l_bor[0], l_bor[1] - l_bor[2], 0], [l_bor[0], l_bor[1] + l_bor[2], 0]))
    k = 1
    if l_bor[3] != 0:
        k = 0.9
    return [k * center * center_br, k * up * perif_br, k * down * perif_br, k * right * perif_br, k* left * perif_br]
    
    