import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import networkx as nx
import pandas as pd
import math



class Graph:


    def __init__(self):

        self.__image = mpimg.imread("data\poland.png")
        self.G = nx.DiGraph()
        self.__data = pd.read_csv('data\data.csv')
        self.__data_length = len(self.__data)
        self.add_nodes()
        self.add_edges()


    def add_nodes(self):

        for i in range(self.__data_length):
            self.G.add_node(i + 1, 
                              coordinates = (self.__data['Coordinate_X'][i], 
                                             self.__data['Coordinate_Y'][i]),
                              label = self.__data['City'][i],
                              size = self.__data['Vertex_Size'][i])


    def add_edges(self):

        for i in range(self.__data_length):

            lst = []
            lst = self.__data['Connections'][i].split(';')

            for elem in lst:
                elem = int(elem)
                weight = math.sqrt((self.__data['Coordinate_X'][i] - self.__data['Coordinate_X'][elem - 1])**2
                                   + (self.__data['Coordinate_Y'][i] - self.__data['Coordinate_Y'][elem - 1])**2)
                self.G.add_edge(i + 1, elem, weight = int(weight / 2.9724))


    def print(self, way = None):

        plt.figure()
        plt.imshow(self.__image)
        pos = nx.get_node_attributes(self.G, 'coordinates')
        edge_labels = {(u, v): d['weight'] for u, v, d in self.G.edges(data=True)}
        node_sizes = [self.G.nodes[node]['size'] for node in self.G.nodes]
        nx.draw(self.G, pos = pos, with_labels = True, node_size = node_sizes)

        if way:
            nx.draw_networkx_edges(self.G, pos = pos, edgelist = way, width = 3, edge_color = 'red')
            
        nx.draw_networkx_edge_labels(self.G, pos = pos, edge_labels = edge_labels, font_color = 'red', font_size = 7)
        plt.axis('off')
        plt.show()