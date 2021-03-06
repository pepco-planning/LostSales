import os
import re


def setUpFolderPath():
    folderPath = input()

    if not os.path.exists(folderPath):
        print("Error! Podany folder nie istnieje. Spróbuj ponownie.")
        folderPath = setUpFolderPath()

    return folderPath


def checkEntryFiles(folderPath):
    requiaredFiles = ["StoreCountryGroup.csv", "GradeCutOff.csv", "GradeSellOff.csv", "DSParam.csv"]

    for file in requiaredFiles:
        while not(os.path.isfile(folderPath + file)):
            print("Error! Umieść w folderze plik ", file, " i zatwierdź.")
            input()

        print("Plik ", file, " jest.")


def setStartEndWeeks():
    return ['Y2021W01', 'Y2021W04']
    ################### odkomentować przed startem
    # startEndWeeks = []
    #
    # print("Podaj początkowy tydzień (np. Y2021W01):")
    # startEndWeeks.append(input())
    #
    # print("Podaj końcowy tydzień (np. Y2021W10):")
    # startEndWeeks.append(input())
    #
    # if not(re.match(r"Y[0-9][0-9][0-9][0-9]W[0-9][0-9]", startEndWeeks[0])
    #        and re.match(r"Y[0-9][0-9][0-9][0-9]W[0-9][0-9]", startEndWeeks[1])):
    #     print("Error! Podany format tygodni jest niepoprawny")
    #     setStartEndWeeks()
    # elif startEndWeeks[0][:5] != startEndWeeks[1][:5]:
    #     print("Error! Zakres dat musi pochodzić z tego samego roku planistycznego")
    #     setStartEndWeeks()
    # elif int(startEndWeeks[0][1:5] + startEndWeeks[0][6:8]) > int(startEndWeeks[1][1:5] + startEndWeeks[1][6:8]):
    #     print("Error! Początkowy tydzień nie może być mniejszy od końcowego.")
    #     setStartEndWeeks()
    #
    # return startEndWeeks

