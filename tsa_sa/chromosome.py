from random import shuffle, uniform, randint
import copy


class Chromosome:
    # GA / SA
    cities = []

    fit = 1
    dist_matrix = []

    group_size = 1

    # SA
    runs = 10000
    temp = 1
    cooling_dec = 0.999

    def calc_solution(self):
        if len(self.cities) == 0:
            return 0
        prev_city = self.cities[-1]
        distance = 0
        for c in self.cities:
            cur_city = c
            distance += self.dist_matrix[cur_city.id][prev_city.id]
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

    def local_search(self):
        res = []

        best = 9999999
        best_c = []

        # EVERY STARTING POINT GREEDY
        for i in range(0, len(self.cities)-1):
            print len(self.cities)-i
            print best

            c1 = self.cities.pop(i)
            heap = [c1]
            while len(self.cities) > 0:
                c2 = self.find_close(c1, self.cities)
                self.cities.remove(c2)
                assert c2 not in self.cities
                assert c2 not in heap
                heap.append(c2)
                c1 = c2

            self.cities = heap
            self.calc_solution()
            res.append(self.fit)

            if self.fit < best:
                best = self.fit
                best_c = copy.copy(self.cities)
                self.save_sol()

        self.cities = best_c
        self.calc_solution()

        return res

    def simulated_annealing(self):
        new_ind = create_ind(self.cities, self.dist_matrix)
        self.calc_solution()
        res = []

        for r in range(0, self.runs):
            #  sim ann
            r1, r2 = new_ind.mutate()
            if new_ind.fit < self.fit or uniform(0, 1) < self.temp:
                self.swap(r2, r1)
                self.fit = new_ind.fit
                self.cooling()
            else:
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

    def cooling(self):
        self.temp *= self.cooling_dec

    def rank_select(self, pop):
        total = sum(range(0, len(pop) + 1))
        r = uniform(0, total)
        tot = 0
        for c in range(1, len(pop) + 1):
            if tot + c >= r:
                return pop[c - 1]
            tot += c

    def find_close(self, cit1, popu):
        res = 0
        best = 99999999
        for c in popu:
            if self.dist_matrix[cit1.id][c.id] < best:
                best = self.dist_matrix[cit1.id][c.id]
                res = c
        return res


def create_ind(cities, d_m):
    new_ind = Chromosome()
    new_ind.cities = copy.deepcopy(cities)
    new_ind.heap = copy.deepcopy(cities)
    new_ind.dist_matrix = d_m
    return new_ind

