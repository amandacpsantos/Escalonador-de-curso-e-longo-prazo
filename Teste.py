from File import File as f
import copy as c
import numpy as np

#nameFileIn ou nameFileOut pode ou não ser passado.
#Caso não há, o nome padrão é in.txt e out.txt respectivamente.

nameFileIn = "in.txt"

arquivo = f(nameFileIn)
print(arquivo.getMultProcess())
print(arquivo.getProcess())
print(arquivo.getOperation())
arquivo.createOut()


#--------------------------------------------------------
#MEMÓRIA / PRONTO / EVENTOS / CPU / ES / INICIO / FIM /
tabela=[
        [[],[],"",0,[],0,0]                            ]
#--------------------------------------------------------



