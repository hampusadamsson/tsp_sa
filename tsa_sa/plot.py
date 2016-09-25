import matplotlib.pyplot as plt


def plot_res(val, opt):
    optimal = opt
    plt.plot(val, color='b')
    plt.plot([optimal]*len(val), color='r')
    plt.ylabel('Fitness')
    plt.xlabel('Best: ' + str(val[len(val)-1]))
    plt.show()