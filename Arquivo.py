import os
import operator

class File(object):

    def __init__(self, nameFileIn=None):
        self.__nameFileIn = str(nameFileIn)
        self.__nameFileOut = None
        self.__pointerFile = self.__searchPointerFile()

    def getMultProcess(self):
        ref_file = self.__openFile(self.__nameFileIn, 'r')
        number = ref_file.readline().split('=')[1]
        self.__closeFile(ref_file)
        return number

    def getProcess(self):
        listProcess = []
        ref_file = self.__openFile(self.__nameFileIn, 'r')

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

    def getOperation(self):
        listOperation = []
        ref_file = self.__openFile(self.__nameFileIn, 'r')

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

    def createOut(self, listDate=[]):
        self.__arqObject.close()

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
