import graph as gp
import model as md
import pandas as pd
import random
import networkx as nx
import os
import matplotlib.pyplot as plt



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

        first_population, list_id = self.generate_firts_population(size_population = 10000)

        i = 0
        print('\nMin:\n')
        for elem in first_population[list_id[0]].DT:
            print('\n', i, ':', elem)
            i += 1

        i = 0
        print('\nMax:\n')
        for elem in first_population[list_id[1]].DT:
            print('\n', i, ':', elem)
            i += 1
        

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


    def generate_firts_population(self, size_population):

        first_population = []
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
            
            for i in range(self.__data_n):
                for value in self.SP[i][i + 1]:
                    points.append([i + 1, value[0]])

            for elem in points:
                HP[random.randint(0, 5)].append(elem)
            
            for i in range(len(HP)):
                one_result.DT[i] = self.generate_track(HP[i], 4)

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

        list_id = [0, 0]
        list_id[0] = goal_functions.index(min(goal_functions))
        list_id[1] = goal_functions.index(max(goal_functions))

        return first_population, list_id


    def solve_SC(self):

        self.SC = [[0, 0] for _ in range(self.__data_n)]

        for i in range(self.__data_n):
            self.SC[i][0] = self.__data['Coordinate_X'][i]
            self.SC[i][1] = self.__data['Coordinate_Y'][i]


    def solve_SP(self):

        self.SP = []

        for i in range(self.__data_n):

            lst = self.__data['Packages_to_sent'][i].split(';')
            dc = dict()
            dc[i + 1] = []

            for elem in lst:
                
                key, value = elem.split(':')
                dc[i + 1].append([int(key), int(value)])

            self.SP.append(dc)