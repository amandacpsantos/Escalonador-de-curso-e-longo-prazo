from PoliticaFCFS import PoliticaFCFS

class PoliticaPrioridade(PoliticaFCFS):

    def __init__(self, listaProcesso, listaEvento, multiprogramacao):
        super().__init__(listaProcesso, listaEvento, multiprogramacao)


    def __ioOrdenadoPrioridade(self):
        listaPrioridade =[]

        for processo in self.filaProntos:
            listaPrioridade.append([processo, self.dictProcesso.get(processo)[3]])

        #organizar fila de prontos pela priopridade
        listaPrioridade = sorted(listaPrioridade, key=lambda sort: sort[1], reverse=True)


        for processo in listaPrioridade:
            index = listaPrioridade.index(processo)
            listaPrioridade[index] = processo[0]

        self.filaProntos = listaPrioridade.copy()

    def tcp(self):
        self.__ioOrdenadoPrioridade()

        tempo = self.tempoAtual + int(self.listaEvento[1])

        # processo entrando na CPU
        if self.cpu[0] == 0 and len(self.filaProntos) > 0:
            self.tempoAtual += int(self.listaEvento[1])
            self.cpu[0] = self.filaProntos.pop()

            # saber qual pico da CPU está
            if self.dictProcesso[self.cpu[0]][0] != 0:
                self.cpu[1] = int(self.dictProcesso[self.cpu[0]][0]) + self.tempoAtual
                self.dictProcesso[self.cpu[0]][0] = 0
            else:
                self.cpu[1] = int(self.dictProcesso[self.cpu[0]][2]) + self.tempoAtual
                self.dictProcesso[self.cpu[0]][2] = 0

        # processo saindo da CPU
        else:
            # se ja passou pelos dois picos
            if self.dictProcesso[self.cpu[0]][0] == 0 and self.dictProcesso[self.cpu[0]][2] == 0:
                # fazer TPR
                self.tpr()
            else:
                self.io.append([self.cpu[0], int(self.dictProcesso[self.cpu[0]][1]) + self.tempoAtual])
                self.cpu[0] = 0
                self.cpu[1] = 0

        self.tempoAtual = tempo
