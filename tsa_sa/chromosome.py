from random import shuffle, uniform, randint
import copy


class Chromosome:
    # GA / SA
    cities = []

    fit = -1
    dist_matrix = []

    group_size = 1

    # SA
    runs = 10000
    temp = 1
    cooling_dec = 0.999
    gen = 1

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

    def calc_tour_solution(self, tour):
        assert len(tour) > 0
        prev_city = tour[-1]
        distance = 0
        for c in tour:
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

    def two_opt_swap(self, i, k):
        l1 = []
        l2 = []

        for x in range(0, i):
            l1.append(self.cities.pop(0))
        for y in range(0, k):
            if len(self.cities) <= 0:
                break
            l2.insert(0, self.cities.pop(0))

        self.cities = l1+l2+self.cities

    def two_opt(self):
        res = []
        swaps = len(self.cities)-1
        self.calc_solution()
        best = self.fit
        res.append(best)
        improves = True

        gen = 0
        while improves:
            gen += 1
            improves = False
            for i in range(0, swaps):
                for k in range(i+1, swaps):
                    rev_back = copy.copy(self.cities)
                    self.two_opt_swap(i, k)
                    self.calc_solution()
                    res.append(best)
                    if self.fit < best:
                        best = self.fit
                        self.save_sol()
                        improves = True
                    else:
                        self.cities = rev_back
        return res

    def local_search(self):
        res = []

        best = 9999999
        best_c = []

        # EVERY STARTING POINT GREEDY
        for i in range(len(self.cities)-1, 0, -1):
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

    def simulated_annealing_two_opt(self):
        self.calc_solution()
        best = self.fit

        cool = []
        res = []
        for r in range(0, self.runs):
            i = randint(0, len(self.cities) - 2)
            k = randint(0, len(self.cities)-i)

            rev_back = copy.copy(self.cities)
            self.two_opt_swap(i, k)
            self.calc_solution()

            if best > self.fit or uniform(0, 1) < self.temp:
                best = self.fit
            else:
                self.cities = rev_back
                self.fit = best
                res.append(best)
                self.save_sol()
                cool.append(30000*self.temp)
                print best
            self.cooling()

        self.fit = best
        return res, cool

    def simulated_annealing(self):
        res = []
        new_ind = create_ind(self.cities, self.dist_matrix)
        self.calc_solution()
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
#        self.gen *= 1.0001

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

