import matplotlib.pyplot as plt


def plot_res(val1, optimal):
    plt.plot(val1, color='g')
    plt.plot(([int(optimal)] * len(val1)), color='r')
    plt.ylabel('Fitness')
    plt.xlabel('Generations')

    plt.show()


def plot_res2(val1, val2, optimal):
    plt.plot(val1, color='b')
    plt.plot(val2, color='g')
    plt.plot(([int(optimal)] * len(val1)), color='r')
    plt.ylabel('Fitness')
    plt.xlabel('Generations & temperature')

    plt.show()