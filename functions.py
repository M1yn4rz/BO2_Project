import networkx as nx
import copy
import random



class Functions:


    def __init__(self, n, SW):

        self.n = n

        self.SW = SW


    def generate_track(self, points, start, SG):

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

                shortest_path = nx.shortest_path(SG, source=elem[0], target=elem[1], weight='weight')
                connection_path = nx.shortest_path(SG, source=main_path[-1], target=shortest_path[0], weight='weight')
                main_path.extend(connection_path[1:-1])
                main_path.extend(shortest_path)

        end_path = nx.shortest_path(SG, source=main_path[-1], target=start, weight='weight')
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
    

    def attaching_wagons(self, result):

        for i in range(self.n):

            max_packages = 0
            actually_packages = 0
            DT_copy = copy.deepcopy(result.DT[i])
            DP_copy = copy.deepcopy(result.DP[i])
            SW_copy = copy.deepcopy(self.SW)
            DP_actually = {}
            result.DW[i] = [0 for _ in range(len(self.SW))]

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

            while self.sum_wagon_capacity(result.DW[i]) < max_packages:

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

    
    def sum_wagon_capacity(self, DW):

        capacity = 0

        for i in range(len(self.SW)):
            capacity += self.SW[i][2] * DW[i]
            
        return capacity