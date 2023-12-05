import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import networkx as nx
import pandas as pd
import math



class Graph:

    def __init__(self):
        self.__image = mpimg.imread("data\poland.png")
        self.G = nx.Graph()
        self.__data = pd.read_csv('data\data.csv')
        self.add_nodes()
        self.add_edges()

    def add_nodes(self):
        for i in range(16):
            self.__G.add_node(i + 1, 
                              coordinates = (self.__data['Coordinate_X'][i], 
                                             self.__data['Coordinate_Y'][i]),
                              label = self.__data['City'][i])

    def add_edges(self):
        for i in range(16):
            lst = []
            lst = self.__data['Connections'][i].split(';')
            for elem in lst:
                elem = int(elem)
                weight = math.sqrt((self.__data['Coordinate_X'][i] - self.__data['Coordinate_X'][elem - 1])**2
                                   + (self.__data['Coordinate_Y'][i] - self.__data['Coordinate_Y'][elem - 1])**2)
                self.__G.add_edge(i + 1, elem, weight = int(weight / 2.9724))


    def print(self, way = None):
        plt.figure()
        plt.imshow(self.__image)
        pos = nx.get_node_attributes(self.__G, 'coordinates')
        edge_labels = {(u, v): d['weight'] for u, v, d in self.__G.edges(data=True)}
        nx.draw(self.__G, pos = pos, with_labels = True)
        if way:
            nx.draw_networkx_edges(self.__G, pos = pos, edgelist = way, width = 3, edge_color = 'red')
        nx.draw_networkx_edge_labels(self.__G, pos = pos, edge_labels = edge_labels, font_color = 'red', font_size = 7)
        plt.axis('off')
        plt.show()
        return ""