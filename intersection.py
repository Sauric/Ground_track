from constants import *

distance = lambda x1, y1, z1, x2, y2, z2: R * np.arccos((x1 * x2 + y1 * y2 + z1 * z2) / R ** 2)


def satellite_pos(t_):
    x = a * cos(f1 * t_) + b * cos(f2 * t_)
    y = a * sin(f1 * t_) - b * sin(f2 * t_)
    z = c * sin(gamma * t_)
    ph = atan2(y, x)
    te = atan2(sqrt(x ** 2 + y ** 2), z)
    return ph, te


def satellite_pos2(t_):
    x = a * cos(f1 * t_) + b * cos(f2 * t_)
    y = a * sin(f1 * t_) - b * sin(f2 * t_)
    z = c * sin(gamma * t_)
    ph = atan2(y, x)
    te = atan2(sqrt(x ** 2 + y ** 2), z)
    return x, y, z, ph, te


def satellite_pos_xyz(t_):
    x = a * cos(f1 * t_) + b * cos(f2 * t_)
    y = a * sin(f1 * t_) - b * sin(f2 * t_)
    z = c * sin(gamma * t_)
    return x, y, z


def mid_step_per_t():
    dist = 0
    accur = 10000
    for i in range(accur):
        x1, y1, z1 = satellite_pos_xyz(i)
        x2, y2, z2 = satellite_pos_xyz(i + 1)
        dist += distance(x1, y1, z1, x2, y2, z2)
    return dist / accur


# for i in range(10):
#     x1, x2, x3 = satellite_pos_xyz(i)
#     x4, x5, x6 = satellite_pos_xyz(i + 1)
#
#     print("distanse in 1 of time = ", sqrt((x4 - x1) ** 2 + (x5 - x2) ** 2 + (x6 - x3) ** 2))

step = min(fabs(longitude[1] - longitude[0]),
               fabs(latitude[1] - latitude[0])) / 2
mid_V = mid_step_per_t()
step1 = (0.25*step*r/mid_V)
step2 = (2*np.pi*r_c*0.0001/mid_V)
print("Step1 = %f\nStep2 = %f\nMid_V = %f\n" % (step1, step2, mid_V))

def meeting_time(begin=0):

    t_ = begin
    while True:
        ph, te = satellite_pos(t_)
        if (longitude[0] <= ph <= longitude[1] and
                latitude[0] <= te <= latitude[1]):
            break
        t_ += step1

    t1, t2 = False, False
    t = t_ - step1
    while True:
        ph, te = satellite_pos(t)
        if (longitude[0] <= ph <= longitude[1] and
                latitude[0] <= te <= latitude[1]):
            break
        t += step2
    t_ = t
    # calc center of cicrcle
    x0 = R * cos(phi0) * sin(teta0)
    y0 = R * sin(phi0) * sin(teta0)
    z0 = R * cos(teta0)

    d_rad = r_c  #

    # print('d=', *d)
    print('d-rad =', d_rad)
    # calculated

    # step2 = 3 * step / (gamma + omega * r)
    while True:
        # print('t- t_ =', t - t_)
        x, y, z, ph, te = satellite_pos2(t)
        if (ph > longitude[1] or te > latitude[1] or
                ph < longitude[0] or te < latitude[0]):
            print('t- t_ =', t - t_)
            break
        dist = R * np.arccos((x * x0 + y * y0 + z * z0) / R ** 2)
        t += step2
        if not t1:
            if dist <= r_c:
                t1 = t - step2
            else:
                continue
        elif not t2 and dist >= r_c:
            t2 = t - step2
            break
    if t1 and t2:
        return t_, step1, t1, t2, step2
    return meeting_time(t)
