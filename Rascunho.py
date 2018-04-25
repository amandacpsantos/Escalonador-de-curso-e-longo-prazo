from File import File as f
import copy as c
import numpy as np

#nameFileIn ou nameFileOut pode ou não ser passado.
#Caso não há, o nome padrão é in.txt e out.txt respectivamente.

nameFileIn = "in.txt"
arquivo = f(nameFileIn)

tempoEventos = arquivo.getOperation()
multProgramacao = int(arquivo.getMultProcess())

# ORDENAÇÃO PELO NÚMERO DE CHEGADA
listaDadosProcessos = sorted(arquivo.getProcess(), key=lambda sort: sort[4],reverse=True)


# TABELA CONSULTA DADOS E PICO CPU / LISTA DE IDS
listaID = []
dictInfor = {}
for processo in listaDadosProcessos:
    dictInfor[processo[0]] = ['0', processo[1],processo[2],processo[3] ]
    listaID.append(processo[0])
print(dictInfor)
print(listaID)

#--------------------------------------------------------
#DISPOSIÇÃO DA TABELA
#MEMÓRIA / PRONTO / EVENTOS / CPU / ES / INICIO / FIM /
tabela=[
        [[],[],"",-1,{},0,0]
                            ]
#--------------------------------------------------------

numLinhaTabela = 0
check = 0

while len(listaID) !=0 and check < 13:

    #TRABALHA EM CIMA SEMPRE DE UMA NOVA LINHA
    linhaTabela = c.deepcopy(tabela[numLinhaTabela])

    #SE A MEMÓRIA ESTIVER MENOR QUE A MULTIPROGRAMAÇÃO
    if len(linhaTabela[0]) < multProgramacao:

        ### CRIAR PROCESSO NA COLUNA EVENTO:
        linhaTabela[2] = "CPR-"+ listaID[-1]

        # ADD O TEMPO DE CRIAÇÃO
        linhaTabela[-2] = tabela[numLinhaTabela][-1]
        linhaTabela[-1] += int(tempoEventos[0])
        tabela.append(linhaTabela)
        numLinhaTabela += 1

        ### CRIAR LINHA+1 COM O PROCESSO NA MEMÓRIA E NA FILA DE PRONTO
        proxLinha = c.deepcopy(tabela[numLinhaTabela])
        proxLinha[0].append(listaID[-1])

        # INSERE NO [0] PARA USAR O .POP E PEGAR QUEM CHEGOU PRIMEIRO
        proxLinha[1].insert(0,listaID[-1])

        proxLinha[2] = ""

        proxLinha[-2] = proxLinha[-1]
        proxLinha[-1] += int(tempoEventos[0])

        # ADD LINHA NA TABELA
        tabela.append(proxLinha)
        numLinhaTabela += 1
        #print(tabela)

        listaID.pop()

    #SE A CPU ESTIVER VAZIA E A TIVER PROCESSO NA FILA DE PRONTOS
    elif linhaTabela[3] == -1 and len(linhaTabela[1]) > 0:

        ### CRIAR ALOCAÇÃO DE PROCESSO NA CPU NA COLUNA EVENTO:
        processoAtual = linhaTabela[1].pop()
        linhaTabela[2] = "TCP-" + processoAtual

        # ADD O TEMPO DE EVENTO TCP
        linhaTabela[-2] = linhaTabela[-1]
        linhaTabela[-1] += int(tempoEventos[1])
        tabela.append(linhaTabela)
        numLinhaTabela += 1

        proxLinha = c.deepcopy(tabela[numLinhaTabela])

        # PARA ALOCAR O PROCESSO DA CPU É PRECISO VERIFICAR SE HÁ ALGUM PROCESSO NA ESPERA PARA MARCAR O TEMPO DE TCP
        # DA COLUNA ES. SE A COLUNA DE E/S ESTIVER VAZIA, ACRESCENTAR ALL TEMPO DO PICO DO PROCESSO.

        #SE NÃO HOUVER PROCESSO EM ESPERA
        if len(proxLinha[4]) == 0:
            proxLinha[2] = ""
            proxLinha[3] = processoAtual

            #VERICAR SE É O PRIMEIRO OU SEGUNDO PICO
            if dictInfor[proxLinha[3]][0] == "0": #SE FOR O PRIMEIRO PICO
                dictInfor[proxLinha[3]][0] = "1"


                # ADD TEMPO DO PRIMEIRO PICO
                proxLinha[-2] = proxLinha[-1]
                proxLinha[-1] += int(dictInfor[proxLinha[3]][1])

                # ZERAR O TEMPO DO PRIMEIRO PICO
                dictInfor[proxLinha[3]][1] = "0"

            elif dictInfor[proxLinha[3]][0] == "1": #SE FOR O SEGUNDO PICO
                dictInfor[proxLinha[3]][0] = "2"

                # ADD TEMPO DO SEGUNDO PICO
                proxLinha[-2] = proxLinha[-1]
                proxLinha[-1] += int(dictInfor[proxLinha[3]][3])

                # ZERAR O TEMPO DO SEGUNDO PICO
                dictInfor[proxLinha[3]][3] = "0"

            tabela.append(proxLinha)
            numLinhaTabela += 1

        #SE HOUVER PROCESSO EM ESPERA
        elif proxLinha[4].__len__() != 0:
            pass

    # SE A CPU ESTIVER CHEIA
    elif linhaTabela[3] != -1:
        processoAtual = linhaTabela[3]
        linhaTabela[4][processoAtual] = linhaTabela[-1] + int(dictInfor[processoAtual][2])
        linhaTabela[3] = -1
        print(linhaTabela)
        tabela.append(linhaTabela)
        numLinhaTabela += 1



    check += 1


print("\n------- TABELA -------")
print(np.array(tabela))
#print(dictInfor)