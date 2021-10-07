import daxDownloader as dd
import daxQueries as dq
import functions as f
import StockAndSales

import pandas as pd
import numpy as np
import os
import datetime


print('### Lost Sales ###')
print("Witaj użytkowniku! W celu wyliczenia lost sales podążaj za instrukcjami.")


print("Ustaw ścieżkę folderu, gdzie będą trzymane wszystkie pliki csv:")
################### odkomentować przed startem
# folderPath = f.setUpFolderPath()
folderPath = r"c:\Mariusz\MyProjects\LostSales\input files" ## f.setUpFolderPath()

print("Umieść w folderze ", folderPath, " wymgane pliki .csv: StoreAttributes, GradeCutOff, GradeSellOff, DSParam")


stockAndSales_path = folderPath + "/StockAndSales.csv"

storeCountryGroup_path = folderPath + "/StoreCountryGroup.csv"
gradeCutOff_path = folderPath + "/GradeCutOff.csv"
gradeSellOff_path = folderPath + "/GradeSellOff.csv"
dsParam_path = folderPath + "/DSParam.csv"
outputFilePath_path = folderPath + "/LostSales.csv"

################### odkomentować przed startem
# f.checkEntryFiles(folderPath)



# 0. Pobierz dane:
################### odkomentować przed startem
# StockAndSales.run(stockAndSales_path)
stockAndSales = pd.read_csv(stockAndSales_path)
storeCountryGroup = pd.read_csv(storeCountryGroup_path)
cutOff = pd.read_csv(gradeCutOff_path)


# 1. rename
main = stockAndSales

# 1,5. Utworzyć pętlę i liczyć wszystko poniżej osobno dla każdego depu

# 2. calculate Store Week Contribution
contribution = main.groupby(['CategoryID', 'StrNumber', 'Week'])['SalesValue'].agg('sum').reset_index()
contribution['Contribution'] = (contribution['SalesValue'] / contribution.groupby(['CategoryID', 'StrNumber'])['SalesValue'].
                            transform('sum')).\
                            round(17)
contribution = contribution[['CategoryID', 'StrNumber', 'Week', 'Contribution']]
contribution.fillna(0, inplace=True)
main = main.merge(contribution, on=['CategoryID', 'StrNumber', 'Week'])


# 3. Add gradeCutOff
cutOff = cutOff.melt()
cutOff['Grade'] = [1, 2, 3, 4, 5, 6]
cutOff.drop(columns=['variable'], inplace=True)
cutOff.rename(columns={'value': 'CutOff'}, inplace=True)
cutOff.sort_values(by='CutOff', inplace=True)

temp = main.groupby(['CategoryID', 'StrNumber'])['SalesValue'].agg('sum')
temp = pd.DataFrame(temp).reset_index()
temp = temp.groupby(['CategoryID']).apply(lambda x: x.sort_values(['SalesValue'], ascending=False))
temp = temp.drop(columns=['CategoryID'])

temp['CumSum'] = temp.groupby('CategoryID')['SalesValue'].transform('cumsum')
temp['Pct'] = temp['CumSum'] / temp.groupby('CategoryID')['SalesValue'].transform('sum')

temp = temp.reset_index()
temp.drop(columns=['CumSum', 'level_1'], inplace=True)
temp.Pct = np.where(temp.Pct > 1, 1, temp.Pct)

temp[['SalesValue', 'Pct']] = temp[['SalesValue', 'Pct']].fillna(0)

temp.sort_values(by=['Pct'], inplace=True)

cutTemp = pd.merge_asof(temp, cutOff, left_on="Pct", right_on="CutOff", direction='forward')
cutTemp.drop(columns=['Pct', 'CutOff', 'SalesValue'], inplace=True)

main = pd.merge(main, cutTemp, on=['StrNumber', 'CategoryID'])

del temp
del cutTemp


# Country Group contribution calculation

countryGroup = pd.read_csv(storeCountryGroup_path)
countryGroup = main.merge(countryGroup, how="left", on=['StrNumber'])
countryGroup['CumSum'] = countryGroup.groupby(['CategoryID', 'CountryGroup', 'Week'])['SalesValue'].agg('sum')
countryGroup['CGPct'] = (countryGroup['CumSum'] / countryGroup.groupby(['CategoryID', 'CountryGroup'])['SalesValue'].transform('sum')).round(17)

print(countryGroup)




StockAndSales.to_csv('StockAndSales.csv',index=False)





