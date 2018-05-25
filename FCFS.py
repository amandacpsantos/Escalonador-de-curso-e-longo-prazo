from File import File as f

# pegar informações do arquivo de entrada
nameFileIn = "in.txt"
arquivo = f(nameFileIn)
listaProcesso = arquivo.getProcess()
listaEvento = arquivo.getOperation()
multiprogramacao = int(arquivo.getMultProcess())


def imprime(tempoAtual, filaMemoria, filaProntos, cpu, io,cont):
    print(str(cont) + " : " +
        str(tempoAtual) + " -- " + str(filaMemoria) + " -- " + str(filaProntos) + " -- EVENTO -- " + str(cpu) + " -- " + str(
            io))


def checkTempoIo(io, cpu):
    for processo in io:
        # se o termino do tempo da CPU for maior que outro processo precisa sair da IO.
        if cpu[1] >= processo[1]:
            return [processo[0], io.index(processo) ]

    return [0]


def cpr(filaMemoria, filaProntos, listaSJF, tempoAtual, listaEvento):
    tempoAtual = tempoAtual + int(listaEvento[0])

    processo = listaSJF.pop()[0]
    filaMemoria.insert(0, processo)
    filaProntos.insert(0, processo)

    return tempoAtual


def tcp(filaProntos, tempoAtual, dictProcesso, cpu, io, filaMemoria, listaEvento):
    tempo = tempoAtual + int(listaEvento[1])

    # processo entrando na CPU
    if cpu[0] == 0 and len(filaProntos) > 0:
        tempoAtual = tempoAtual + int(listaEvento[1])
        cpu[0] = filaProntos.pop()


        # saber qual pico da CPU está
        if dictProcesso[cpu[0]][0] != 0:
            cpu[1] = int(dictProcesso[cpu[0]][0]) + tempoAtual
            dictProcesso[cpu[0]][0] = 0
        else:
            cpu[1] = int(dictProcesso[cpu[0]][2]) + tempoAtual
            dictProcesso[cpu[0]][2] = 0

    # processo saindo da CPU
    else:
        # se ja passou pelos dois picos
        if dictProcesso[cpu[0]][0] == 0 and dictProcesso[cpu[0]][2] == 0:
            # fazer TPR
            tempo = tpr(tempoAtual, cpu, filaMemoria, listaEvento)
        else:
            io.append([ cpu[0], int(dictProcesso[cpu[0]][1]) + tempoAtual ])
            cpu[0] = 0
            cpu[1] = 0


    return tempo


def tpr(tempoAtual, cpu, filaMemoria, listaEvento):
    cpu[0] = 0
    cpu[1] = 0
    filaMemoria.pop()
    return tempoAtual + int(listaEvento[2])


def ioToProntos(processo, filaProntos):
    #print("Antes >> {}".format(filaProntos))
    filaProntos.insert(0, processo)
    #print("Depois >> {}".format(filaProntos))

    return filaProntos


tempoAtual = 0
filaMemoria = []
filaProntos = []
cpu = [0, 0]
evento = []
io = []
listaSJF = []

# adicionar o tempo total no final da lista de cada processo.
for lista in listaProcesso:
    lista.append(int(lista[1]) + int(lista[3]))

# lista para escalonamento de longo prazo usando SJF
listaSJF = sorted(listaProcesso, key=lambda sort: sort[5], reverse=True)

# dicionario com processo como chave e os valores relacionados a ele
dictProcesso = {}
for processo in listaProcesso:
    dictProcesso[processo[0]] = processo[1:]

cont = 0
checkMemoria = 1

while checkMemoria!= 0 :

    # verificar se há algum processo do io pronto para ir pra fila de prontos entre processos da cpu
    if len(io) > 0:

        io = sorted(io, key=lambda sort: sort[1], reverse=False)

        for processo in io:
            if processo[1] <= tempoAtual:
                filaProntos = ioToProntos(processo[0], filaProntos)
                io.pop(io.index(processo))

        if cpu[0] ==0 and len(filaProntos) ==0:
            filaProntos = ioToProntos(io[0][0], filaProntos)
            io.pop(0)


    # verificar se a memoria tem espaço e realizar o cpr
    if len(filaMemoria) < multiprogramacao and len(listaSJF) > 0:
        tempoAtual = cpr(filaMemoria, filaProntos, listaSJF, tempoAtual, listaEvento)
    else:
        # verificar se há processo para ir para a fila de prontos
        if len(io) > 0:
            processoFromIO = checkTempoIo(io, cpu)

            # se houver processo com tempo menor que o que estiver na cpu
            if (processoFromIO[0] != 0):
                ioToProntos(processoFromIO[0], filaProntos)
                io.pop(processoFromIO[1])


        # verificar se a cpu está vazio ou cheia
        if cpu[0] == 0:
            if len(filaProntos) > 0:
                tempoAtual = tcp(filaProntos, tempoAtual, dictProcesso, cpu, io, filaMemoria, listaEvento)
        else:
            tempoAtual = cpu[1]
            tempoAtual = tcp(filaProntos, tempoAtual, dictProcesso, cpu, io, filaMemoria, listaEvento)

    cont += 1
    imprime(tempoAtual, filaMemoria, filaProntos, cpu, io, cont)

    if len(filaMemoria) ==0 and len(io) == 0 and cpu[0] == 0: checkMemoria = 0



print(dictProcesso)
