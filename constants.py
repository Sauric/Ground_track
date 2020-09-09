import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import sin, cos, sqrt, fabs, atan2
from PIL import Image, ImageEnhance
from collections import deque

size = 100
R = 6378  # Radius of earth (km)
r = R + 2000  # Radius of satellite orbit (km)
G = 6.67430 * (10 ** (-11))  # Gravitational constant (m^3/kg*s^2)
M = 5.9722 * (10 ** 24)  # Earth mass (kg)
V = sqrt(G * M / (r * 10 ** 3))  # Velocity of Satellite (m/s)
# print('V=', V)
dt = 200  # Delta time (s)
omega = 0.0000729211840505999  # Earth Angular Velocity (rad/s)

r_c = 1010 # Radius of circle on the Earth
al = 30 * (np.pi / 180)  # angle of rotation of the satellite trajectory about the x axis
                         # i. e. angle between the plane of equator and the plane of satellite motion
phi0, teta0 = -1 * (3.5 * np.pi / 2) , -1 * (2 * np.pi / 6)  # np.pi/2 - r_c/R <= teta0 <= r_c/R - np.pi/2
dTeta = (r_c / R)
# phi0, teta0 = (2 * np.pi - phi0), (-np.pi / 2 + teta0)  # centre of a circle on sphere
circle_diap = [-np.pi, np.pi]

lstep = 1  # time step
# Different constants for findig ground track and circle on earth
A = R * sin(dTeta) * cos(teta0) * cos(phi0)
B = - R * cos(dTeta) * sin(teta0) * cos(phi0)
C = R * sin(dTeta) * sin(phi0)
D = - R * sin(dTeta) * cos(teta0) * sin(phi0)
E = R * cos(dTeta) * sin(teta0) * sin(phi0)
F = R * sin(dTeta) * cos(phi0)
G = R * sin(dTeta) * sin(teta0)
H = R * cos(dTeta) * cos(teta0)

phi0, teta0 = -1 * phi0, -1 * teta0

# al = -al
a = R * (1 + cos(al)) / 2
b = R * (1 - cos(al)) / 2
c = -R * sin(al)

# al = -al
f1 = V * 0.001 / r + omega
f2 = V * 0.001 / r - omega
gamma = V * 0.001 / r
if teta0 - dTeta > np.pi / 2 + al or teta0 + dTeta < np.pi / 2 - al:
    print('Interception is impossible')
    exit()
elif np.pi / 2 - al <= teta0 <= np.pi / 2 + al:
    print("\n Case 2 \n")
    min_, max_ = 10, -1
    for p in np.linspace(0, 4 * np.pi / 2, 500):
        x = A * np.cos(p) + C * np.sin(p) + B
        y = D * np.cos(p) + F * np.sin(p) + E
        it = np.arctan2(y, x)
        if it < min_:
            min_ = it
        if it > max_:
            max_ = it


elif teta0 > np.pi/2 + al or teta0 < np.pi/2 - al:
    print("\n Case 3 \n")
    if teta0 > np.pi/2 + al:
        shirota = np.pi/2 + al
    else:
        shirota = np.pi/2 - al
    min_, max_ = False, False
    p = 2*np.pi/500

    tet0 = atan2(sqrt((A+B)**2 + (D+E)**2), G+H)
    for p in np.linspace(0, 2*np.pi, 500):
        x = A * cos(p) + C * sin(p) + B
        y = D * cos(p) + F * sin(p) + E
        z = G * cos(p) + H

        tet1 = atan2(sqrt(x * x + y * y), z)
        # print((tet1 - tet0)*180/np.pi, end=' ')
        if tet0 <= shirota < tet1 or tet1 <= shirota < tet0:
            print('enter')
            if not min_:
                min_ = atan2(y, x)
                print('tet1 (grad), P',tet1*180/np.pi, p)
            elif not max_:
                max_ = atan2(y, x)
                print('tet1 (grad), P',tet1*180/np.pi, p)
                break
        tet0 = tet1
longitude = (min_, max_) if min_ < max_ else (max_,min_)
latitude = (max(teta0 - dTeta, np.pi / 2 - al), min(teta0 + dTeta, np.pi / 2 + al))
# print('longitude (grad)',longitude[0]*180/np.pi, longitude[1]*180/np.pi)
# print('latitude (rad)',latitude[0]*180/np.pi, latitude[1]*180/np.pi)
# print('Circle diapazone :', *circle_diap)

def spec_line():
    x, y, z = np.array([]), np.array([]), np.array([])
    for t in latitude:
        ph = np.mgrid[longitude[0]:longitude[1]:100j]
        # ph = np.mgrid[0:2*np.pi:100j]
        x = np.hstack((x, R * np.cos(ph) * sin(t)))
        y = np.hstack((y, R * np.sin(ph) * sin(t)))
        z = np.hstack((z, R * np.array([cos(t)] * 100)))
    for p in longitude:
        t = np.mgrid[latitude[0]:latitude[1]:100j]
        # t = np.mgrid[-np.pi/2:np.pi/2:100j]
        x = np.hstack((x, R * cos(p) * np.sin(t)))
        y = np.hstack((y, R * sin(p) * np.sin(t)))
        z = np.hstack((z, R * np.cos(t)))

    return x, y, z


# Rot_matr_z = np.array([
#         [cos(phi0), - sin(phi0), 0],
#         [sin(phi0), cos(phi0), 0],
#         [0, 0, 1]
#     ])
#     Rot_matr_y = np.array([
#         [cos(teta0), 0, sin(teta0)],
#         [0, 1, 0],
#         [-sin(teta0), 0, cos(teta0)]
#     ])
#
#
#     teta = np.array([(r_c / R)] * 100)
#     phi = np.mgrid[0: 2 * np.pi: 100j]
#     x = R * np.cos(phi) * np.sin(teta)
#     y = R * np.sin(phi) * np.sin(teta)
#     z = R * np.cos(teta)
#     xyz = np.array([x, y, z]).T
#     xyz = np.dot(np.dot(xyz, Rot_matr_y), Rot_matr_z).T
#
#     ax.plot(xyz[0], xyz[1], xyz[2], color='r', linewidth=4)
