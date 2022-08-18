from AlgoritmoGenetico import AlgoritmoGenetico
from AlgoritmoGeneticoParalelo import AlgoritmoGeneticoParalelo

if __name__ == "__main__":
    AG = AlgoritmoGenetico(random_seed=7)
    AGP = AlgoritmoGeneticoParalelo(random_seed=7)
    print("Tempo de execução sequencial: " + str(AG.start))
    print("Tempo de execução paralelo: " + str(AGP.start))
