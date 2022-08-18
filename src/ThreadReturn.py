from threading import Thread

## Classe ThreadReturn implementa Thread, porém com adendo do retorno no metodo join
class ThreadReturn(Thread):

    def __init__(self, group=None, target=None, name=None,args=(), kwargs={}): ## Contrutor da classe
        Thread.__init__(self, group, target, name, args, kwargs) ## Cria uma thread
        self._return = None ## Variavel de retorno

    def run(self): ## Metodo de execução do metodo target, o .start() chama esse metodo
        if self._target is not None:
            self._return = self._target(*self._args,**self._kwargs) ## Pega o retorno do metodo target

    def join(self, *args): ## Metodo join, responsável por fazer esperar a execução da thread 
        Thread.join(self, *args) ## espera a execução da thread
        return self._return ## retorna o valor obtido na execução do metodo target