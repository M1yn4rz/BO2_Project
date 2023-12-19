import graph as gp
import model as md
import pandas as pd
import random
import networkx as nx
import os
import matplotlib.pyplot as plt
import copy
import sys
sys.setrecursionlimit(10000)



class Algorithm:

    def __init__(self, SL, SW, n):

        self.graph = gp.Graph()
        self.__data = pd.read_csv('data\data.csv')
        self.__data_n = len(self.__data)

        self.SC = []
        self.SL = SL
        self.SW = SW
        self.SP = []
        self.SG = self.graph.G

        self.n = n

        self.solve_SC()
        self.solve_SP()

        self.AG()


    def AG(self):

        size_population = 1000
        epochs = 50

        first_population = self.generate_firt_population(size_population)

        actually_population = first_population

        list_min_f = []
        list_max_f = []
        list_mean_f = []
        X = [i + 1 for i in range(epochs)]

        percent = 0

        for per in range(epochs):

            if int(per/epochs*100) != percent:
                os.system('cls' if os.name == 'nt' else 'clear')
                percent = int((per + 1)/epochs*100)
                print('\nGenerate new epochs process:', percent, '%')

            actually_population = self.sort(actually_population)

            actually_population = actually_population[:len(actually_population)//5]
            population_to_mutate = copy.deepcopy(actually_population)

            while len(actually_population) < size_population:

                actually_population.append(self.mutate_population(population_to_mutate))

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
        
    
    def mutate_population(self, population):

        result_id = random.randint(0, len(population) - 1)

        return self.mutate_points(population[result_id])

    def mutate_points(self, result):
        
        new_result = copy.deepcopy(result)

        for _ in range(5):
            train1 = random.randint(0, self.n - 1)
            itr = 0
            while len(new_result.HP[train1]) == 0:
                train1 = random.randint(0, self.n - 1)
                itr += 1
                if itr > 1000:
                    print("ERROR - infinity loop in mutate points")
            train2 = random.randint(0, self.n - 1)
            itr = 0
            while train1 == train2:
                train2 = random.randint(0, self.n - 1)
                itr += 1
                if itr > 1000:
                    print("ERROR - infinity loop in mutate points")
            point_id = random.randint(0, len(new_result.HP[train1]) - 1)
            new_result.HP[train2].append(new_result.HP[train1][point_id])
            del new_result.HP[train1][point_id]
        
        for _ in range(2):
            train = random.randint(0, self.n - 1)
            random.shuffle(new_result.HP[train])

        for i in range(self.n):
            new_result.DT[i] = self.generate_track(new_result.HP[i], 4)

        return new_result

    def mutate_lok(self, result):
        pass


    def mutate_wag(self, result):
        pass


    def sort(self, population):
        def quicksort(population):
            if len(population) <= 1:
                return population
            else:
                pivot = population[0]
                less = [x for x in population[1:] if x.f <= pivot.f]
                greater = [x for x in population[1:] if x.f > pivot.f]
                return quicksort(less) + [pivot] + quicksort(greater)
        return quicksort(population)


    def generate_track(self, points, start):

        main_path = [start]

        for elem in points:

            permit = True
            first = None

            for point in main_path:
                if point == elem[0]:
                    first = point
                if first and point == elem[1]:
                    permit = False

            if permit:

                shortest_path = nx.shortest_path(self.SG, source=elem[0], target=elem[1], weight='weight')
                connection_path = nx.shortest_path(self.SG, source=main_path[-1], target=shortest_path[0], weight='weight')
                main_path.extend(connection_path[1:-1])
                main_path.extend(shortest_path)

        end_path = nx.shortest_path(self.SG, source=main_path[-1], target=start, weight='weight')
        main_path.extend(end_path[1:])

        previous = None
        to_delete = []

        for i in range(len(main_path)):
            if main_path[i] == previous:
                to_delete.append(i)
            previous = main_path[i]

        to_delete.reverse()

        for i in to_delete:
            del main_path[i]

        result_path = []

        for i in range(len(main_path) - 1):
            result_path.append([main_path[i], main_path[i + 1]])

        return result_path


    def generate_firt_population(self, size_population):

        first_population = []
        goal_functions = []
        percent = 0

        for per in range(size_population):

            if int(per/size_population*100) != percent:
                os.system('cls' if os.name == 'nt' else 'clear')
                percent = int((per + 1)/size_population*100)
                print('\nGenerate first population process:', percent, '%')
                
            one_result = md.Model(self.SC, self.SL, self.SW, self.n, self.SG)

            HP = [[] for _ in range(self.n)]
            points = []
            
            for i in range(self.__data_n):
                for value in self.SP[i + 1]:
                    points.append([i + 1, value[0], value[1]])

            for elem in points:
                random_id = random.randint(0, 5)
                HP[random_id].append(elem[:-1])
                if elem[0] not in one_result.DP[random_id].keys():
                    one_result.DP[random_id][elem[0]] = []
                one_result.DP[random_id][elem[0]].append([elem[1], elem[2]])

            one_result.HP = HP
            
            for i in range(len(HP)):
                one_result.DT[i] = self.generate_track(HP[i], 4)

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
                
            first_population.append(one_result)

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

        return first_population


    def sum_w_capacity(self, DW):
        capacity = 0
        for i in range(len(self.SW)):
            capacity += self.SW[i][2] * DW[i]
        return capacity


    def solve_SC(self):

        self.SC = [[0, 0] for _ in range(self.__data_n)]

        for i in range(self.__data_n):
            self.SC[i][0] = self.__data['Coordinate_X'][i]
            self.SC[i][1] = self.__data['Coordinate_Y'][i]


    def solve_SP(self):

        self.SP = {}

        for i in range(self.__data_n):

            lst = self.__data['Packages_to_sent'][i].split(';')
            
            self.SP[i + 1] = []

            for elem in lst:
                
                key, value = elem.split(':')
                self.SP[i + 1].append([int(key), int(value)])