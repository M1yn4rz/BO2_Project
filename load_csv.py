import pandas as pd



class Load_csv:


    def __init__(self):

        self.__data = pd.read_csv('data\data.csv')
        self.__data_n = len(self.__data)


    def read_coordinates(self):

        coordinates = [[0, 0] for _ in range(self.__data_n)]

        for i in range(self.__data_n):
            coordinates[i][0] = self.__data['Coordinate_X'][i]
            coordinates[i][1] = self.__data['Coordinate_Y'][i]
        
        return coordinates


    def read_packages(self):

        packages = {}

        for i in range(self.__data_n):

            lst = self.__data['Packages_to_sent'][i].split(';')
            packages[i + 1] = []

            for elem in lst:
                key, value = elem.split(':')
                packages[i + 1].append([int(key), int(value)])

        return packages