import os
import matplotlib.pyplot as plt
import copy
import random
import model as md
import functions as fn



class First_population:


    def __init__(self, n, SL, SW, SP, SC, SG):

        self.fn = fn.Functions()

        self.SL = SL
        self.SW = SW
        self.SP = SP
        self.SC = SC
        self.SG = SG

        self.n = n

        
    def generate_first_population(self, size_population):

        population = []
        goal_functions = []
        percent = 0

        for per in range(size_population):

            if int(per/size_population*100) != percent:
                os.system('cls' if os.name == 'nt' else 'clear')
                percent = int(per/size_population*100)
                print('\nGenerate first population process:', percent + 1, '%')
                
            one_result = md.Model(self.SC, self.SL, self.SW, self.n, self.SG)

            HP = [[] for _ in range(self.n)]
            points = []
            
            for i in range(len(self.SC)):
                for value in self.SP[i + 1]:
                    points.append([i + 1, value[0], value[1]])

            idx = 0

            for elem in points:

                # random_id = random.randint(0, 5)
                HP[idx].append(elem[:-1])

                if elem[0] not in one_result.DP[idx].keys():
                    one_result.DP[idx][elem[0]] = []

                one_result.DP[idx][elem[0]].append([elem[1], elem[2]])

                idx += 1

                if idx == self.n:
                    idx = 0

            one_result.HP = HP
            
            for i in range(len(HP)):
                one_result.DT[i] = self.fn.generate_track(HP[i], 4, self.SG)

            SL_copy = copy.deepcopy(self.SL)
            itr = 0

            for i in range(self.n):

                lok = random.randint(0, len(SL_copy) - 1)

                while SL_copy[lok][1] == 0:
                    lok = random.randint(0, len(SL_copy) - 1)
                    itr += 1
                    if itr > 1000:
                        print("ERROR - infinity loop in DL")

                SL_copy[lok][1] -= 1
                one_result.DL[i] = lok

            for i in range(self.n):

                max_packages = 0
                actually_packages = 0
                DT_copy = copy.deepcopy(one_result.DT[i])
                DP_copy = copy.deepcopy(one_result.DP[i])
                SW_copy = copy.deepcopy(self.SW)
                DP_actually = {}

                for elem in DT_copy:

                    if elem[0] in DP_copy.keys():

                        for e in DP_copy[elem[0]]:

                            if e[0] not in DP_actually:
                                DP_actually[e[0]] = e[1]
                            else:
                                DP_actually[e[0]] += e[1]
                            actually_packages += e[1]

                        del DP_copy[elem[0]]

                    if actually_packages > max_packages:
                        max_packages = actually_packages

                    if elem[1] in DP_actually.keys():
                        actually_packages -= DP_actually[elem[1]]
                        del DP_actually[elem[1]]

                    itr1 = 0

                    while self.sum_w_capacity(one_result.DW[i]) < max_packages:

                        random_id = random.randint(0, len(self.SW) - 1)
                        itr1 += 1

                        if itr1 > 1000:
                            print("ERROR - infinity loop in DW")

                        itr2 = 0

                        while SW_copy[random_id][1] == 0:
                            random_id = random.randint(0, len(self.SW) - 1)
                            itr2 += 1
                            if itr2 > 1000:
                                print("ERROR - infinity loop in DW")

                        one_result.DW[i][random_id] += 1
                        SW_copy[random_id][1] -= 1

            goal_functions.append(one_result.goal_function())
                
            population.append(one_result)

        min__ = min(goal_functions)
        max__ = max(goal_functions)
        mean__ = sum(goal_functions)/len(goal_functions)
        
        print('\nMin GF:', min__)
        print('Max GF:', max__)
        print('Mean GF:', mean__)

        X = [i + 1 for i in range(size_population)]
        min_ = [min__ for _ in range(size_population)]
        max_ = [max__ for _ in range(size_population)]
        mean_ = [mean__ for i in range(size_population)]

        plt.plot(X, goal_functions, label = 'Aktualna funkcja celu')
        plt.plot(X, min_, label = 'Najmniejsza funkcja celu')
        plt.plot(X, max_, label = 'Największa funkcja celu')
        plt.plot(X, mean_, label = 'Średnia funkcja celu')
        plt.title('Pierwsza wygenerowana populacja')
        plt.xlabel('Numer populacji')
        plt.ylabel('Wartość funkcji celu')
        plt.legend()
        plt.grid()
        plt.show()

        return population


    def sum_w_capacity(self, DW):

        capacity = 0

        for i in range(len(self.SW)):
            capacity += self.SW[i][2] * DW[i]
            
        return capacity