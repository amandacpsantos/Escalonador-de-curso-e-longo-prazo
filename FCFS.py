from File import File as f
#pegar informações do arquivo de entrada
nameFileIn = "in.txt"
arquivo = f(nameFileIn)
listaProcesso = arquivo.getProcess()
listaEvento = arquivo.getOperation()
multiprogramacao = int(arquivo.getMultProcess())


def imprime(tempoAtual, filaMemoria, filaProntos):
    print(str(tempoAtual) + " | " + str(filaMemoria) + " | " + str(filaProntos) + " | " )

def checkTempoIo(io, cpu, tempoEvento = 0):
    numtempo = 0
    if (tempoEvento > 0):
        numtempo = tempoEvento
    else:
        numtempo = cpu[1]

    for processo in io:
        #se o termino do tempo da CPU for maior que outro processo precisa sair da IO.
        if cpu[1] >= io[processo]:
            return processo
    return 0

def cpr(filaMemoria, filaProntos, listaSJF, tempoAtual, tempoExec = int(listaEvento[0]) ):
    tempoAtual = tempoAtual + tempoExec

    #TODO COLOCAR CHECK TEMPO IO

    processo = listaSJF.pop()[0]
    filaMemoria.insert(0,processo)
    filaProntos.insert(0,processo)

    return tempoAtual

def ioToProntos(processo, filaProntos):
    filaProntos.insert(0,processo)

def tcp(filaProntos, tempoAtual, dictProcesso, cpu):
    tempoAtual = tempoAtual + 5
    resul = checkTempoIo(cpu, tempoAtual)
    if resul == 0:
        cpu[0] = filaProntos.pop()
        cpu[1] = dictProcesso[cpu[0]][0] + tempoAtual

def tpr(processo, tempoAtual = 0, tempoExec = listaEvento[2]):
    pass

tempoAtual = 0
filaMemoria = []
filaProntos = []
cpu = [0,0]
evento = []
io = {}
listaSJF = []

print(filaMemoria)
print(filaProntos)
print(tempoAtual)

#adicionar o tempo total no final da lista de cada processo.
for lista in listaProcesso:
    lista.append(int(lista[1]) + int(lista[3]))

#lista para escalonamento de longo prazo
listaSJF = sorted(listaProcesso, key=lambda sort: sort[5],reverse=True)

dictProcesso = {}
for processo in listaProcesso:
   dictProcesso[processo[0]] = processo[1:]

while len(listaSJF) > 0:
    #verificar se a memoria tem espaço e realizar o cpr
    if(len(filaMemoria) < multiprogramacao):
        tempoAtual = cpr(filaMemoria, filaProntos, listaSJF, tempoAtual)

    #verificar se há processo para ir para a fila de prontos
    if(len(io) > 0) :
        processoFromIO = checkTempoIo(io, cpu)
        #se houver processo com tempo menor que o que estiver na cpu
        if(processoFromIO !=0):
            ioToProntos(processoFromIO, filaProntos)

    #verificar se a cpu está


    imprime(tempoAtual, filaMemoria, filaProntos)


    break