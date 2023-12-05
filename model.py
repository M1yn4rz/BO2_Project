import graph as gp
import math



class Model:


    def __init__(self, SC, SL, SW):

        self.n = 0
        self.f = 0

        self.SC = SC
        self.SL = SL
        self.SW = SW

        self.HF = []
        self.HL = []

        self.DL = []
        self.DW = []
        self.DT = []
        self.DP = []


    def goal_function(self):

        self.HL = [0 for k in range(self.n)]
        self.HF = [0 for k in range(self.n)]

        for i in range(self.n):
            self.solve_HL(i)
        
        for i in range(self.n):
            self.solve_HF(i)

        self.f = sum(self.HF)

        return self.f


    def solve_HF(self, i):

        HV = 0

        for j in range(len(self.SW)):
            HV += self.SW[j, 0] * self.DW[i][j]

        self.HF[i] = (self.SL[self.DL[i]] + HV) * self.HL[i]

        return self.HF


    def solve_HL(self, i):

        for j in self.DT[i]:
            self.HL[i] += math.sqrt((self.SC[self.DT[i][0]][0] - self.SC[self.DT[i][1]][0])**2 
                                    + (self.SC[self.DT[i][0]][1] - self.SC[self.DT[i][1]][1])**2)

        return self.HL