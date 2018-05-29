from File import File as f
from App import App as a


# Pegar Informações do Arquivo de Entrada
nameFileIn = "in.txt"
arquivo = f(nameFileIn)
listaProcesso = arquivo.getProcess()
listaEvento = arquivo.getOperation()
multiprogramacao = int(arquivo.getMultProcess())

# Executar
app = a(listaProcesso, listaEvento, multiprogramacao)
a = app.executa()
arquivo.createOut('out.txt', a)
