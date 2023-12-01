import math as m
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from auxulary import *
from constants import *
from threading import Thread


   
def main(dl):
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
    
    lamps = lamps_6

    field = [[],[],[],[],[]]

    boards = [(0.195, 0.195, 0.0125, 0), 
              (0.195,- 0.195, 0.0125, 0),
              (- 0.195,0.195, 0.0125, 0), 
              (- 0.195, - 0.195, 0.0125, 0),
              (0, 0, 0.0125, 0)]
    counter = 0
    #расчёт поля без учёта затенений
    rough = new.r_min
    # rough_list = [[],[],[],[]]
    while rough <= new.r_max:
        phi = 0
        # rough_list[0].append(rough)
        d_phi = 2 * m.pi / 570
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
        # print(rough)
                    

    # path = 'D:/Рабочий стол/git projects/test/3/' + name + '.txt'
    # np.savetxt(path, np.transpose(np.matrix(field[2:4])))
    

    # x = np.array(field[0])
    # y = np.array(field[1])
    # z = np.array(field[2])
    # # построение точек

    # fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # ax.scatter(x, y, z)
    # ax.set_zlim(0,np.max(z))
    # plt.show()

    return field[2]
    # print(rough_list)


    
# def from_file(name):
    # R_view = 3
    # field = np.loadtxt(name)
    # check = list()
    # nan = field[int(N/2)][int(N/2)]
    # for i in range(N):
    #     for j in range(int(N)):
    #         if abs(m.sqrt((i - N/2) ** 2 + (j - N/2) ** 2) - R_view/dr) < 0.2:
    #             if j - N/2 >= 0:
    #                 check.append([m.acos((i - N / 2)/m.sqrt((i - N / 2)**2 + (j - N / 2)**2)), field[i][j]])
    #             else:
    #                 check.append([m.pi + m.acos((i - N / 2)/m.sqrt((i - N / 2)**2 + (j - N / 2)**2)), field[i][j]])
                
    # fig = plt.figure()
    # x = np.linspace(0,r,N)
    # xgrid, ygrid = np.meshgrid(x, x)
    # ax = fig.add_subplot(projection='3d')
    # ax.plot_surface(xgrid, ygrid, field, rstride=2, cstride = 2, cmap='seismic')
    # plt.show()
    # np.savetxt(name+ '.txt', np.array(check))

# for i in range(5):
#     main(-i/100, str(-i))
#     print(-i)

# for i in range(5):
#     from_file('C:/Users/naumenko/Documents/code/quad + ' + str(-i))
#     print(-i)

data = []
j = 0
for i in (-4, -2, 0, 2, 4, 6, 8):
    data.append(main(i / 100))
    print((i), ' done')
    j += 1

# print(data)
path = 'D:/Рабочий стол/git projects/test/6_lamps.txt'
np.savetxt(path, np.transpose(np.matrix(data)))
