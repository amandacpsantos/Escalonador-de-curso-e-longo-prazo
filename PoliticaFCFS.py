class PoliticaFCFS(object):

    def __init__(self, listaProcesso, listaEvento, multiprogramacao):
        self.listaProcesso = listaProcesso
        self.listaEvento = listaEvento
        self.multiprogramacao = multiprogramacao
        self.listaSJF = self.getListaSJF()
        self.dictProcesso = self.getDictProcesso()
        # -----------------------------------------------
        self.tempoAtual = 0
        self.filaMemoria = []
        self.filaProntos = []
        self.cpu = [0, 0]
        self.evento = []
        self.io = []

    def getListaSJF(self):
        # add ao processo o tempo total de CPU
        for lista in self.listaProcesso:
            lista.append(int(lista[1]) + int(lista[3]))

        # lista para escalonamento de longo prazo usando SJF
        listaSJF = sorted(self.listaProcesso, key=lambda sort: sort[5], reverse=True)
        return listaSJF

    def getDictProcesso(self):
        # gerar um dicionario com todas informações sendo o numero do processo a chave
        dictP = {}
        for processo in self.listaProcesso:
            dictP[processo[0]] = processo[1:]
        return dictP

    def __imprime(self, cont):
        print(str(cont) + " : " +
              str(self.tempoAtual) + " -- " +
              str(self.filaMemoria) + " -- " +
              str(self.filaProntos) + " -- EVENTO -- " +
              str(self.cpu) + " -- " + str(self.io))

    def checkTempoIo(self):
        for processo in self.io:
            # se o termino do tempo da CPU for maior que outro processo precisa sair da IO.
            if self.cpu[1] >= processo[1]:
                return [processo[0], self.io.index(processo)]

        return [0]

    def cpr(self):
        self.tempoAtual = int(self.tempoAtual + int(self.listaEvento[0]))

        processo = self.listaSJF.pop()[0]
        self.filaMemoria.insert(0, processo)
        self.filaProntos.insert(0, processo)

    def tcp(self):
        tempo = self.tempoAtual + int(self.listaEvento[1])

        # processo entrando na CPU
        if self.cpu[0] == 0 and len(self.filaProntos) > 0:
            self.tempoAtual = self.tempoAtual + int(self.listaEvento[1])
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

        self.tempoAtual = int(tempo)

    def tpr(self):
        self.cpu[0] = 0
        self.cpu[1] = 0
        self.filaMemoria.pop()
        self.tempoAtual = int(self.tempoAtual + int(self.listaEvento[2]))

    def ioToProntos(self, processo):
        self.filaProntos.insert(0, processo)
        # return filaProntos

    def executa(self):

        checkMemoria = 1
        cont = 0

        while checkMemoria != 0:

            # verificar se há algum processo do io pronto para ir pra fila de prontos entre processos da cpu
            if len(self.io) > 0:

                self.io = sorted(self.io, key=lambda sort: sort[1], reverse=False)

                for processo in self.io:
                    if processo[1] <= self.tempoAtual:
                        self.ioToProntos(processo[0])
                        self.io.pop(self.io.index(processo))

                if self.cpu[0] == 0 and len(self.filaProntos) == 0:
                    self.ioToProntos(self.io[0][0])
                    self.io.pop(0)

            # verificar se a memoria tem espaço e realizar o cpr
            if len(self.filaMemoria) < self.multiprogramacao and len(self.listaSJF) > 0:
                self.cpr()

            else:
                # verificar se há processo para ir para a fila de prontos
                if len(self.io) > 0:
                    processoFromIO = self.checkTempoIo()

                    # se houver processo com tempo menor que o que estiver na cpu
                    if processoFromIO[0] != 0:
                        self.ioToProntos(processoFromIO[0])
                        self.io.pop(processoFromIO[1])

                # verificar se a cpu está vazio ou cheia
                if self.cpu[0] == 0:
                    if len(self.filaProntos) > 0:
                        self.tcp()
                else:
                    self.tempoAtual = int(self.cpu[1])
                    self.tcp()

            cont += 1
            self.__imprime(cont)

            if len(self.filaMemoria) == 0 and len(self.io) == 0 and self.cpu[0] == 0:
                checkMemoria = 0

        print(self.dictProcesso)
