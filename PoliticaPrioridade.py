from Politica import Politica

class PoliticaPrioridade(Politica):

    def __init__(self, listaProcesso, listaEvento, multiprogramacao):
        super().__init__(listaProcesso, listaEvento, multiprogramacao)


    def ioToProntos(self, processo):
        self.filaProntos.insert(0, processo)
        if self.cpu[0] != 0:
            #verificar se há um processo na fila de prontos com maior prioridade

            if self.__verifivarPreempcao() == True:

                #print(self.dictProcesso)
                devolTempo = self.cpu[1] - self.tempoAtual

                if self.dictProcesso[self.cpu[0]][2] == 0:
                    self.dictProcesso[self.cpu[0]][2] = devolTempo
                else:
                    self.dictProcesso[self.cpu[0]][0] = devolTempo

                #tcp para tirar da cpu
                self.tcp()
                #tcp para colocar na cpu
                self.tcp()

                #print(self.dictProcesso)
                self.cont += 1

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

    def __verifivarPreempcao(self):
        prioridadeCPU = self.dictProcesso[self.cpu[0]][3]
        #print('Proceso na cpu {} tem priopridade {}'.format(self.cpu[0],prioridadeCPU))

        for processo in self.filaProntos:
            #print('Proceso {} tem priopridade {}'.format(processo, self.dictProcesso[processo][3]))

            #verificar se o processo da fila de prontos tem maior prioridade que o da cpu
            if self.dictProcesso[processo][3] < prioridadeCPU:
                return True
        return False

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
                #passar o processo da cpu e gravar com o tempo que ele deve sair
                self.io.append([self.cpu[0], int(self.dictProcesso[self.cpu[0]][1]) + self.tempoAtual])
                self.cpu[0] = 0
                self.cpu[1] = 0

        self.tempoAtual = tempo

