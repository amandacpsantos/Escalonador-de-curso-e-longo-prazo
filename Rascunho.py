from File import File as f
import copy as c
import numpy as np

#nameFileIn ou nameFileOut pode ou não ser passado.
#Caso não há, o nome padrão é in.txt e out.txt respectivamente.

nameFileIn = "in.txt"
arquivo = f(nameFileIn)

tempoEventos = arquivo.getOperation()
multProgramacao = int(arquivo.getMultProcess())
listaDadosProcessos = sorted(arquivo.getProcess(), key=lambda sort: sort[4],reverse=1)
tempoEventos = arquivo.getOperation()

#--------------------------------------------------------
#MEMÓRIA / PRONTO / EVENTOS / CPU / ES / INICIO / FIM /
tabela=[
        [[],[],"",0,[],0,0]
                            ]
#--------------------------------------------------------


numLinhaTabela = 0


#TODO
# MUDAR listaDadosProcessos para numProcessos.
while listaDadosProcessos.__len__()!=0:

    #SE A MEMÓRIA ESTIVER MENOR QUE A MULTIPROGRAMAÇÃO
    linhaTabela = c.deepcopy(tabela[numLinhaTabela])

    if linhaTabela[0].__len__() < multProgramacao:

        # CRIAR PROCESSO EM EVENTO:
        linhaTabela[2] = "CPR-"+listaDadosProcessos[-1][0]

        # ADD O TEMPO DE CRIAÇÃO
        linhaTabela[-2] = tabela[numLinhaTabela][-1]
        linhaTabela[-1] += int(tempoEventos[0])
        tabela.append(linhaTabela)
        numLinhaTabela += 1

        # CRIAR LINHA+1 COM O PROCESSO NA MEMÓRIA E NA FILA DE PRONTO
        proxLinha = c.deepcopy(tabela[numLinhaTabela])
        proxLinha[0].append(listaDadosProcessos[-1][0])
        proxLinha[1].append(listaDadosProcessos[-1][0])
        proxLinha[2] = ""
        proxLinha[-2] = proxLinha[-1]
        proxLinha[-1] += int(tempoEventos[0])

        # ADD LINHA NA TABELA
        tabela.append(proxLinha)
        numLinhaTabela += 1
        #print(tabela)

        listaDadosProcessos.pop()


    else:
        #TODO
        # Tratar trocar de contexto pra CPU
        # Lista de espera
        # Finalizar processos para o if reconhecer que há mais.
        # tirar esse break horroroso que está aí só pra testar a primeira parte
        print("Limite memória")
        break

print("\n------- TABELA -------")
print(np.array(tabela))





