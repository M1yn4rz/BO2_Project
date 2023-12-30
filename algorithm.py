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
import os
import threading
import queue



sys.setrecursionlimit(10000)



class Algorithm:


    def __init__(self, n):

        self.load_csv = ld.Load_csv()
        self.graph = gp.Graph()

        self.SL = self.load_csv.read_locomotives()
        self.SW = self.load_csv.read_wagons()
        self.SP = self.load_csv.read_packages()
        self.SC = self.load_csv.read_coordinates()
        self.SG = self.graph.G

        self.n = n
        self.fn = fn.Functions(n, self.SW)
        self.fp = fp.First_population(self.n, 
                    self.SL, self.SW, self.SP, self.SC, self.SG)


    def AG(self, size_population = 1000, epochs = 50, previous_population = 5, mutate_power = 5, start = 4):

        population = self.fp.generate_first_population(size_population, start)

        actually_population = population
        previous_population = int(previous_population / 100 * size_population)

        mutate_power = int(mutate_power / 100 * self.n * 10)

        list_min_f = []
        list_max_f = []
        list_mean_f = []
        X = [i + 1 for i in range(epochs)]

        percent = 0

        for per in range(epochs):

            if per/epochs*100 >= percent:
                os.system('cls' if os.name == 'nt' else 'clear')
                percent = int((per + 1)/epochs*100)
                print('\nGenerate new epochs process :', percent, '%')
                print('Actually epoch :', per + 1, '/', epochs, ': All epochs')

            actually_population = self.fn.sort(actually_population)
            actually_population = actually_population[:previous_population]
            population_to_mutate = copy.deepcopy(actually_population)

            args = (population_to_mutate, mutate_power, start)

            while len(actually_population) < size_population:
                actually_population.append(self.mutate_population(args))

            for result in actually_population:

                for i in range(self.n):
                    result.solve_HL(i)
                    result.solve_HF(i)

                result.goal_function()

            goal_functions = [x.f for x in actually_population]

            list_min_f.append(min(goal_functions))
            list_max_f.append(max(goal_functions))
            list_mean_f.append(sum(goal_functions)/len(goal_functions))

        # plt.plot(X, list_min_f, label = 'Najmniejsza funkcja celu danej populacji')
        # plt.plot(X, list_max_f, label = 'Największa funkcja celu danej populacji')
        # plt.plot(X, list_mean_f, label = 'Średnia funkcja celu danej populacji')
        # plt.title('Wykres funkcji celu kolejnych populacji')
        # plt.xlabel('Numer populacji')
        # plt.ylabel('Wartość funkcji celu')
        # plt.legend()
        # plt.grid()
        # plt.show()

        best_id = goal_functions.index(min(goal_functions))
        best_result = actually_population[best_id]

        for i in range(self.n):
            print("\n", i, ":", best_result.DT[i])

        return best_result
    

    def start_AG(self, size_population = 1000, previous_population = 5, mutate_power = 5, start = 4):

        population = self.fp.generate_first_population(size_population, start)
        previous_population = int(previous_population / 100 * size_population)
        mutate_power = int(mutate_power / 100 * self.n * 10)

        return population, previous_population, mutate_power
    

    def loop_AG(self, actually_population, size_population, previous_population, mutate_power, start = 4):

        actually_population = self.fn.sort(actually_population)
        actually_population = actually_population[:previous_population]
        population_to_mutate = copy.deepcopy(actually_population)

        args = (population_to_mutate, mutate_power, start)
        results_queue = queue.Queue()

        loop = (size_population - len(actually_population))//7
        loops = [loop for _ in range(7)]

        for i in range((size_population - len(actually_population)) - sum(loops)):
            loops[i] += 1

        threads = []

        for i in range(7):
            threads.append(threading.Thread(target=self.generate_population_in_thread, args=(args, loops[i], results_queue)))

        for i in range(7):
            threads[i].start()

        for i in range(7):
            threads[i].join()

        for _ in range(7):
            actually_population.extend(results_queue.get())

        for result in actually_population:

            for i in range(self.n):
                result.solve_HL(i)
                result.solve_HF(i)

            result.goal_function()

        return actually_population
    

    def generate_population_in_thread(self, args, loops, queue):
        lst = []
        for _ in range(loops):
            lst.append(self.mutate_population(args))
        queue.put(lst)


    def mutate_population(self, args):

        population, mutate_power, start = args
        result_id = random.randint(0, len(population) - 1)

        return self.mutate_points(population[result_id], mutate_power, start)


    def mutate_points(self, result, mutate_power, start):
        
        new_result = copy.deepcopy(result)

        for _ in range(mutate_power * 2):

            train_max_track = new_result.HL.index(max(new_result.HL))
            train_min_track = new_result.HL.index(min(new_result.HL))

            point_id = random.randint(0, len(new_result.HP[train_max_track]) - 1)
            new_result.HP[train_min_track].append(new_result.HP[train_max_track][point_id])
            del new_result.HP[train_max_track][point_id]

            new_result.DT[train_max_track] = self.fn.generate_track(new_result.HP[train_max_track], start, self.SG)
            new_result.DT[train_min_track] = self.fn.generate_track(new_result.HP[train_min_track], start, self.SG)
            new_result.solve_HL(train_max_track)
            new_result.solve_HL(train_min_track)
            new_result.solve_HF(train_max_track)
            new_result.solve_HF(train_min_track)
        
        for _ in range(mutate_power):

            train_max_track = new_result.HL.index(max(new_result.HL))
            test_result = copy.deepcopy(new_result)

            random.shuffle(test_result.HP[train_max_track])
            test_result.DT[train_max_track] = self.fn.generate_track(test_result.HP[train_max_track], start, self.SG)
            test_result.solve_HL(train_max_track)

            itr = 0

            while test_result.HL[train_max_track] > new_result.HL[train_max_track]:

                random.shuffle(test_result.HP[train_max_track])
                test_result.DT[train_max_track] = self.fn.generate_track(test_result.HP[train_max_track], start, self.SG)
                test_result.solve_HL(train_max_track)
                itr += 1

                if itr > 10:
                    break

            if itr < 10:
                new_result = copy.deepcopy(test_result)
                new_result.solve_HF(train_max_track)

        self.mutate_locomotives(new_result, mutate_power)
        self.fn.attaching_wagons(new_result)

        return new_result


    def mutate_locomotives(self, result, mutate_power):

        SL_copy = copy.deepcopy(self.SL)
        itr = 0

        for _ in range(mutate_power):

            i = random.randint(0, self.n - 1)
            lok = random.randint(0, len(SL_copy) - 1)

            while SL_copy[lok][1] == 0:
                lok = random.randint(0, len(SL_copy) - 1)
                itr += 1
                if itr > 100:
                    print("ERROR - infinity loop in DL")

            SL_copy[lok][1] -= 1
            result.DL[i] = lok