import os
from tkinter import *
import pandas as pd
import numpy as np
from tkinter import messagebox as msb
import time
# checking if the path is correct


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

# displaying a text in a TextBox
def display_text(master, content):
    infoField = Text(master, bg='light grey', width=50, height=6, font=("Helvetica", 10)) # , padx=8, pady=8
    infoField.place(relx=0.4, rely=0.75)
    infoField.insert(1.0, content)
    # T.tag_configure("center", justify="center")
    # infoField.tag_add("center", 1.0, "end")
    return infoField

def check_path(master, folderPath, fileName):
    if len(fileName) < 1:
        fileName = 'no_file'

    dirPath = folderPath + fileName
    if os.path.exists(dirPath):
        requiaredFiles = ["StoreCountryGroup.csv", "GradeCutOff.csv", "GradeSellOff.csv", "DS_PARAM.csv"]
        text1 = ""

        for file in requiaredFiles:
            if not(os.path.isfile(folderPath + file)):
                text1 = text1 + file + ', \n'
        if text1 == "":
            display_text(master, f"Good! \n\nThe folder path exist and there is no missing files\n\nYou can click on \n'Submit' button")
        else:
            display_text(master, f"The folder path exist but there are \nsome missing files such as: \n\n{text1}")

    else:
        if fileName == 'no_file':
            display_text(master, "Error! \n\nThe chosen file name does not exist \n\nPlease try type the file name again")
        else:
            display_text(master, "Error! \n\nThe chosen directory does not exist \n\nPlease try type the folder path again")

    return dirPath

def setTextInput(text, e4):
    e4.delete(0,"end")
    e4.insert(0, text)

# Instruction
model_description = "'Folder path': \nWhere do you keep input files.\n" \
                    "Example: 'c:\Mariusz\MyProjects\LostSales\input files'\n\n" \
                    "'Database file name': \nA name of the database file\n" \
                    "Example: 'StockAndSales_PQ1.zip'\n\n" \
                    "'Download db': \nDo you have a .csv database file or you are going to download a new one?\n\n" \
                    "'check' button: \nThe button is checking whether the chosen path is correct and if it contains all of the necessary files"

def calculation(folder):
    MsgBox = msb.askquestion('Exit Application', 'Are you sure you want to exit the application',
                                       icon='warning')
    if MsgBox == 'yes':
        stockAndSales = pd.read_csv(folder, compression='zip')
        # -Calculations--------------------------------------------
        stockAndSales.rename(
            columns={'StrNumber': 'Store', 'SalesValue': 'SalesR', 'SalesQty': 'SalesQ', 'StockQty': 'StockQ'},
            inplace=True)

        # make sure you can do this:
        stockAndSales = stockAndSales[(stockAndSales['SalesR'] > 0) & (stockAndSales['SalesQ'] > 0)]
        stockAndSales['StockQ'] = stockAndSales['StockQ'].apply(lambda x: 0 if x < 0 else x)

        # -Total Sales per Category/Store--------------------------
        temp = stockAndSales.groupby(['CategoryID', 'Store']).agg({'SalesR': 'sum', 'SalesQ': 'sum'}).reset_index()
        temp.rename({'SalesR': 'Total_CatSalesR', 'SalesQ': 'Total_CatSalesQ'}, axis=1, inplace=True)
        stockAndSales = pd.merge(stockAndSales, temp, on=['CategoryID', 'Store'], how='left').sort_values(
            by=['Store', 'CategoryID'])
        del temp

        # -Total Sales per Store-----------------------------------
        temp = stockAndSales.groupby(['Store']).agg({'SalesR': 'sum'}).reset_index()
        temp.rename({'SalesR': 'Total_StoreSalesR'}, axis=1, inplace=True)
        stockAndSales = pd.merge(stockAndSales, temp, on=['Store'], how='left').sort_values(by=['Store', 'CategoryID'])
        del temp

        # -Aggregation---------------------------------------------
        stockAndSales['SalesAUP'] = stockAndSales.SalesR / stockAndSales.SalesQ
        stockAndSales['Total_SalesAUP'] = stockAndSales.Total_CatSalesR / stockAndSales.Total_CatSalesQ
        stockAndSales['SellOff'] = stockAndSales.SalesQ / (stockAndSales.StockQ + stockAndSales.SalesQ)

        stockAndSales['CatSalesRatio'] = stockAndSales.Total_CatSalesR / stockAndSales.Total_StoreSalesR  # Profiles
        stockAndSales['WeekSalesRatio'] = stockAndSales.SalesR / stockAndSales.Total_CatSalesR  # Profiles_Sales Ratio

        # -Temporary added manually--------------------------------
        stockAndSales['DesiredSellOff'] = 0.15
        stockAndSales['MLQ'] = 120
        stockAndSales['IncreaseFactor'] = 0.10

        # -Final Calculations--------------------------------------
        stockAndSales['s1'] = np.where(stockAndSales.SellOff > stockAndSales.DesiredSellOff, 1,
                                       np.where(stockAndSales.StockQ <= stockAndSales.MLQ, 1, 0))
        stockAndSales['s2'] = np.where(stockAndSales.s1 == 1,
                                       np.where(stockAndSales.WeekSalesRatio - stockAndSales.CatSalesRatio > 0, 1, 0), 0)
        stockAndSales['s2'] = np.where(stockAndSales.s1 == 1,
                                       np.where(stockAndSales.WeekSalesRatio - stockAndSales.CatSalesRatio > 0, 1, 0), 0)

        stockAndSales['ConditionCalc'] = np.where(stockAndSales.s2 == 0, stockAndSales.SalesR, 0)
        stockAndSales['ConditionMix'] = np.where(stockAndSales.s2 == 0, stockAndSales.WeekSalesRatio, 0)
        stockAndSales['SalesAdjusted'] = stockAndSales.ConditionCalc / stockAndSales.ConditionMix
        stockAndSales['SalesAdjusted'].fillna(0, inplace=True)

        stockAndSales['s3_Ret'] = np.where(stockAndSales.s2 == 0, 0,
                                           stockAndSales.WeekSalesRatio * stockAndSales.SalesAdjusted - stockAndSales.SalesR)
        stockAndSales['s4_Ret'] = np.where(stockAndSales.s1 == 1,
                                           np.where(stockAndSales.WeekSalesRatio - stockAndSales.CatSalesRatio < 0,
                                                    stockAndSales.SalesR * stockAndSales.IncreaseFactor, 0), 0)
        stockAndSales['s4_Q'] = (stockAndSales.s3_Ret + stockAndSales.s4_Ret) / np.where(stockAndSales.SalesAUP == 0,
                                                                                         stockAndSales.Total_SalesAUP,
                                                                                         stockAndSales.SalesAUP)

        folderPath = 'c:\Mariusz\MyProjects\LostSales\input files\\'
        stockAndSales.head().to_csv(folderPath + 'final_df.csv', index=False)
        msb.showinfo("Information", f"The Model is ready.\nFolder:\n{folderPath}\nFile:\n'final_df.csv'")
    else:
        msb.showinfo('Return', 'You will now return to the application screen')