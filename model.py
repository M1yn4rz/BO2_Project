import graph as gp
import math
import networkx as nx



class Model:


    def __init__(self, SC, SL, SW, n, SG):

        self.SG = SG

        self.n = n
        self.f = 0

        self.SC = SC
        self.SL = SL
        self.SW = SW

        self.HF = [0 for _ in range(self.n)]
        self.HL = [0 for _ in range(self.n)]
        self.HP = []

        self.DL = [0 for _ in range(self.n)]
        self.DW = [[0 for _ in range(len(SW))] for _ in range(self.n)]
        self.DT = [0 for _ in range(self.n)]
        self.DP = [{} for _ in range(self.n)]


    def goal_function(self):

        self.f = sum(self.HF)

        return self.f


    def solve_HF(self, i):

        self.HF[i] = 0

        HV = 0

        for j in range(len(self.SW)):
            HV += self.SW[j][0] * self.DW[i][j]

        self.HF[i] = (self.SL[self.DL[i]][0] + HV) * self.HL[i] / 100

        return self.HF


    def solve_HL(self, i):

        self.HL[i] = 0

        if not self.DT[i]:
            self.HL[i] = 0
            return 0

        path = [self.DT[i][0][0]]

        for elem in self.DT[i]:
            path.append(elem[1])

        for j in range(len(path) - 1):
            
            current_node = path[j]
            next_node = path[j + 1]

            if self.SG.has_edge(current_node, next_node):
                self.HL[i] += self.SG[current_node][next_node]['weight']
            else:
                raise ValueError(f"Edge {current_node} -> {next_node} not found in the graph.")
            
        return self.HL[i]
    

    def __str__(self):
        str_ = ""
        str_ += "\nThe best result:"
        str_ += "\n\n\tNumber of trains: " + str(self.n)
        str_ += "\n\n\tGoal function value: " + str(round(self.f, 3))
        str_ += "\n\n\tStatistics in individual trains:\n"
        for i in range(self.n):
            str_ += "\n\t\tTrain " + str(i + 1)
            str_ += "\t- " + "distance : " + str(self.HL[i]) + " km"
            str_ += "\t- " + "fuel : " + str(self.HF[i]) + " L"
            str_ += "\t- " + "locomotive : " + str(self.DL[i])
            str_ += "\t- " + "wagons : " + str(self.DW[i])
        str_ += "\n\n\tTracks in individual trains:"
        for i in range(self.n):
            str_ += "\n\n\t\tTrain " + str(i + 1) + " :\n"
            str_ += "\n" + str(self.DT[i])
        return str_