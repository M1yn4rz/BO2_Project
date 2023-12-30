import graph as gp
import algorithm as ag
import pandas as pd



def main():

    new_ag = ag.Algorithm(n = 6)
    
    best_result = new_ag.AG(size_population = 1000, 
                            epochs = 100, 
                            previous_population = 1,
                            mutate_power = 10,
                            start = 4)

    g = gp.Graph()

    g.print(best_result.DT[0])
    g.print(best_result.DT[1])
    g.print(best_result.DT[2])
    g.print(best_result.DT[3])
    g.print(best_result.DT[4])
    g.print(best_result.DT[5])



if __name__ == "__main__":

    main()