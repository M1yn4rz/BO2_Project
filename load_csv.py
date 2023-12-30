import pandas as pd



class Load_csv:


    def __init__(self):

        self.__data = pd.read_csv('data\data.csv')
        self.__data_n = len(self.__data)
        self.__packages = pd.read_csv('data\packages.csv')
        self.__packages_n = len(self.__packages)
        self.__locomotives = pd.read_csv('data/locomotives.csv')
        self.__wagons = pd.read_csv('data/wagons.csv')


    def read_coordinates(self):

        coordinates = [[0, 0] for _ in range(self.__data_n)]

        for i in range(self.__data_n):
            coordinates[i][0] = self.__data['Coordinate_X'][i]
            coordinates[i][1] = self.__data['Coordinate_Y'][i]
        
        return coordinates


    def read_packages(self):

        packages = {}

        for i in range(self.__packages_n):

            row = self.__packages.iloc[i]
            
            if row[0] not in packages.keys():
                packages[row[0]] = []

            packages[row[0]].append([row[2], row[4]])

        return packages
    

    def read_locomotives(self):
        return self.__locomotives.values.tolist()
    
    def read_wagons(self):
        return self.__wagons.values.tolist()