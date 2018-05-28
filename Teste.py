from File import File as f
from App import App as a


# pegar informações do arquivo de entrada
nameFileIn = "in.txt"
arquivo = f(nameFileIn)
listaProcesso = arquivo.getProcess()
listaEvento = arquivo.getOperation()
multiprogramacao = int(arquivo.getMultProcess())



app = a(listaProcesso, listaEvento, multiprogramacao)
arquivo.createOut('out.txt', app.executa())

