from AlgoritmoGenetico import AlgoritmoGenetico
from ThreadReturn import ThreadReturn
from typing import List, Tuple
import time

## Typagem
individuo = List[str]

## Classe AlgoritmoGeneticoParalelo, herda de AlgoritmoGenetico e implementa o paralelismo
class AlgoritmoGeneticoParalelo(AlgoritmoGenetico):

    def __init__(
            self, 
            qtd_geracoes : int = 5, 
            qtd_individuos : int = 4,
            menor : int = -10,
            maior : int = 10,
            porct_crossover : float = 0.7,
            porct_mutacao : float = 0.01,
            qtd_elementos_roleta : int = 10, ## Configuração adicional para definir a quantidade de elementos na roleta
            random_seed : int = None
        ) -> None:
        AlgoritmoGenetico.__init__(self, qtd_geracoes, qtd_individuos, menor, maior, porct_crossover, porct_mutacao, qtd_elementos_roleta, random_seed)

    def _cria_filhos(self, lista_individuos : List[individuo]) -> Tuple[individuo, individuo] :
        thread_1 = ThreadReturn(target=self._rodeio, args=(lista_individuos,)) ## Escolhe um individuo usando thread
        thread_2 = ThreadReturn(target=self._rodeio, args=(lista_individuos,)) ## Escolhe um individuo usando thread
        thread_1.start()
        thread_2.start()
        return self._crossover(thread_1.join(), thread_2.join()) ## Realiza o crossover

    @property
    def start(self) -> float:
        inicio = time.time()
        lista_individuos = [] ## Lista de individuos na geração
        for geracao in range(self._qtd_geracoes):
            if not lista_individuos: ## Cria os individuos, caso não existam
                ## Criando os individuos utilizando thread - Inicio
                lista_threads = [] ## Lista de threads
                for i in range(self._qtd_individuos):
                    lista_threads.append(ThreadReturn(target=self._cria_individuo)) ## Cria uma thread, com a tarefa de criar um individuo
                    lista_threads[-1].start() ## Inicia a operação da thread
                for thread in lista_threads:
                    lista_individuos.append(thread.join()) ## Espera a thread termina de executar e salva o valor resultante
                ############################## - Fim
            novos_individuos = []
            lista_threads = []
            ## Criando os filhos utilizando threads - Inicio
            for i in range(int(self._qtd_individuos/2)): ## Gera os filhos, realizando os rodeios e o crossover, para criação dos filhos dos individuos selecionados
                lista_threads.append(ThreadReturn(target=self._cria_filhos, args=(lista_individuos,))) ## Cria uma thread, com a tarefa de criar um filho
                lista_threads[-1].start() ## Inicia a operação da thread
            for thread in lista_threads:
                novos_individuos += thread.join() ## Espera a thread termina de executar e salva o valor resultante
            ############################## - Fim
            lista_individuos = self._mutacao(novos_individuos) ## Realiza  amutação em um dos filhos
        fim = time.time()
        return fim - inicio