import pandas as pd
import numpy as np
import gui
# import daxDownloader as dd
# import daxQueries as dq
# import functions as f
# import StockAndSales
# import os
# import datetime


# print('### Lost Sales ###')

################### odkomentować przed startem
# print("Witaj użytkowniku! W celu wyliczenia lost sales podążaj za instrukcjami.")
# print("Ustaw ścieżkę folderu, gdzie będą trzymane wszystkie pliki csv:")
# folderPath = f.setUpFolderPath()
# folderPath = r"c:\Mariusz\MyProjects\LostSales\input files" ## f.setUpFolderPath()
# print("Umieść w folderze ", folderPath, " wymgane pliki .csv: StoreAttributes, GradeCutOff, GradeSellOff, DSParam")

# 0. Pobierz dane:
################### odkomentować przed startem
# StockAndSales.run(stockAndSales_path)
# stockAndSales = pd.read_csv(stockAndSales_path, compression='zip')
# storeCountryGroup = pd.read_csv(storeCountryGroup_path)
# cutOff = pd.read_csv(gradeCutOff_path)

# folderPath = r"\\10.2.5.140\zasoby\Planowanie\PERSONAL FOLDERS\Mariusz Borycki\Python Projects\LostSales\input files"

# df = pd.read_excel('c:\Mariusz\MyProjects\LostSales\Lost Sales Model.xlsm', sheet_name='Sheet1')
# folderPath = df.iloc[0,1]
# file_name = df.iloc[0,2]
# stockAndSales_path = f"{folderPath}\{file_name}"

folderPath = r"\\10.2.5.140\zasoby\Planowanie\PERSONAL FOLDERS\Mariusz Borycki\Python Projects\LostSales\input files"
stockAndSales_path = folderPath + '/StockAndSales_PQ1.zip'
stockAndSales = pd.read_csv(stockAndSales_path, compression='zip')
# -Calculations--------------------------------------------
stockAndSales.rename(columns={'StrNumber':'Store', 'SalesValue':'SalesR', 'SalesQty':'SalesQ', 'StockQty':'StockQ'}, inplace=True)

# make sure you can do this:
stockAndSales = stockAndSales[(stockAndSales['SalesR'] > 0) & (stockAndSales['SalesQ'] > 0)]
stockAndSales['StockQ'] = stockAndSales['StockQ'].apply(lambda x: 0 if x < 0 else x)

# -Total Sales per Category/Store--------------------------
temp = stockAndSales.groupby(['CategoryID','Store']).agg({'SalesR':'sum', 'SalesQ':'sum'}).reset_index()
temp.rename({'SalesR':'Total_CatSalesR', 'SalesQ':'Total_CatSalesQ'}, axis=1, inplace=True)
stockAndSales = pd.merge(stockAndSales, temp, on=['CategoryID','Store'], how='left').sort_values(by=['Store', 'CategoryID'])
del temp

# -Total Sales per Store-----------------------------------
temp = stockAndSales.groupby(['Store']).agg({'SalesR':'sum'}).reset_index()
temp.rename({'SalesR':'Total_StoreSalesR'}, axis=1, inplace=True)
stockAndSales = pd.merge(stockAndSales, temp, on=['Store'], how='left').sort_values(by=['Store', 'CategoryID'])
del temp

# -Aggregation---------------------------------------------
stockAndSales['SalesAUP'] = stockAndSales.SalesR / stockAndSales.SalesQ
stockAndSales['Total_SalesAUP'] = stockAndSales.Total_CatSalesR / stockAndSales.Total_CatSalesQ
stockAndSales['SellOff'] = stockAndSales.SalesQ / (stockAndSales.StockQ + stockAndSales.SalesQ)

stockAndSales['CatSalesRatio'] = stockAndSales.Total_CatSalesR / stockAndSales.Total_StoreSalesR # Profiles
stockAndSales['WeekSalesRatio'] = stockAndSales.SalesR / stockAndSales.Total_CatSalesR # Profiles_Sales Ratio

# -Temporary added manually--------------------------------
stockAndSales['DesiredSellOff'] = 0.15
stockAndSales['MLQ'] = 120
stockAndSales['IncreaseFactor'] = 0.10

# -Final Calculations--------------------------------------
stockAndSales['s1'] = np.where(stockAndSales.SellOff > stockAndSales.DesiredSellOff, 1, np.where(stockAndSales.StockQ <= stockAndSales.MLQ, 1, 0))
stockAndSales['s2'] = np.where(stockAndSales.s1 == 1, np.where(stockAndSales.WeekSalesRatio-stockAndSales.CatSalesRatio > 0, 1, 0), 0)
stockAndSales['s2'] = np.where(stockAndSales.s1 == 1, np.where(stockAndSales.WeekSalesRatio-stockAndSales.CatSalesRatio > 0, 1, 0), 0)

stockAndSales['ConditionCalc'] = np.where(stockAndSales.s2 == 0, stockAndSales.SalesR, 0)
stockAndSales['ConditionMix'] = np.where(stockAndSales.s2 == 0, stockAndSales.WeekSalesRatio, 0)
stockAndSales['SalesAdjusted'] = stockAndSales.ConditionCalc / stockAndSales.ConditionMix
stockAndSales['SalesAdjusted'].fillna(0, inplace=True)

stockAndSales['s3_Ret'] = np.where(stockAndSales.s2 == 0, 0, stockAndSales.WeekSalesRatio * stockAndSales.SalesAdjusted - stockAndSales.SalesR)
stockAndSales['s4_Ret'] = np.where(stockAndSales.s1 == 1, np.where(stockAndSales.WeekSalesRatio - stockAndSales.CatSalesRatio < 0, stockAndSales.SalesR * stockAndSales.IncreaseFactor, 0), 0)
stockAndSales['s4_Q'] = (stockAndSales.s3_Ret + stockAndSales.s4_Ret) / np.where(stockAndSales.SalesAUP == 0, stockAndSales.Total_SalesAUP, stockAndSales.SalesAUP)

stockAndSales.head().to_csv(folderPath + '/final_df.csv', index=False)