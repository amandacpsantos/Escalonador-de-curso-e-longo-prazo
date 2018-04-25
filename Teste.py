#https://github.com/amandacpsantos/Escalonador-de-curso-e-longo-prazo

from File import File as f

#TESTE MAPEAMENTO ARQUIVO ENTRADA

#nameFileIn ou nameFileOut pode ou não ser passado.
#Caso não há, o nome padrão é in.txt e out.txt respectivamente.

nameFileIn = "in.txt"

arquivo = f(nameFileIn)
print("Multiprogramação: {}".format(arquivo.getMultProcess()))
print("Lista de processos: {}".format(arquivo.getProcess()))
print("Lista de eventos: {}".format(arquivo.getOperation()))
arquivo.createOut()


#--------------------------------------------------------
#MEMÓRIA / PRONTO / EVENTOS / CPU / ES / INICIO / FIM /
tabela=[
        [[],[],"",0,[],0,0]                            ]
#--------------------------------------------------------



