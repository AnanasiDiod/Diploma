import math as m
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from auxulary import *
from constants import *
from threading import Thread


   
def main(dl, alpha = 0):
    lamps_3 = [(0.105 + dl, 0, new.lamp_radius, new.P),
               (- (0.105 + dl) * m.sin(m.pi / 6), (0.105 + dl) * m.cos(m.pi / 6), new.lamp_radius, new.P),
               (- (0.105 + dl) * m.sin(m.pi / 6), - (0.105 + dl) * m.cos(m.pi / 6), new.lamp_radius, new.P)]
    
    lamps_4 = [(0.105 + dl, 0, new.lamp_radius, new.P),
               (- (0.105 + dl), 0, new.lamp_radius, new.P),
               (0, 0.105 + dl, new.lamp_radius, new.P),
               (0, - (0.105 + dl), new.lamp_radius, new.P)]
    
    lamps_6 = [(0.105 + dl, 0.05, new.lamp_radius, new.P),
               (0.105 + dl, - 0.05, new.lamp_radius, new.P),
               (- (0.105 + dl) * m.sin(m.pi / 6) + 0.05 * m.cos(m.pi / 6), (0.105 + dl) * m.cos(m.pi / 6) + 0.05 * m.sin(m.pi / 6), new.lamp_radius, new.P),
               (- (0.105 + dl) * m.sin(m.pi / 6) - 0.05 * m.cos(m.pi / 6), (0.105 + dl) * m.cos(m.pi / 6) - 0.05 * m.sin(m.pi / 6), new.lamp_radius, new.P),
               (- (0.105 + dl) * m.sin(m.pi / 6) + 0.05 * m.cos(m.pi / 6), - (0.105 + dl) * m.cos(m.pi / 6) - 0.05 * m.sin(m.pi / 6), new.lamp_radius, new.P),
               (- (0.105 + dl) * m.sin(m.pi / 6) - 0.05 * m.cos(m.pi / 6), - (0.105 + dl) * m.cos(m.pi / 6) + 0.05 * m.sin(m.pi / 6), new.lamp_radius, new.P)]
    
    lamps_8 = [(0.105 + dl, 0.05, new.lamp_radius, new.P),
               (0.105 + dl, -0.05, new.lamp_radius, new.P),
               (-(0.105 + dl), 0.05, new.lamp_radius, new.P),
               (-(0.105 + dl), -0.05, new.lamp_radius, new.P),
               (0.05, 0.105 + dl, new.lamp_radius, new.P),
               (-0.05, 0.105 + dl, new.lamp_radius, new.P),
               (0.05, - (0.105 + dl), new.lamp_radius, new.P),
               (-0.05, - (0.105 + dl), new.lamp_radius, new.P)]
    
    lamps_6_custom = [(0.1 + dl + 0.05 * m.cos(alpha), 0.05 * m.sin(alpha), new.lamp_radius, new.P),
                      (0.1 + dl - 0.05 * m.cos(alpha), - 0.05 * m.sin(alpha), new.lamp_radius, new.P),
                      ( -(0.1 + dl) * m.sin(m.pi / 6) - 0.05 * m.cos(m.pi / 3 - alpha), (0.1 + dl) * m.cos(m.pi / 6) + 0.05 * m.sin(m.pi / 3 - alpha), new.lamp_radius, new.P),
                      ( -(0.1 + dl) * m.sin(m.pi / 6) + 0.05 * m.cos(m.pi / 3 - alpha), (0.1 + dl) * m.cos(m.pi / 6) - 0.05 * m.sin(m.pi / 3 - alpha), new.lamp_radius, new.P),
                      ( -(0.1 + dl) * m.sin(m.pi / 6) - 0.05 * m.cos(m.pi / 3 + alpha), - (0.1 + dl) * m.cos(m.pi / 6) - 0.05 * m.sin(m.pi / 3 + alpha), new.lamp_radius, new.P),
                      ( -(0.1 + dl) * m.sin(m.pi / 6) + 0.05 * m.cos(m.pi / 3 + alpha), - (0.1 + dl) * m.cos(m.pi / 6) + 0.05 * m.sin(m.pi / 3 + alpha), new.lamp_radius, new.P)]
    
    lamps = lamps_6_custom

    field = [[],[],[],[],[]]

    boards = [(0.195, 0.195, 0.0125, 0), 
              (0.195,- 0.195, 0.0125, 0),
              (- 0.195,0.195, 0.0125, 0), 
              (- 0.195, - 0.195, 0.0125, 0),
               (0, 0, 0.0125, 0)]
    
    # print(lamps)
    counter = 0
    #расчёт поля без учёта затенений
    rough = new.r_min
    # rough_list = [[],[],[],[]]
    while rough <= new.r_max:
        phi = 0
        # rough_list[0].append(rough)
        d_phi = 2 * m.pi / 572
        # rough_list[1].append(rough)
        while phi < 2 * m.pi:
            # rough_list[2].append(rough)
            x = rough * m.cos(phi)
            y = rough * m.sin(phi)
            local_field = 0
            for l in lamps:
                D = m.sqrt((l[0] - x) ** 2 + (l[1] - y) ** 2)
                alpha = 2*m.atan(new.L/(2 * D))
                lamp_flow = l[3] * (alpha + m.sin(alpha)) / (2 * (m.pi ** 2) * D * new.L)
                num_index = 1
                
                index = np.array([center_br,perif_br,perif_br,perif_br,perif_br])
                for lb in lamps + boards:
                        if lb != l:
                            intersection = intersect_lamp((x, y, 0), l, lb)
                            index = np.array([max(index[0] - intersection[0], 0),
                                              max(index[1] - intersection[1], 0),
                                              max(index[2] - intersection[2], 0),
                                              max(index[3] - intersection[3], 0),
                                              max(index[4] - intersection[4], 0)])
                            num_index = max(np.sum(index), 0)
                local_field += lamp_flow * num_index
            field[0].append(x)
            field[1].append(y)
            field[2].append(local_field)
            field[3].append(phi)
            field[4].append(rough)
            phi += d_phi   
        rough += new.dr

    return field[2]
data = []

for i in (0, m.pi / 6, m.pi / 4, m.pi / 3, m.pi / 2):
    data.append(main(0, i))
    print((i), ' done')

# Устреднение

data_meaned = []
for i in data:
    temp = []
    for j in range(int(len(i)/2)):
        temp.append((i[j * 2] + i[j * 2 + 1])/2)
    data_meaned.append(temp)

path = 'D:/Рабочий стол/git projects/test/6_lamps_different_angles.txt'
np.savetxt(path, np.transpose(np.matrix(data_meaned)*0.1))
