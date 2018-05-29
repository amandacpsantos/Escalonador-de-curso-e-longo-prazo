from Politica import Politica


class PoliticaRoundRobin(Politica):

    def __init__(self, listaProcesso, listaEvento, multiprogramacao):
        super().__init__(listaProcesso, listaEvento, multiprogramacao)

    def tcp(self):

        tempo = self.tempoAtual + int(self.listaEvento[1])

        # Processo entrando na CPU
        if self.cpu[0] == 0 and len(self.filaProntos) > 0:
            self.tempoAtual = self.tempoAtual + int(self.listaEvento[1])
            self.cpu[0] = self.filaProntos.pop()

            # Saber qual pico da CPU está
            if int(self.dictProcesso[self.cpu[0]][0]) != 0:
                self.cpu[1] = 20 + self.tempoAtual
                # Verifica quanto de tempo resta para execução do primero pico
                # Se for maior que 20 reduz apenas 20 do tempo, se for igual ou menor, reduz o tempo restante
                if int(self.dictProcesso[self.cpu[0]][0]) > 20:
                    self.dictProcesso[self.cpu[0]][0] = int(self.dictProcesso[self.cpu[0]][0]) - 20
                else:
                    self.dictProcesso[self.cpu[0]][0] = int(self.dictProcesso[self.cpu[0]][0]) - int(self.dictProcesso[self.cpu[0]][0])
            else:
                # Verifica quanto de tempo resta para execução do segundo pico
                # Se for maior que 20 reduz apenas 20 do tempo, se for igual ou menor, reduz o tempo restante
                self.cpu[1] = 20 + self.tempoAtual
                if int(self.dictProcesso[self.cpu[0]][2]) > 20:
                    self.dictProcesso[self.cpu[0]][2] = int(self.dictProcesso[self.cpu[0]][2]) - 20
                else:
                    self.dictProcesso[self.cpu[0]][2] = int(self.dictProcesso[self.cpu[0]][2]) - int(self.dictProcesso[self.cpu[0]][2])

                # Processo saindo da CPU
        else:
            # Se ja passou pelos dois picos
            if self.dictProcesso[self.cpu[0]][0] == 0 and self.dictProcesso[self.cpu[0]][2] == 0:
                # Fazer TPR
                self.tpr()
            else:
                if int(self.dictProcesso[self.cpu[0]][0]) == 0:
                    self.io.append([self.cpu[0], int(self.dictProcesso[self.cpu[0]][1]) + self.tempoAtual])
                else:
                    self.io.append([self.cpu[0], 20 + self.tempoAtual])
                self.cpu[0] = 0
                self.cpu[1] = 0

        self.tempoAtual = int(tempo)
