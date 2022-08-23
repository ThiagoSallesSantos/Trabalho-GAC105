from AlgoritmoGenetico import AlgoritmoGenetico, AlgoritmoGeneticoParalelo

if __name__ == "__main__":
    ## Algoritmo Genetico em Sequencial
    AG = AlgoritmoGenetico(random_seed=7)
    print("Tempo de execução sequencial: " + str(AG.start[1]))
    ## Algoritmo Genetico em Paralelo
    AGP = AlgoritmoGeneticoParalelo(random_seed=7)
    print("Tempo de execução paralelo: " + str(AGP.start[1]))
