import os
import matplotlib.pyplot as plt
import copy
import random
import model as md
import functions as fn



class First_population:


    def __init__(self, n, SL, SW, SP, SC, SG):

        self.fn = fn.Functions(n, SW)

        self.SL = SL
        self.SW = SW
        self.SP = SP
        self.SC = SC
        self.SG = SG

        self.n = n

        
    def generate_first_population(self, size_population, start):

        population = []
        goal_functions = []
        percent = 0

        for per in range(size_population):

            # if int(per/size_population*100) >= percent:
            #     os.system('cls' if os.name == 'nt' else 'clear')
            #     percent = int((per+1)/size_population*100)
            #     print('\nGenerate first population process:', percent, '%')
                
            one_result = md.Model(self.SC, self.SL, self.SW, self.n, self.SG)

            HP = [[] for _ in range(self.n)]
            points = {}
            
            for key in self.SP:
                for elem in self.SP[key]:
                    if (key, elem[0]) not in points.keys():
                        points[key, elem[0]] = 0
                    points[key, elem[0]] += elem[1]

            idx = 0

            for elem in points.keys():
                
                HP[idx].append(elem)

                if elem[0] not in one_result.DP[idx].keys():
                    one_result.DP[idx][elem[0]] = {}

                if elem[1] not in one_result.DP[idx][elem[0]].keys():
                    one_result.DP[idx][elem[0]][elem[1]] = 0

                one_result.DP[idx][elem[0]][elem[1]] += points[elem[0], elem[1]]

                idx += 1

                if idx == self.n:
                    idx = 0

            one_result.HP = HP
            
            for i in range(len(HP)):
                one_result.DT[i] = self.fn.generate_track(HP[i], start, self.SG)

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

            self.fn.attaching_wagons(one_result)

            for i in range(self.n):
                one_result.solve_HL(i)
                one_result.solve_HF(i)

            # goal_functions.append(one_result.goal_function())
            population.append(one_result)

        # min__ = min(goal_functions)
        # max__ = max(goal_functions)
        # mean__ = sum(goal_functions)/len(goal_functions)
        
        # print('\nMin GF:', min__)
        # print('Max GF:', max__)
        # print('Mean GF:', mean__)

        # X = [i + 1 for i in range(size_population)]
        # min_ = [min__ for _ in range(size_population)]
        # max_ = [max__ for _ in range(size_population)]
        # mean_ = [mean__ for i in range(size_population)]

        # plt.plot(X, goal_functions, label = 'Aktualna funkcja celu')
        # plt.plot(X, min_, label = 'Najmniejsza funkcja celu')
        # plt.plot(X, max_, label = 'Największa funkcja celu')
        # plt.plot(X, mean_, label = 'Średnia funkcja celu')
        # plt.title('Pierwsza wygenerowana populacja')
        # plt.xlabel('Numer populacji')
        # plt.ylabel('Wartość funkcji celu')
        # plt.legend()
        # plt.grid()
        # plt.show()

        return population