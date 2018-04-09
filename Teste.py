from File import File as f

arquivo = f("in.txt")
print(arquivo.getMultProcess())
print(arquivo.getProcess())
print(arquivo.getOperation())
arquivo.createOut()
