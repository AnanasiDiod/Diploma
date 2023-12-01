import math as m
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from auxulary import *
from constants import *


   
def main(dl, name):
    lamps_triple = [(N/2 - 0.05 / dr, N/2 + (0.075 + dl) / dr, 0.028 / dr, P), 
                    (N/2 + 0.05 / dr, N/2 + (0.075 + dl) / dr, 0.028 / dr, P),
                    (N/2 - (0.09 + dl * m.cos(m.pi / 6)) / dr, N/2 - (0.006 + dl * m.sin(m.pi / 6)) / dr, 0.028 / dr, P), 
                    (N/2 + (0.09 + dl * m.cos(m.pi / 6)) / dr, N/2 - (0.006 + dl * m.sin(m.pi / 6)) / dr, 0.028 / dr, P),
                    (N/2 - (0.04 + dl * m.cos(m.pi / 6)) / dr, N/2 - (0.081 + dl * m.sin(m.pi / 6)) / dr, 0.028 / dr, P), 
                    (N/2 + (0.04 + dl * m.cos(m.pi / 6)) / dr, N/2 - (0.081 + dl * m.sin(m.pi / 6)) / dr, 0.028 / dr, P)]
    
    lamps_quad = [(N/2 - (0.04 + dl * m.cos(m.pi / 4)) / dr, N/2, 0.028 / dr, P), 
                  (N/2 + (0.04 + dl * m.cos(m.pi / 4)) / dr, N/2, 0.028 / dr, P)]#,
                #   (N/2 - (0.04 + dl * m.cos(m.pi / 4)) / dr, N/2 - (0.11 + dl * m.cos(m.pi / 4)) / dr, 0.028 / dr, P), 
                #   (N/2 + (0.04 + dl * m.cos(m.pi / 4)) / dr, N/2 - (0.11 + dl * m.cos(m.pi / 4)) / dr, 0.028 / dr, P),
                #   (N/2 - (0.11 + dl * m.cos(m.pi / 4)) / dr, N/2 + (0.04 + dl * m.cos(m.pi / 4)) / dr, 0.028 / dr, P), 
                #   (N/2 - (0.11 + dl * m.cos(m.pi / 4)) / dr, N/2 - (0.04 + dl * m.cos(m.pi / 4)) / dr, 0.028 / dr, P),
                #   (N/2 + (0.11 + dl * m.cos(m.pi / 4)) / dr, N/2 + (0.04 + dl * m.cos(m.pi / 4)) / dr, 0.028 / dr, P), 
                #   (N/2 + (0.11 + dl * m.cos(m.pi / 4)) / dr, N/2 - (0.04 + dl * m.cos(m.pi / 4)) / dr, 0.028 / dr, P)]
    
    lamps = lamps_quad
    field = np.zeros((N, N), dtype=float)

    boards = [(N/2 + 0.195 / dr, N/2 + 0.195 / dr, 0.025 / dr, 0), 
              (N/2 + 0.195 / dr, N/2 - 0.195 / dr, 0.025 / dr, 0),
              (N/2 - 0.195 / dr, N/2 + 0.195 / dr, 0.025 / dr, 0), 
              (N/2 - 0.195 / dr, N/2 - 0.195 / dr, 0.025 / dr, 0),
              (N/2, N/2, 0.025, 0)]
    counter = 0
    #расчёт поля без учёта затенений
    for i in range(N):
        for j in range(N):
                for l in lamps:
                    # расстояние от точик наблюдения до лампы, поток от которой мы сейчас считаем
                    D = dr * m.sqrt((l[0] - i + 1) ** 2 + (l[1] - j + 1) ** 2)
                    if  D >= r_min:
                        # print(';')
                        alpha = 2*m.atan(L/(2 * D))
                        lamp_flow = l[3] * (alpha + m.sin(alpha)) / (2 * (m.pi ** 2) * D * L)
                        num_index = 1
                        index = np.array([center_br,perif_br,perif_br,perif_br,perif_br])#центр, верх, низ, право, лево
                        #вычтем из потока то, что его пересекает
                        for lb in lamps + boards:
                            if lb != l:
                                index -= np.array(intersect_lamp((i, j, 0), l, lb))
                                num_index = max(np.sum(index), 0)
                        
                        # field[i][j] += lamp_flow * num_index
                        field[i][j] += num_index

                    # elif D <= 0.01:
                    #     field[i][j] += np.max(field[0]) * 2
                        
                    else:
                        field[i][j] = (np.min(field[0]) + np.max(field[0]))/2
                        # print('qq')
                counter += 1
                print(counter/ N ** 2)

    path = 'D:/Рабочий стол/git projects/test/' + name + '.txt'
    np.savetxt(path, field)


    fig = plt.figure()
    x = np.linspace(0,r,N)
    xgrid, ygrid = np.meshgrid(x, x)
    ax = fig.add_subplot(projection='3d')
    ax.plot_surface(xgrid, ygrid, field, rstride=2, cstride = 2, cmap='seismic')
    plt.show()
    return path


    
def from_file(name):
    R_view = 3
    field = np.loadtxt(name)
    check = list()
    nan = field[int(N/2)][int(N/2)]
    for i in range(N):
        for j in range(int(N)):
            if abs(m.sqrt((i - N/2) ** 2 + (j - N/2) ** 2) - R_view/dr) < 0.2:
                if j - N/2 >= 0:
                    check.append([m.acos((i - N / 2)/m.sqrt((i - N / 2)**2 + (j - N / 2)**2)), field[i][j]])
                else:
                    check.append([m.pi + m.acos((i - N / 2)/m.sqrt((i - N / 2)**2 + (j - N / 2)**2)), field[i][j]])
                
    fig = plt.figure()
    x = np.linspace(0,r,N)
    xgrid, ygrid = np.meshgrid(x, x)
    ax = fig.add_subplot(projection='3d')
    ax.plot_surface(xgrid, ygrid, field, rstride=2, cstride = 2, cmap='seismic')
    plt.show()
    np.savetxt(name+ '.txt', np.array(check))

# for i in range(5):
#     main(-i/100, str(-i))
#     print(-i)

# for i in range(5):
#     from_file('C:/Users/naumenko/Documents/code/quad + ' + str(-i))
#     print(-i)

# file = main(0, 'test')
from_file("D:/Рабочий стол/git projects/test/test.txt")