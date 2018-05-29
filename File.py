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

            # ABRIR ARQUIVO E IR DIRETO AO PONTO QUE COMEÇAM OS PROCEDIMENTOS
            ref_file.seek(self.__pointerFile[1])

            # PEGAR TODAS AS LINHAS REFERENTES AOS PROCEDIMENTOS E SALVAR EM UMA LISTA
            line = ref_file.readline()
            while line.__len__() != 2:
                listProcess.append(line)
                line = ref_file.readline()

            # LIMPAR AS LINHAS REFERENTES AOS PROCEDIMENTOS SALVOS E SALVAR APENAS O VALORES EM UMA LISTA
            listDataProcess = []
            for processo in listProcess:
                byEqual = processo.split('=')[1]
                byComma = byEqual.split(",")
                listProcessUnit = []
                listProcessUnit.append(processo.split('=')[0][-1])
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
            # ABRIR ARQUIVO E IR DIRETO AO PONTO QUE COMEÇA AS OPERAÇÕES
            ref_file.seek(self.__pointerFile[2])

            # PEGAR TODAS AS LINHAS REFERENTES AS OPERAÇÕES E SALVAR EM UMA LISTA
            line = ref_file.readline()
            while line:
                listOperation.append(line)
                line = ref_file.readline()

            # LIMPAR AS LINHAS REFERENTES AS OPERAÇÕES SALVAS E SALVAR APENAS O VALORES EM UMA LISTA
            listDataOperation = []
            for operacao in listOperation:
                limp1 = operacao.split("=")[1]
                listDataOperation.append(limp1[0])

            self.__closeFile(ref_file)
            return listDataOperation

        return None


    def __formatString(self, string, data):
        numProcess = len(data)
        cont = 1
        stringSave = string+'\n'
        for num in range(0, numProcess):
            stringSave += "-TE-P" + str(cont) + "=" + str(abs(data[str(cont)])) + "\n"
            cont += 1

        stringSave += '-TME=' + str(self.__countTime(data)) + '\n'

        return stringSave


    @staticmethod
    def __countTime(dictTime):
        time = 0
        for key in dictTime:
            time += abs(dictTime[key])
        return time/len(dictTime)


    def createOut(self, nameFileOut=None, data=[]):
        if nameFileOut is None:
            nameFileOut = self.__nameFileOut

        if len(data) > 0:
            string = ''
            string += self.__formatString('FCFS', data[0][0])
            string += self.__formatString('Prioridade-CP', data[1][0])
            string += self.__formatString('Round-Robin(20)', data[2][0])
            print(string)

            ref_file = open(nameFileOut, 'w+', encoding="utf-8")
            ref_file.write(string)
            ref_file.close()

    def __openFile(self, nameFile, mode):
        try:
            self.arqObject = open(nameFile, mode, encoding="utf-8")
            return self.arqObject
        except FileNotFoundError:
            return None

    @staticmethod
    def __closeFile(ref_file):
        ref_file.close()

    def __searchPointerFile(self):
        listPointer = []

        ref_file = self.__openFile(self.__nameFileIn, 'r')

        if ref_file is not None:

            pointB = ref_file.tell()
            line = ref_file.readline()
            pointA = ref_file.tell()

            while line:
                if "Multiprogramacao" in line:
                    listPointer.append(pointB)

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
