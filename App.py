from PoliticaFCFS import PoliticaFCFS as pF
from PoliticaPrioridade import PoliticaPrioridade as pP
from PoliticaRoundRobin import PoliticaRoundRobin as pR
import copy as c


class App(object):
    def __init__(self, listaProcesso, listaEvento, multiprogramacao):
        self.listaValues = []
        self.__listaProcesso = c.deepcopy(listaProcesso)
        self.__listaEvento = listaEvento
        self.__multiprogramacao = multiprogramacao

    def executa(self):
        pol1 = pF(self.__listaProcesso, self.__listaEvento, self.__multiprogramacao)
        pol2 = pP(self.__listaProcesso, self.__listaEvento, self.__multiprogramacao)
        pol3 = pR(self.__listaProcesso, self.__listaEvento, self.__multiprogramacao)

        return [pol1.executa(),
                pol2.executa(),
                pol3.executa()]
