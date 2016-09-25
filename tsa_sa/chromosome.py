from random import shuffle, uniform, randint
import copy


class Chromosome:
    # GA / SA
    cities = []
    fit = 1

    # SA
    runs = 10000
    temp = 1
    cooling_dec = 0.999
    nr_swaps = 1
    cur_gen = 1

    def calc_solution(self):
        if len(self.cities) == 0:
            return 0
        prev_city = self.cities[-1]
        distance = 0
        for c in self.cities:
            cur_city = c
            distance += cur_city.calc_dist_euc2d(prev_city)
#             distance += cur_city.calc_dist_euc2d_swift(prev_city)
            prev_city = cur_city
        self.fit = distance

    def shuffle(self):
        shuffle(self.cities)
        self.calc_solution()

    def save_sol(self):
        text_file = open("solution.csv", "w")
        for c in self.cities:
            text_file.write(str(c.id) + '\n')
        text_file.close()

    def simulated_annealing(self):
        new_ind = create_ind(self.cities)
        self.calc_solution()
        res = []

        for r in range(0, self.runs):
            changes = []
            for t in range(0, self.nr_swaps):
                r1, r2 = new_ind.mutate()
                changes.insert(0, [r1, r2])
            if new_ind.fit < self.fit or uniform(0, 1) < self.temp:
                for r1, r2 in changes:
                    self.swap(r2, r1)
                self.fit = new_ind.fit
                self.cooling()
            else:
                for r1, r2 in changes:
                    new_ind.swap(r2, r1)
            res.append(new_ind.fit)
        return res

    #  swaps 2 cities
    def mutate(self):
        rand1 = randint(0, len(self.cities) - 1)
        rand2 = rand1
        while rand1 == rand2:
            rand2 = randint(0, len(self.cities) - 1)
        return self.swap(rand1, rand2)

    def swap(self, rand1, rand2):
        self.cities[rand2], self.cities[rand1] = self.cities[rand1], self.cities[rand2]
        self.calc_solution()
        return rand1, rand2

    def swapclose(self):
        rand = randint(0, len(self.cities) - 1)
        prox = self.cities[rand].close_neigh(self.cities)
        inspos = self.cities.index(prox)
        cit = self.cities.pop(rand)
        self.cities.insert(inspos, cit)

    def cooling(self):
        #self.temp *= self.cooling_dec
        self.cur_gen *= self.cooling_dec
        self.temp = 1/self.cur_gen


def create_ind(cities):
    new_ind = Chromosome()
    new_ind.cities = copy.deepcopy(cities)
    return new_ind

