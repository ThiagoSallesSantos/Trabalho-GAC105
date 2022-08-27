from AlgoritmoGenetico import AlgoritmoGenetico, AlgoritmoGeneticoParalelo

if __name__ == "__main__":
    qtd_gerecaos = 100
    qtd_individuos = 10000
    ## Algoritmo Genetico em Sequencial
    # AG = AlgoritmoGenetico(qtd_gerecaos, qtd_individuos, random_seed=7)
    # print("Tempo de execução sequencial: " + str(AG.start[1]))
    ## Algoritmo Genetico em Paralelo
    AGP = AlgoritmoGeneticoParalelo(qtd_gerecaos, qtd_individuos, random_seed=7, qtd_processos=4)
    print("Tempo de execução paralelo: " + str(AGP.start[1]))
