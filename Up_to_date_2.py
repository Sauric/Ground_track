# the earth is motionless
# the satellite has an angular velocity
from interseption import *

t_, step, t1, t2, step2 = meeting_time()
err = tuple(((satellite_pos_xyz(t1)), (satellite_pos_xyz(t1 + step2))))
err = distance(*err[0], *err[1])/2
print('meeting tim() =  %f hours\nt1 = %f\nt2 = %f\n' % (t_/3600, t1, t2))
# exit()
if __name__ == '__main__':
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    plt.xlim([-r - 10, r + 10])
    plt.ylim([-r - 10, r + 10])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title('Circle')
    # ax.view_init(azim=2*np.pi/2)
    # plt.axis('off')
    # Load earthmap with PIL
    bm = Image.open('earthmap.jpg')
    bm = ImageEnhance.Brightness(bm).enhance(3)
    # It's big, so I'll rescale it, convert to array, and divide by 256 to get RGB values that matplotlib accept
    print(*bm.size)
    bm = np.array(bm.resize([d // 3 for d in bm.size])) / 256.

    # d/1 is normal size, anything else is smaller - faster loading time on Uni HPC

    # Coordinates of the image - don't know if this is entirely accurate, but probably close
    lons = np.linspace(-180, 180, bm.shape[1]) * np.pi / 180
    lats = np.linspace(-90, 90, bm.shape[0])[::-1] * np.pi / 180

    # Repeat code specifying face colours

    x = np.outer(R * np.cos(lons), np.cos(lats)).T
    y = np.outer(R * np.sin(lons), np.cos(lats)).T
    z = np.outer(R * np.ones(np.size(lons)), np.sin(lats)).T
    ax.plot_surface(x, y, z,
                    rstride=4, cstride=4,
                    facecolors=bm, linewidth=0.1, shade=False, alpha=0.3)

    # plotting circle on Earth
    phi = np.mgrid[circle_diap[0]:circle_diap[1]:200j]
    x = A * np.cos(phi) + C * np.sin(phi) + B
    y = D * np.cos(phi) + F * np.sin(phi) + E
    z = G * np.cos(phi) + H * np.ones(len(phi))
    ax.plot(x, y, z, color='r', alpha=0.5  )

    # plotting some helpfull lines
    x, y, z = spec_line()  #
    ax.plot(x, y, z, color='black')
    phi = np.mgrid[0:2 * np.pi:100j]
    x = R * np.cos(phi) * cos(al)
    y = R * np.sin(phi) * cos(al)
    z = R * np.array([sin(al)] * 100)
    ax.plot(x, y, z, color='orange')
    x = R * np.cos(phi) * cos(-al)
    y = R * np.sin(phi) * cos(-al)
    z = R * np.array([sin(-al)] * 100)
    ax.plot(x, y, z, color='orange')

    plt.ion()
    # plotting satellite trajectory and ground track realtime
    x, y, z = deque([], lstep + 1), deque([], lstep + 1), deque([], lstep + 1)
    x_gt, y_gt, z_gt = deque([], lstep + 1), deque([], lstep + 1), deque([], lstep + 1)
    t = 0 #t1 - 100*step
    colr = "g"
    while t <= 1000000: #t2 + 10*step:
        # ground track
        x_gt.append(a * cos(f1 * t) + b * cos(f2 * t))
        y_gt.append(a * sin(f1 * t) - b * sin(f2 * t))
        z_gt.append(c * sin(gamma * t))
        if t == t1 or t == t2:
            colr = "black"
        else:
            colr = "green"
        if t < t1 or t > t2:
            t += 2*step
        else:
            t += 30*step2

        ax.plot(x_gt, y_gt, z_gt, color=colr)
        plt.draw()
        plt.pause(0.00001)

    plt.ioff()
    plt.show()
    # fig.savefig('mpl.jpg')
