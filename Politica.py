import copy as c


class Politica(object):


    def __init__(self, listaProcesso, listaEvento, multiprogramacao):
        self.listaProcesso = c.deepcopy(listaProcesso)
        self.listaEvento = listaEvento
        self.multiprogramacao = multiprogramacao
        self.listaSJF = self.getListaSJF()
        self.dictProcesso = self.getDictProcesso()
        self.somatorio = self.getSoma()

        # -----------------------------------------------

        self.tempoAtual = 0
        self.filaMemoria = []
        self.filaProntos = []
        self.cpu = [0, 0]
        self.evento = []
        self.io = []
        self.values = []
        self.cont = 0


    def getSoma(self):
        listaSoma = []
        for key in self.dictProcesso:
            soma = sum(list(map(int, self.dictProcesso[key]))[0:3])
            listaSoma.append(soma)

        return listaSoma


    def getListaSJF(self):

        # Add ao processo o tempo total de CPU
        for lista in self.listaProcesso:
            lista.append(int(lista[1]) + int(lista[3]))

        # Lista para escalonamento de longo prazo usando SJF
        listaSJF = sorted(self.listaProcesso, key=lambda sort: sort[5], reverse=True)
        return listaSJF

    def getDictProcesso(self):
        # Gerar um dicionario com todas informações sendo o numero do processo a chave
        dictP = {}
        for processo in self.listaProcesso:
            dictP[processo[0]] = processo[1:]
        return dictP

    def imprime(self):
        print(str(self.cont) + " : " +
              str(self.tempoAtual) + " -- " +
              str(self.filaMemoria) + " -- " +
              str(self.filaProntos) + " -- EVENTO -- " +
              str(self.cpu) + " -- " + str(self.io))

    def checkTempoIo(self):
        for processo in self.io:
            # Se o termino do tempo da CPU for maior que outro processo precisa sair da I/O.
            if self.cpu[1] >= processo[1]:
                return [processo[0], self.io.index(processo)]
        return [0]

    def cpr(self):
        self.tempoAtual = int(self.tempoAtual + int(self.listaEvento[0]))

        processo = self.listaSJF.pop()[0]
        self.filaMemoria.insert(0, processo)
        self.filaProntos.insert(0, processo)

    def checkValues(self, processo, time):
        self.values.append([processo, time])

    def tcp(self):
        tempo = self.tempoAtual + int(self.listaEvento[1])

        # Processo entrando na CPU
        if self.cpu[0] == 0 and len(self.filaProntos) > 0:
            tempoAtual = self.tempoAtual + int(self.listaEvento[1])
            self.cpu[0] = self.filaProntos.pop()

            # Saber qual pico da CPU está
            if self.dictProcesso[self.cpu[0]][0] != 0:
                self.cpu[1] = int(self.dictProcesso[self.cpu[0]][0]) + tempoAtual
                self.dictProcesso[self.cpu[0]][0] = 0
            else:
                self.cpu[1] = int(self.dictProcesso[self.cpu[0]][2]) + tempoAtual
                self.dictProcesso[self.cpu[0]][2] = 0

        # Processo saindo da CPU
        else:
            # Se ja passou pelos dois picos
            if self.dictProcesso[self.cpu[0]][0] == 0 and self.dictProcesso[self.cpu[0]][2] == 0:
                # Fazer TPR
                self.tpr()
            else:
                self.io.append([self.cpu[0], int(self.dictProcesso[self.cpu[0]][1]) + self.tempoAtual])
                self.cpu[0] = 0
                self.cpu[1] = 0

        self.tempoAtual = int(tempo)

    def tpr(self):
        # Zera a CPU, remove da memoria o processo e atualiza o tempo
        processo = self.cpu[0]
        self.cpu[0] = 0
        self.cpu[1] = 0
        self.filaMemoria.remove(processo)
        tempo = int(self.tempoAtual + int(self.listaEvento[2]))
        self.checkValues(processo,tempo)
        return tempo

    def ioToProntos(self, processo):
        self.filaProntos.insert(0, processo)

    def executa(self):

        checkMemoria = 1

        while checkMemoria != 0:
            # Verificar se há algum processo do I/O pronto para ir pra Fila de Prontos entre processos da CPU
            if len(self.io) > 0:

                self.io = sorted(self.io, key=lambda sort: sort[1], reverse=False)

                # Verificar se há algum processo já disponivel para Fila de Prontos
                for processo in self.io:
                    if processo[1] <= self.tempoAtual:
                        self.ioToProntos(processo[0])
                        self.io.pop(self.io.index(processo))
                # Verificar se o processador e o CPU estão vazios para pular o tempo do proximo processo no I/O
                if self.cpu[0] == 0 and len(self.filaProntos) == 0:
                    self.ioToProntos(self.io[0][0])
                    self.tempoAtual = self.io[0][1]
                    self.io.pop(0)

            # Verificar se a memoria tem espaço e realizar o CPR
            if len(self.filaMemoria) < self.multiprogramacao and len(self.listaSJF) > 0:
                self.cpr()

            else:
                # Verificar se há processo para ir para a Fila de Prontos
                if len(self.io) > 0:
                    processoFromIO = self.checkTempoIo()

                    # Se houver processo com tempo menor que o que estiver na CPU
                    if processoFromIO[0] != 0:
                        self.ioToProntos(processoFromIO[0])
                        self.io.pop(processoFromIO[1])

                # Verificar se a CPU está vazio ou cheia
                if self.cpu[0] == 0:
                    if len(self.filaProntos) > 0:
                        self.tcp()
                else:
                    self.tempoAtual = int(self.cpu[1])
                    self.tcp()

            self.cont += 1

            if len(self.filaMemoria) == 0 and len(self.io) == 0 and self.cpu[0] == 0:
                checkMemoria = 0



        lOrd = self.values = sorted(self.values, key=lambda sort: sort[0], reverse=False)

        lValue = []

        for lista in lOrd:
            lValue.append(lista[1])

        l = zip(lValue, self.somatorio)

        tEstimado = []

        for tupla in l:
            tEstimado.append(tupla[0] - tupla[1])

        return tEstimado



