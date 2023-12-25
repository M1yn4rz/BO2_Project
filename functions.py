import networkx as nx



class Functions:


    def __init__(self):

        pass


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