from simulated_annealing import make_sim_ann
import sys


def sim_a_solver(prob, param):
    sim = make_sim_ann(prob)
    sim.parse_input(param)

    best = sim.run()
    sol = best.fit
    best.save_sol()
    print(str(sol))

city = sys.argv[1]
prob = ''.join(sys.argv)
prob = prob.replace(" ", "")
prob = prob.split("-")
prob.reverse()
prob.pop()
sim_a_solver(city, prob)
