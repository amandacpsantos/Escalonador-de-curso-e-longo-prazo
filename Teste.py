from File import File as f
from PoliticaFCFS import PoliticaFCFS as pF
from PoliticaPrioridade import PoliticaPrioridade as pP
from PoliticaRoundRobin import PoliticaRoundRobin as pR


# pegar informações do arquivo de entrada
nameFileIn = "in.txt"
arquivo = f(nameFileIn)
listaProcesso = arquivo.getProcess()
listaEvento = arquivo.getOperation()
multiprogramacao = int(arquivo.getMultProcess())

pol = pF(listaProcesso, listaEvento, multiprogramacao)
pol.executa()

pol2 = pP(listaProcesso, listaEvento, multiprogramacao)
pol2.executa()

print('\n\n-------------------\n\n')

pol3 = pR(listaProcesso, listaEvento, multiprogramacao)
pol3.executa()
