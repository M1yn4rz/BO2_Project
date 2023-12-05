import graph as gp
import model as md
import pandas as pd



class Algorithm:

    def __init__(self):

        self.graph = gp.Graph()
        self.__data = pd.read_csv('data\data.csv')

        self.SC = []
        #self.SL = 
        #self.SW = 
        #self.SP = 
        self.SG = self.graph.G


    def AG(self):

        pass


    def solve_SC(self):

        self.SC = [[0, 0] for i in range(16)]

        for i in range(16):
            self.SC[i][0] = self.__data['Coordinate_X'][i]
            self.SC[i][1] = self.__data['Coordinate_Y'][i]

