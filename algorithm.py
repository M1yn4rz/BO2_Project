import graph as gp
import model as md
import pandas as pd
import load_csv as ld
import random
import networkx as nx
import os
import matplotlib.pyplot as plt
import copy
import sys
import first_population as fp
import functions as fn



sys.setrecursionlimit(10000)



class Algorithm:


    def __init__(self, SL, SW, n):

        self.load_csv = ld.Load_csv()
        self.graph = gp.Graph()
        self.fn = fn.Functions()

        self.SL = SL
        self.SW = SW
        self.SP = self.load_csv.read_packages()
        self.SC = self.load_csv.read_coordinates()
        self.SG = self.graph.G

        self.n = n

        self.fp = fp.First_population(self.n, 
                    self.SL, self.SW, self.SP, self.SC, self.SG)


    def AG(self, size_population = 1000, epochs = 50, previous_population = 5, mutate_power = 5):

        population = self.fp.generate_first_population(size_population)

        actually_population = population
        previous_population = int(previous_population / 100 * size_population)

        list_min_f = []
        list_max_f = []
        list_mean_f = []
        X = [i + 1 for i in range(epochs)]

        percent = 0

        for per in range(epochs):

            if int(per/epochs*100) != percent:
                os.system('cls' if os.name == 'nt' else 'clear')
                percent = int((per + 1)/epochs*100)
                print('\nGenerate new epochs process :', percent, '%')
                print('Actually epoch :', per, '/', epochs, ': All epochs')

            actually_population = self.fn.sort(actually_population)
            actually_population = actually_population[:previous_population]
            population_to_mutate = copy.deepcopy(actually_population)

            itr = 0
            max_itr = size_population - previous_population
            percent_epoch = 0

            while len(actually_population) < size_population:
                actually_population.append(self.mutate_population(population_to_mutate, mutate_power))
                itr += 1

                if int(itr/max_itr*100) != percent_epoch:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    percent_epoch = int((itr + 1)/max_itr*100)
                    print('\nGenerate new epochs process :', percent, '%')
                    print('Actually epoch :', per + 1, '/', epochs, ': All epochs')
                    print('Generate actually epoch :', percent_epoch, '%')

                if itr > 10 * max_itr:
                    print("ERROR - infinity loop in mutate")
                    return None

            for result in actually_population:
                result.goal_function()

            goal_functions = [x.f for x in actually_population]

            list_min_f.append(min(goal_functions))
            list_max_f.append(max(goal_functions))
            list_mean_f.append(sum(goal_functions)/len(goal_functions))

        plt.plot(X, list_min_f, label = 'Najmniejsza funkcja celu danej populacji')
        plt.plot(X, list_max_f, label = 'Największa funkcja celu danej populacji')
        plt.plot(X, list_mean_f, label = 'Średnia funkcja celu danej populacji')
        plt.title('Wykres funkcji celu kolejnych populacji')
        plt.xlabel('Numer populacji')
        plt.ylabel('Wartość funkcji celu')
        plt.legend()
        plt.grid()
        plt.show()

        best_id = goal_functions.index(min(goal_functions))
        best_result = actually_population[best_id]

        for i in range(self.n):
            print("\n", i, ":", best_result.DT[i])

        return best_result
        
    
    def mutate_population(self, population, mutate_power):

        result_id = random.randint(0, len(population) - 1)

        return self.mutate_points(population[result_id], mutate_power)


    def mutate_points(self, result, mutate_power):
        
        new_result = copy.deepcopy(result)

        for _ in range(int(mutate_power / 100 * self.n * 20)):

            train_max_track = new_result.HL.index(max(new_result.HL))
            train_min_track = new_result.HL.index(min(new_result.HL))

            point_id = random.randint(0, len(new_result.HP[train_max_track]) - 1)
            new_result.HP[train_min_track].append(new_result.HP[train_max_track][point_id])
            del new_result.HP[train_max_track][point_id]

            new_result.DT[train_max_track] = self.fn.generate_track(new_result.HP[train_max_track], 4, self.SG)
            new_result.DT[train_min_track] = self.fn.generate_track(new_result.HP[train_min_track], 4, self.SG)
            new_result.solve_HL(train_max_track)
            new_result.solve_HL(train_min_track)
        
        for _ in range(int(mutate_power / 100 * self.n * 10)):

            train_max_track = new_result.HL.index(max(new_result.HL))
            test_result = copy.deepcopy(new_result)

            random.shuffle(test_result.HP[train_max_track])
            test_result.DT[train_max_track] = self.fn.generate_track(test_result.HP[train_max_track], 4, self.SG)
            test_result.solve_HL(train_max_track)

            itr = 0

            while test_result.HL[train_max_track] > new_result.HL[train_max_track]:

                random.shuffle(test_result.HP[train_max_track])
                test_result.DT[train_max_track] = self.fn.generate_track(test_result.HP[train_max_track], 4, self.SG)
                test_result.solve_HL(train_max_track)
                itr += 1

                if itr > 100:
                    break

            if itr < 100:
                new_result = copy.deepcopy(test_result)

        self.mutate_lok(new_result, mutate_power)
        self.mutate_wag(new_result)

        return new_result


    def mutate_lok(self, result, mutate_power):

        SL_copy = copy.deepcopy(self.SL)
        itr = 0

        for _ in range(int(mutate_power / 100 * self.n * 10)):

            i = random.randint(0, self.n - 1)

            lok = random.randint(0, len(SL_copy) - 1)

            while SL_copy[lok][1] == 0:
                lok = random.randint(0, len(SL_copy) - 1)
                itr += 1
                if itr > 1000:
                    print("ERROR - infinity loop in DL")

            SL_copy[lok][1] -= 1
            result.DL[i] = lok


    def mutate_wag(self, result):

        for i in range(self.n):

            max_packages = 0
            actually_packages = 0
            DT_copy = copy.deepcopy(result.DT[i])
            DP_copy = copy.deepcopy(result.DP[i])
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

                while self.sum_w_capacity(result.DW[i]) < max_packages:

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

                    result.DW[i][random_id] += 1
                    SW_copy[random_id][1] -= 1


    def sum_w_capacity(self, DW):

        capacity = 0

        for i in range(len(self.SW)):
            capacity += self.SW[i][2] * DW[i]
            
        return capacity