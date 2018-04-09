from File import File as f

#nameFileIn ou nameFileOut pode ou não ser passado.
#Caso não há, o nome padrão é in.txt e out.txt respectivamente.

nameFileIn = "in2.txt"

arquivo = f(nameFileIn)
print(arquivo.getMultProcess())
print(arquivo.getProcess())
print(arquivo.getOperation())
arquivo.createOut()
