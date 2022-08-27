from multiprocessing import Process, Manager
from typing import List, Tuple, Dict
import random
import math
import time
from unittest import result

## Typagem
individuo = List[str]
individuo_processado = Tuple[individuo, int, int]

class AlgoritmoGenetico:

    def __init__(
            self, 
            qtd_geracoes : int = 5, 
            qtd_individuos : int = 4,
            menor : int = -10,
            maior : int = 10,
            porct_crossover : float = 0.7,
            porct_mutacao : float = 0.01,
            random_seed : int = None
        ) -> None:
        ## Valores de configuração
        self._qtd_geracoes = qtd_geracoes
        self._qtd_individuos = qtd_individuos if qtd_individuos%2 == 0 else qtd_individuos + 1 ## Verificação e certificação que sempre haja uma quantidade par de individuos a serem criados 
        self._menor = menor
        self._maior = maior
        self._porct_crossover = porct_crossover
        self._porct_mutacao = porct_mutacao
        random.seed(random_seed)
        #################################

    def set_qtd_individuos(self, qtd_individuos): ## Metodo para setar a quantidade de individuos presentes nas gerações
        self._qtd_individuos = qtd_individuos

    def set_qtd_geracoes(self, qtd_geracoes): ## Metodo para setar a quantidade de gerações
        self._qtd_geracoes = qtd_geracoes

    @property
    def _cria_individuo(self) -> individuo: ## Cria um individuo, que terá um valor entre os parametros menor e maior, essa valor será em binário.
        size_individuo = len(format(max(abs(self._menor), abs(self._maior)), "b")) + 1 ## pega a quantidade de bits necessária para representa o maior valor, +1 do bit de negativo ou positivo
        valor_int = random.randint(self._menor, self._maior) ## Escolhe um valor entre os limites inferiores (menor) e superior (maior)
        valor_bin = [x for x in "{:0{}b}".format(abs(valor_int) & 2 ** size_individuo - 1, size_individuo)] ## Transoforma o número inteiro em binário com o tamanho de bits o tamanho de bits calculado, e salva em uma lista
        valor_bin[0] = "1" if valor_int < 0 else "0" ## Adiciona o bit de verificação se o número é negativo ou não, esse bit é o primeiro bit do vetor
        return valor_bin

    def _convert_int(self, individuo : individuo) -> int: ## Converte o valor binário em inteiro
        valor_str = "".join(x for x in individuo[1:]) ## Transforma o valor binário que está na lista em uma string, o bit de verificação se é negativo não é processado
        valor_int = int(valor_str, 2) ## Converte o valor binário (que está em uma string) em inteiro
        valor_int *= -1 if individuo[0] == "1" else 1 ## Verifica se o valor é negativo ou não, no bit de verificação se o número é negativo ou não
        return valor_int

    def _fitness(self, valor_int : int) -> int: ## Realiza a função fitness
        return (valor_int**2) - (3*valor_int) + 4

    def _rodeio(self, lista_individuos : List[individuo_processado]) -> individuo: ## Realiza o rodeio, escolhendo 2 individuos e devolvendo o melhor adaptado
        roleta = []
        for individuo in lista_individuos: ## Cria uma roleta com base na porcentagem destinada a cada individuo, ou porção destinada da roleta ao individuo
            for i in range(individuo[2]):
                roleta.append(individuo[:2])
        escolha_1 = random.choice(roleta) ## Seleciona um individuo
        escolha_2 = random.choice(roleta) ## Seleciona um individuo
        return escolha_1[0].copy() if escolha_1[1] > escolha_2[1] else escolha_2[0].copy() ## Devolve o individuo mais bem adaptado dos individuos selecionados

    def _verifica_valor(self, individuo : individuo) -> bool: ## Verifica se o valor não extrapolou os limites
        valor_int = self._convert_int(individuo) ## Converte o valor em binário para inteiro
        return True if (self._menor <= valor_int <= self._maior) else False ## Devolve True, caso o valor esteja dentro do limite e False caso contrário

    def _crossover(self, individuo_1 : individuo, individuo_2 : individuo) -> Tuple[individuo, individuo]: ## Realiza o crossover entre 2 individuos
        qtd_posicoes = math.ceil(len(individuo_1) * self._porct_crossover) ## Calcula quantas posições devem ser trocadas entre os individuos
        posicoes_trocadas = []
        aux_individuo_1 = individuo_1.copy() ## Realiza a cópia do individuo 1
        aux_individuo_2 = individuo_2.copy() ## Realiza a cópia do individuo 2
        for i in range(qtd_posicoes):
            posicao = random.randint(0, len(individuo_1) - 1) ## Escolhe um posição aleatória dos individuos para ser trocada
            while posicao in posicoes_trocadas: ## Não permite que troque a mesma posição mais de uma vez
                posicao = random.randint(0, len(individuo_1) - 1)
            ## Realiza a troca de posições - Inicio
            aux = aux_individuo_1[posicao]
            aux_individuo_1[posicao] = aux_individuo_2[posicao]
            aux_individuo_2[posicao] = aux
            ############################## - Fim
            posicoes_trocadas.append(posicao)
        ## Retorna os filhos gerados do crossover, verificando se o valor deles não extrapolou os limites, caso extrapole retorna o valor sem crossover
        return aux_individuo_1 if self._verifica_valor(aux_individuo_1) else individuo_1, aux_individuo_2 if self._verifica_valor(aux_individuo_2) else individuo_2

    def _mutacao(self, lista_individuos : List[individuo]) -> List[individuo]: ## Realiza a mutação de um individuo
        posicao_individuo = random.randint(0, len(lista_individuos) - 1) ## Escolhe aleatoriamente qual individuo soferá a mutação
        aux_individuo = lista_individuos[posicao_individuo].copy() ## Realiza a cópia do individuo
        qtd_posicoes = math.ceil(len(aux_individuo) * self._porct_mutacao) ## Calcula quantas posições deve ser mutadas
        posicoes_trocadas = []
        for i in range(qtd_posicoes):
            posicao = random.randint(0, len(aux_individuo) - 1)
            while posicao in posicoes_trocadas: ## Escolhe um posição aleatória dos individuos para ser trocada
                posicao = random.randint(0, len(aux_individuo) - 1) ## Não permite que troque a mesma posição mais de uma vez
            ## Realiza a mutação de posições - Inicio
            aux_individuo[posicao] = "1" if aux_individuo[posicao] == "0" else "0"
            ############################## - Fim
            posicoes_trocadas.append(posicao)
        ## Verifica se a mutação no individuo não extrapolou os limites, caso extrapole desfaz a mutação
        lista_individuos[posicao_individuo] = aux_individuo if self._verifica_valor(aux_individuo) else lista_individuos[posicao_individuo]
        return lista_individuos

    def _cria_filho(self, lista_individuos : List[individuo_processado], processo_paralelo : bool = False, retorno_processo : Dict[int, List[individuo]] = None, index : int = None) -> Tuple[individuo, individuo]: ## Gera os filhos, realizando os rodeios e o crossover, para criação dos filhos dos individuos selecionados
        escolha_1 = self._rodeio(lista_individuos) ## Escolhe um individuo
        escolha_2 = self._rodeio(lista_individuos) ## Escolhe um individuo
        resultado = self._crossover(escolha_1, escolha_2) ## Realiza o crossover
        if processo_paralelo: ## Verifica se trata de um processo paralelo
            retorno_processo[index] = resultado ## Retorno para caso a chamada seja via processo em paralelo
        return resultado

    def _processa_individuo(self, lista_individuos : List[individuo]) -> List[individuo_processado]:
        somatorio_resultados = 0 ## Armazena os resultados do individuos na função fitness
        for index, individuo in enumerate(lista_individuos): ## Realiza o fitness dos individuos da geração
            lista_individuos[index] = (individuo, self._fitness(self._convert_int(individuo)))
            somatorio_resultados += lista_individuos[index][1]
        return [(individuos[0], individuos[1], round((individuos[1]/somatorio_resultados) * self._qtd_individuos)) for individuos in lista_individuos] ## Realiza um processamento estético no individuo, para facilitar no processamento

    @property
    def start(self) -> Tuple[List[individuo], float]:
        inicio = time.time() ## Pega o tempo inicial
        lista_individuos = [self._cria_individuo for individuo in range(self._qtd_individuos)] ## Lista de individuos da população
        for geracao in range(self._qtd_geracoes): ## Percorre as gerações
            lista_individuos = self._processa_individuo(lista_individuos) ## Realiza o processamento dos individuos da geração
            novos_individuos = [] ## Armazerna os novos individuos
            while len(novos_individuos) < self._qtd_individuos: ## Gera os x filhos
                novos_individuos += self._cria_filho(lista_individuos) ## Cria 2 filhos
            lista_individuos = self._mutacao(novos_individuos) ## Realiza  amutação em um dos filhos
        fim = time.time() ## Pega o tempo final
        return lista_individuos, fim - inicio
        
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
            random_seed : int = None,
            qtd_processos : int = 2
        ) -> None:
        AlgoritmoGenetico.__init__(self, qtd_geracoes, qtd_individuos, menor, maior, porct_crossover, porct_mutacao, random_seed)
        self._qtd_processos = qtd_processos ## Quantidade de processo a ser criado

    def set_qtd_processos(self, qtd_processos : int) -> None: ## Seta a quantidade de processos a serem utilizados no processamento do AGP
        self._qtd_processos = qtd_processos

    @property
    def start(self) -> Tuple[List[individuo], float]:
        inicio = time.time() ## Pega o tempo inicial
        lista_individuos = [self._cria_individuo for individuo in range(self._qtd_individuos)] ## Lista de individuos da população
        lista_processos = [None for x in range(self._qtd_processos)] ## Cria a lista que irá armazenar os processos
        ## - IMPORTANTE -
        ## Criação da váriavel compartilhavel entre os processos - Inicio
        retorno_processos = Manager().dict() ## Cria a váriavel compartilhavel entre os processos
        ############################## - Fim
        for geracao in range(self._qtd_geracoes): ## Percorre as gerações
            lista_individuos = self._processa_individuo(lista_individuos) ## Realiza o processamento dos individuos da geração
            novos_individuos = [] ## Armazerna os novos individuos
            while len(novos_individuos) < self._qtd_individuos: ## Gera os x filhos
                ## Realiza a criação dos filhos, utilizando de processos para execução paralela, cada processo irá cria dois filhos
                ## Criação de processos - Inicio
                for index_processo in range(self._qtd_processos): ## Cria os processos e os executa
                    lista_processos[index_processo] = Process(target=self._cria_filho, args=(lista_individuos, True, retorno_processos, index_processo))
                    lista_processos[index_processo].start()
                for index_processo in range(self._qtd_processos): ## Espera os processos terminarem a execução, e obtém os resultados
                    lista_processos[index_processo].join()
                    novos_individuos += retorno_processos[index_processo]
                    lista_processos[index_processo].close()
                ############################## - Fim 
            lista_individuos = self._mutacao(novos_individuos) ## Realiza  amutação em um dos filhos
        fim = time.time() ## Pega o tempo final
        return lista_individuos, fim - inicio