 
#  Trabalho Prático - GAC105

 Trabalho prático da matéria GAC105 (Programação Paralela e Concorrente) da Universidade Federal de Lavras.

## Sumário
1. [Autores](#autores)  
2. [Objetivo](#objetivo)
3. [Estrutura do Projeto](#estrutura-do-projeto)
4. [Requisitos](#requisitos)
5. [Preparação do Ambiente](#preparação-do-ambiente)
6. [Execução](#execução)

    6.1. [Executar o arquivo src/main.py](#executar-o-arquivo-srcmainpy)

    6.2. [Executar o arquivo src/AnaliseDesempenho.ipynb](#executar-o-arquivo-srcanalisedesempenhoipynb)

## Autores

- [Chrystian Amaral](https://github.com/chrystian9)
- [Pedro Alves](https://github.com/Hedrobyte)
- [Thiago Salles Santos](https://github.com/ThiagoSallesSantos)

## Objetivo 

Projeto tem como objetivo a realização de análise de desempenho entre dois algoritmos genéticos, sendo um a implementação do outro, porém com uso de  multi-processos. Código de inspiração para este trabalho se ecnontra no repositório [ GCC128-AlgoritmoGenetico
](https://github.com/ThiagoSallesSantos/GCC128-AlgoritmoGenetico).

## Estrutura do Projeto

Estrutura dos arquivos utilizada no projeto:

- src/
    - AlgoritmoGenetico.py
    - AnaliseDesempenho.ipynb
    - main.py
    - resultados.json *
- .gitignore
- README.md
- requirements.txt 

Obs: * Podem variar ou não se encontrar entre os arquivos padrões. 

## Requisitos

- python 3.10.4 ou superior
- python virtualenv 

## Preparação do Ambiente

Clonar o repositório

~~~bash  
git clone https://github.com/ThiagoSallesSantos/Trabalho-GAC105
~~~

Criar um ambiente virtual em python

~~~bash  
python3 -m venv venv
~~~

Iniciar o ambiente virtual em python

Linux:

~~~bash  
source venv/bin/activate
~~~

Windows: 

~~~bash  
venv/Scripts/activate
~~~

Fazer a instalação das dependências

~~~bash  
pip install -r requirements.txt
~~~    

## Execução

Para a execução do projeto existe dois arquivos que podem serem executados:

- __src/main.py__: Finalidade de realizar testes comparativos simples entre os algoritmos sequenciais e paralelos.

- __src/AnaliseDesempenho.ipynb__: Finalidade de realizar testes mais completos, gerar resultados em formato json, e montar gráficos comparativos entre algoritmos sequenciais e paralelos

### Executar o arquivo _src/main.py_

Executando o comando:

~~~bash  
python3 src/main.py
~~~

### Executar o arquivo _src/AnaliseDesempenho.ipynb_

Executando o comando:

~~~bash  
jupyter notebook
~~~

Ou usar uma extensão/aplicação que der suporte, ao uso de notebook em python.

Posteriormente, com a aplicação de suporte ao notebook de sua prefência, basta selecionar o arquivo _src/AnaliseDesempenho.ipynb_, e executar as cédulas.