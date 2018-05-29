from Politica import Politica


class PoliticaPrioridade(Politica):

    def __init__(self, listaProcesso, listaEvento, multiprogramacao):
        super().__init__(listaProcesso, listaEvento, multiprogramacao)

    def ioToProntos(self, processo):
        self.filaProntos.insert(0, processo)
        if self.cpu[0] != 0:
            # Verificar se há um processo na fila de prontos com maior prioridade

            if self.__verifivarPreempcao() is True:

                devolTempo = self.cpu[1] - self.tempoAtual

                if self.dictProcesso[self.cpu[0]][2] == 0:
                    self.dictProcesso[self.cpu[0]][2] = devolTempo
                else:
                    self.dictProcesso[self.cpu[0]][0] = devolTempo

                # TCP para tirar da CPU
                self.tcp()
                # TCP para colocar na CPU
                self.tcp()

                self.cont += 1

    def __ioOrdenadoPrioridade(self):
        listaPrioridade = []

        for processo in self.filaProntos:
            listaPrioridade.append([processo, self.dictProcesso.get(processo)[3]])

        # Organizar Fila de Prontos pela priopridade
        listaPrioridade = sorted(listaPrioridade, key=lambda sort: sort[1], reverse=True)


        for processo in listaPrioridade:
            index = listaPrioridade.index(processo)
            listaPrioridade[index] = processo[0]

        self.filaProntos = listaPrioridade.copy()

    def __verifivarPreempcao(self):
        prioridadeCPU = self.dictProcesso[self.cpu[0]][3]

        for processo in self.filaProntos:

            # Verificar se o processo da Fila de Prontos tem maior prioridade que o da CPU
            if self.dictProcesso[processo][3] < prioridadeCPU:
                return True
        return False

    def tcp(self):
        self.__ioOrdenadoPrioridade()

        tempo = self.tempoAtual + int(self.listaEvento[1])

        # Processo entrando na CPU
        if self.cpu[0] == 0 and len(self.filaProntos) > 0:
            self.tempoAtual += int(self.listaEvento[1])
            self.cpu[0] = self.filaProntos.pop()

            # Saber qual pico da CPU está
            if self.dictProcesso[self.cpu[0]][0] != 0:
                self.cpu[1] = int(self.dictProcesso[self.cpu[0]][0]) + self.tempoAtual
                self.dictProcesso[self.cpu[0]][0] = 0
            else:
                self.cpu[1] = int(self.dictProcesso[self.cpu[0]][2]) + self.tempoAtual
                self.dictProcesso[self.cpu[0]][2] = 0

        # Processo saindo da CPU
        else:
            # se ja passou pelos dois picos
            if self.dictProcesso[self.cpu[0]][0] == 0 and self.dictProcesso[self.cpu[0]][2] == 0:
                # fazer TPR
                self.tpr()
            else:
                # Passar o processo da CPU e gravar com o tempo que ele deve sair
                self.io.append([self.cpu[0], int(self.dictProcesso[self.cpu[0]][1]) + self.tempoAtual])
                self.cpu[0] = 0
                self.cpu[1] = 0

        self.tempoAtual = tempo
