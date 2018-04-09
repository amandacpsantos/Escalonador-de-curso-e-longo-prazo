class File(object):

    def __init__(self, nameFileIn="in.txt"):
        self.__nameFileIn = str(nameFileIn)
        self.__nameFileOut = "out.txt"
        self.__pointerFile = self.__searchPointerFile()

    def getMultProcess(self):
        ref_file = self.__openFile(self.__nameFileIn, 'r')

        if ref_file is not None:
            number = ref_file.readline().split('=')[1]
            self.__closeFile(ref_file)
            return number

        return None

    def getProcess(self):
        listProcess = []
        ref_file = self.__openFile(self.__nameFileIn, 'r')

        if ref_file is not None:

            #ABRIR ARQUIVO E IR DIRETO AO PONTO QUE COMEÇAM OS PROCEDIMENTOS
            ref_file.seek(self.__pointerFile[1])

            #PEGAR TODAS AS LINHAS REFERENTES AOS PROCEDIMENTOS E SALVAR EM UMA LISTA
            line = ref_file.readline()
            while line.__len__() != 2:
                listProcess.append(line)
                line = ref_file.readline()

            #LIMPAR AS LINHAS REFERENTES AOS PROCEDIMENTOS SALVOS E SALVAR APENAS O VALORES EM UMA LISTA
            listDataProcess = []
            for processo in listProcess:
                byEqual = processo.split('=')[1]
                byComma = byEqual.split(",")

                listProcessUnit = []
                for valor in byComma:
                    listProcessUnit.append(valor.split("-")[0])
                    if ";" in valor:
                        listProcessUnit.append(valor[-2])

                listDataProcess.append(listProcessUnit)

            self.__closeFile(ref_file)
            return listDataProcess

        return None

    def getOperation(self):
        listOperation = []
        ref_file = self.__openFile(self.__nameFileIn, 'r')

        if ref_file is not None:
            #ABRIR ARQUIVO E IR DIRETO AO PONTO QUE COMEÇA AS OPERAÇÕES
            ref_file.seek(self.__pointerFile[2])

            #PEGAR TODAS AS LINHAS REFERENTES AS OPERAÇÕES E SALVAR EM UMA LISTA
            line = ref_file.readline()
            while line:
                listOperation.append(line)
                line = ref_file.readline()

            #LIMPAR AS LINHAS REFERENTES AS OPERAÇÕES SALVAS E SALVAR APENAS O VALORES EM UMA LISTA
            listDataOperation = []
            for operacao in listOperation:
                limp1 = operacao.split("=")[1]
                listDataOperation.append(limp1[0])

            self.__closeFile(ref_file)
            return listDataOperation

        return None

    def createOut(self, nameFileOut=None, listDada=[]):
        if nameFileOut is None:
            nameFileOut = self.__nameFileOut

        ref_file = open(nameFileOut, 'w+')

        ref_file.write("FCFS\n"
                       "-TE-P1=\n"
                       "-TE-P2=\n"
                       "-TE-P3=\n"
                       "-TE-P4=\n"
                       "-TME=\n"
                       "Prioridades-CP\n"
                       "-TE-P1=\n"
                       "-TE-P2=\n"
                       "-TE-P3=\n"
                       "-TE-P4=\n"
                       "-TME=\n"
                       "Round-Robin(20)\n"
                       "-TE-P1=\n"
                       "-TE-P2=\n"
                       "-TE-P3=\n"
                       "-TE-P4=\n"
                       "-TME=\n")
        ref_file.close()

    def __openFile(self, nameFile, mode):
        try:
            self.arqObject = open(nameFile, mode)
            return self.arqObject
        except FileNotFoundError:
            return None

    def __closeFile(self,ref_file):
        ref_file.close()

    def __searchPointerFile(self):
        listPointer= []

        ref_file = self.__openFile(self.__nameFileIn, 'r')

        if ref_file is not None:

            pointB = ref_file.tell()
            line = ref_file.readline()
            pointA = ref_file.tell()

            while line:
                if "Multiprogramacao" in line:
                    listPointer.append(pointB);

                elif "Processos" in line:
                    pointB = ref_file.tell()
                    listPointer.append(pointB)

                elif "Operações" in line:
                    pointB = ref_file.tell()
                    listPointer.append(pointB)

                pointB = pointA
                line = ref_file.readline()
                pointA = ref_file.tell()

            self.__closeFile(ref_file)

            return listPointer

        return None