from simulated_annealing import make_sim_ann
from plot import plot_res
import sys


def sim_a_solver(prob, param):
    sim = make_sim_ann(prob)
    sim.parse_input(param)

    print('SA - ' + prob)
    best = sim.run()
    sol = best.fit
    best.save_sol()
    print('FIT: ' + str(sol))
    print('----')

city = sys.argv[1]
prob = ''.join(sys.argv)
prob = prob.replace(" ", "")
prob = prob.split("-")
prob.reverse()
prob.pop()
sim_a_solver(city, prob)
