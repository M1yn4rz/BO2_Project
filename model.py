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

        self.HF = []
        self.HL = []

        self.DL = [0 for _ in range(self.n)]
        self.DW = [[0 for _ in range(len(SW))] for _ in range(self.n)]
        self.DT = [0 for _ in range(self.n)]
        self.DP = [{} for _ in range(self.n)]


    def goal_function(self):

        self.HL = [0 for _ in range(self.n)]
        self.HF = [0 for _ in range(self.n)]

        for i in range(self.n):
            self.solve_HL(i)
        
        for i in range(self.n):
            self.solve_HF(i)

        self.f = sum(self.HF)

        return self.f


    def solve_HF(self, i):

        HV = 0

        for j in range(len(self.SW)):
            HV += self.SW[j][0] * self.DW[i][j]

        self.HF[i] = (self.SL[self.DL[i]][0] + HV) * self.HL[i] / 100

        return self.HF


    def solve_HL(self, i):

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