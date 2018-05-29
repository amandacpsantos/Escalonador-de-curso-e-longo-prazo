from Politica import Politica


class PoliticaFCFS(Politica):

    def __init__(self, listaProcesso, listaEvento, multiprogramacao):
        super().__init__(listaProcesso, listaEvento, multiprogramacao)

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
