import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import LogNorm, ListedColormap
import numpy as np

_fig = plt.figure()

def draw_pareto(epoch, front, p, dim=2):
    xs, front = front
    color = 'black'
    if epoch == 0:
        plt.ion()
        plt.show()

    plt.cla()

    plt.title('Epoch %i' % epoch, color=color)
    plt.ylabel('f2', color=color)
    plt.xlabel('f1', color=color)
    plt.xticks(color=color)
    plt.yticks(color=color)

    if dim == 3:
        ax = Axes3D(_fig)
        ax.scatter(front[:, 0], front[:, 1], front[:, 2], color='blue')

        ax.plot_trisurf(p[:, 0], p[:, 1], p[:, 2], color='red', linewidth=0)
    else:

        plt.scatter(p[:, 0], p[:, 1], color='blue')
        plt.scatter(front[:, 0], front[:, 1], color='red')


    plt.draw()
    plt.pause(0.001)

def draw_3d(epoch, results, problem):
    xs = results[0]
    results = results[1]


    def untuple(sol):
        return problem(sol)

    fig = plt.figure()
    ax = Axes3D(fig, azim=-29, elev=49)
    X = np.arange(-6, 6, 0.1)
    Y = np.arange(-6, 6, 0.1)
    X, Y = np.meshgrid(X, Y)
    Z = np.fromiter(map(untuple, zip(X.flat, Y.flat)), dtype=np.float, count=X.shape[0] * X.shape[1]).reshape(
        X.shape)

    alpha_cm = cm.jet(np.arange(cm.jet.N))
    alpha_cm[:, 3] = 0.25
    alpha_cm = ListedColormap(alpha_cm)

    ax.scatter(xs[:,0], xs[:,1], results, marker='o',cmap=alpha_cm, s=30)
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, norm=LogNorm(), cmap=alpha_cm, linewidth=0.2)

    plt.title('Epoch %i' % epoch)
    plt.xlabel("x")
    plt.ylabel("y")

    plt.show()

def convergence(first_front, optimal_front):
    """Given a Pareto front `first_front` and the optimal Pareto front,
    this function returns a metric of convergence
    of the front as explained in the original NSGA-II article by K. Deb.
    The smaller the value is, the closer the front is to the optimal one.

    first_front.shape : (2, n_1)
    optimal_front.shape : (2, n_2)
    """
    distances = []

    for ind in first_front:
        distances.append(float("inf"))
        for opt_ind in optimal_front:
            dist = 0.
            for i in range(len(opt_ind)):
                dist += (ind[i] - opt_ind[i]) ** 2
            if dist < distances[-1]:
                distances[-1] = dist
        distances[-1] = math.sqrt(distances[-1])

    return sum(distances) / len(distances)


def hypervolume(front, reference_point):
    assert (len(front[0]) == len(reference_point))
    hv = 0
    for individual in front:
        volume = 1
        for i in range(len(reference_point)):
            side_length = abs(individual[i] - reference_point[i])
            volume *= side_length
        hv += volume

    return hv / len(front)
