from PoliticaFCFS import PoliticaFCFS


class PoliticaRoundRobin(PoliticaFCFS):

    def __init__(self, listaProcesso, listaEvento, multiprogramacao):
        super().__init__(listaProcesso, listaEvento, multiprogramacao)

    def tcp(self):
        tempo = self.tempoAtual + int(self.listaEvento[1])

        # processo entrando na CPU
        if self.cpu[0] == 0 and len(self.filaProntos) > 0:
            self.tempoAtual = self.tempoAtual + int(self.listaEvento[1])
            self.cpu[0] = self.filaProntos.pop()

            # saber qual pico da CPU está
            if int(self.dictProcesso[self.cpu[0]][0]) != 0:
                self.cpu[1] = 20 + self.tempoAtual
                if int(self.dictProcesso[self.cpu[0]][0]) > 20:
                    self.dictProcesso[self.cpu[0]][0] = int(self.dictProcesso[self.cpu[0]][0]) - 20
                else:
                    self.dictProcesso[self.cpu[0]][0] = int(self.dictProcesso[self.cpu[0]][0]) - int(self.dictProcesso[self.cpu[0]][0])
            else:
                self.cpu[1] = 20 + self.tempoAtual
                if int(self.dictProcesso[self.cpu[0]][2]) > 20:
                    self.dictProcesso[self.cpu[0]][2] = int(self.dictProcesso[self.cpu[0]][2]) - 20
                else:
                    self.dictProcesso[self.cpu[0]][2] = int(self.dictProcesso[self.cpu[0]][2]) - int(self.dictProcesso[self.cpu[0]][2])

                # processo saindo da CPU
        else:
            # se ja passou pelos dois picos
            if self.dictProcesso[self.cpu[0]][0] == 0 and self.dictProcesso[self.cpu[0]][2] == 0:
                # fazer TPR
                self.tpr()
            else:
                if int(self.dictProcesso[self.cpu[0]][0]) == 0:
                    self.io.append([self.cpu[0], int(self.dictProcesso[self.cpu[0]][1]) + self.tempoAtual])
                else:
                    self.io.append([self.cpu[0], 20 + self.tempoAtual])
                self.cpu[0] = 0
                self.cpu[1] = 0

        self.tempoAtual = int(tempo)
