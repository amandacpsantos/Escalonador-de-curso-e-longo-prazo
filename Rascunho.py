lista_processo = []
operacoes_so = []

ref_arquivo = open("in.txt","r")

#PEGAR QTD MULTIP
multP = ref_arquivo.readline().split('=')[1]


#SEPARAR PROCESSOS E OPERACOES
linha = ref_arquivo.readline()
while linha.__len__() != 2:
    lista_processo.append(linha)
    linha = ref_arquivo.readline()

linha = ref_arquivo.readline()
while linha:
    operacoes_so.append(linha)
    linha = ref_arquivo.readline()

ref_arquivo.close()

# -------------------------------------------------

#LIMPAR DADOS
lista_processo.pop(0)
operacoes_so.pop(0)



#TRATAR CADA PROCESSO
lista_dados_processos = []

for processo in lista_processo:
    limp1 = processo.split('=')[1]

    limp2 = limp1.split(",")
    print(limp2.__str__())

    listaProcessoUnico = []

    for valor in limp2:
        print(valor)
        listaProcessoUnico.append(valor.split("-")[0])
        if ";" in valor:
            listaProcessoUnico.append(valor[-2])

    lista_dados_processos.append(listaProcessoUnico)

print(lista_dados_processos.__str__())




#TRATAR CADA OPERAÇÃO
lista_dados_operacoes = []
for operacao in  operacoes_so:
    limp1 = operacao.split("=")[1]
    lista_dados_operacoes.append(limp1[0])


print(lista_dados_operacoes.__str__())
