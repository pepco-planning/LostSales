from pandas import DataFrame, read_csv

import pandas as pd
import numpy as np
import time
import os.path
import gc

start = time.time()


# Import data per Store and Hierarchy
DataPerStore = r'C:\Planning\Temp\LS\LostSalesData.csv'
CutOff = r'C:\Planning\Temp\LS\GradeCutOff.csv'
Hierarchy = r'C:\Planning\Temp\LS\StoreAttr.csv'
DS_PARAM = r'C:\Planning\Temp\LS\DS_PARAM.csv'
GradeSellOff = r'C:\Planning\Temp\LS\GradeSellOff.csv'
Season = r'C:\Planning\Temp\LS\SeasonStartDate.csv'
Seasons = r'C:\Planning\Temp\LS\Seasons.csv'

print ('1 Processing time:', "{0:.2f}".format(time.time()-start), 'seconds.')


main = pd.read_csv(DataPerStore)
gso = pd.read_csv(GradeSellOff)
str = pd.read_csv(Hierarchy)
seasonstart = pd.read_csv(Season)
allseasons = pd.read_csv(Seasons, header=None)


main['Product'] = main['Product'].astype('category')
main['Version'] = main['Version'].astype('category')
main['Store'] = main['Store'].astype('category')
main['Time'] = main['Time'].astype('category')
main['SalesU'] = main['SalesU'].astype('int32')
main['STCSTKU'] = main['STCSTKU'].astype('int32')

print ('File upload time:', "{0:.2f}".format(time.time()-start), 'seconds.')


# Filter to only Opened stores for more than 14 days
str = str[str.Status == 'Open'].reset_index()
dict = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06', 'JUL':'07','AUG':'08', 'SEP':'09','OCT':'10','NOV':'11','DEC':'12'}

str['OpeningDate'] =  str['OpeningDate'].replace(dict, regex=True)
str['OpeningDate'] = pd.to_datetime(str['OpeningDate'],format='%d-%m-%Y')


allseasons[1] = pd.to_datetime(allseasons[1],format='%Y-%m-%d')
seasonselected = seasonstart.loc[0,"Season"]

index_chosen = allseasons.loc[allseasons[0] == seasonselected].index[0]

startdate = allseasons.loc[index_chosen-2,1]

str['daysdiff'] = (startdate - str['OpeningDate']).dt.days

str = str[str.daysdiff >= 14].reset_index()
str.drop(columns=['level_0','index','CountryGroup','Status','ClosingDate','daysdiff','OpeningDate'], inplace=True)

main = main.merge(str, on='Store', how='inner')

main['Store'] = main['Store'].astype('category')

print ('Stores filtered:', "{0:.2f}".format(time.time()-start), 'seconds.')

#------------------------------------------------------------------------------------------------------
# Section to calaculate Store Week Contribution

# Group by Store, Week
df = main

temp = df.groupby(['Product','Store','Time'])['SalesV'].agg(sum).reset_index()

# Store Week Contribution to the total Sales of the Sub Category per Season
temp['STRPCT'] = (temp['SalesV'] / temp.groupby(['Product','Store'])['SalesV'].transform('sum')).round(17)
temp.drop(columns='SalesV', inplace=True)
main = pd.merge(main,temp, on=['Product','Store','Time'])

# print(main[main.Store == 'S3030'].groupby(['Product','Store'])['SalesV'].transform('sum'))

del temp

print ('Store Week Contribution calculated:', "{0:.2f}".format(time.time()-start), 'seconds.')

# --------------------------------------------------------------------------------------------------------
# Section to grade Stores

cut = pd.read_csv(CutOff, usecols=['GRADE1CUTOFF','GRADE2CUTOFF','GRADE3CUTOFF','GRADE4CUTOFF','GRADE5CUTOFF','GRADE6CUTOFF'])
cut = cut.melt()
cut['Grade']=[1,2,3,4,5,6]
cut.drop(columns=['variable'], inplace=True)
cut.rename(columns={'value':'CutOff'}, inplace=True)
cut.sort_values(by='CutOff', inplace=True)

# Read CSV file
# df = pd.read_csv(Location, usecols=['Product','Store','SalesV'])

temp = df.groupby(['Product','Store'])['SalesV'].agg('sum')
temp = pd.DataFrame(temp).reset_index()
temp = temp.groupby(['Product']).apply(lambda x: x.sort_values(['SalesV'], ascending=False))
temp = temp.drop(columns='Product')



temp['cumsum'] = temp.groupby('Product')['SalesV'].transform('cumsum')

temp['pct'] = temp['cumsum'] / temp.groupby('Product')['SalesV'].transform('sum')


temp = temp.reset_index()
temp.drop(columns=['cumsum','level_1'], inplace=True)


temp['pct'] = np.where(temp['pct'] > 1,1,temp['pct'])

# Create Store Grade based on Contribution

temp[['SalesV','pct']] = temp[['SalesV','pct']].fillna(value=0)

temp.sort_values(by=['pct'], inplace=True)

cuttemp = pd.merge_asof(temp, cut, left_on='pct', right_on='CutOff', direction='forward')
cuttemp.drop(columns=['pct','CutOff','SalesV'],inplace=True)

main = pd.merge(main,cuttemp, on=['Store','Product'])

del temp
del cuttemp

print ('Stores Graded:', "{0:.2f}".format(time.time()-start), 'seconds.')
#--------------------------------------------------------------------------------------------------------
# Country Group Contribution calculation

dh = pd.read_csv(Hierarchy, header=None)
dh.rename(columns={0:'Store',1:'CGroup'}, inplace=True)
dh.drop(columns=[2,3,4], inplace=True)
dh['CGroup'] = dh['CGroup'].astype('category')

# Merge 2 DataFrames that were imported
result = pd.merge(df, dh, how='left', on=['Store'])


# Group by Group, Week and calculate Contribution
result = result.groupby(['Product','CGroup','Time'])['SalesV'].agg(sum)
temp = pd.DataFrame(df)
temp = result.reset_index()

temp['CGPCT'] = (temp['SalesV'] / temp.groupby(['Product','CGroup'])['SalesV'].transform('sum')).round(17)
temp.drop(columns='SalesV', inplace=True)

main = pd.merge(main,dh, on='Store')
main = pd.merge(main,temp, on=['Product','CGroup','Time'])

main['Store'] = main['Store'].astype('category')

del result
del temp
del dh

print ('Country Group contribution:', "{0:.2f}".format(time.time()-start), 'seconds.')


# --------------------------------------------------------------------------------------------------------
# DS PARAM Load

factor = pd.read_csv(DS_PARAM, usecols=['Product','MAXWEEKS','SELLOFF1CUTOFF','SELLOFF1INCREASE','SELLOFF2CUTOFF','SELLOFF2INCREASE','SELLOFF3CUTOFF','SELLOFF3INCREASE'])

fcutoff = pd.melt(factor, id_vars=['Product'], value_vars=['SELLOFF1CUTOFF','SELLOFF2CUTOFF','SELLOFF3CUTOFF'])
fcutoff['variable'] = fcutoff['variable'].str.split("CUTOFF", expand=True)
fcutoff.rename(columns={'value':'cutoff'}, inplace=True)

fincrease = pd.melt(factor, id_vars=['Product'], value_vars=['SELLOFF1INCREASE','SELLOFF2INCREASE','SELLOFF3INCREASE'])
fincrease['variable'] = fincrease['variable'].str.split("INCREASE", expand=True)
fincrease.rename(columns={'value':'inc'}, inplace=True)

temp = pd.merge(fcutoff,fincrease, on=['Product','variable'])
temp.drop(columns=['variable'], inplace=True)
temp.sort_values(by='cutoff', inplace=True)

#main['SellOff'] = main['SalesU']/(main['STCSTKU']+main['SalesU'])

main['SellOff'] = np.where(main['STCSTKU'] + main['SalesU'] == 0,-1,main['SalesU']/(main['STCSTKU']+main['SalesU']))


temp['Product'] = temp['Product'].astype('category')

main['SellOff'] = main['SellOff'].fillna(value=0)
#main.fillna(0, inplace=True)

main['SellOff'] = np.where(main['SellOff'] < 0,0,main['SellOff'])

main.sort_values(by='SellOff', inplace=True)
main = pd.merge_asof(main,temp, left_on='SellOff', right_on='cutoff', by='Product', direction='backward')
main.drop(columns='cutoff', inplace=True)

factor.drop(columns=['SELLOFF1CUTOFF','SELLOFF1INCREASE','SELLOFF2CUTOFF','SELLOFF2INCREASE','SELLOFF3CUTOFF','SELLOFF3INCREASE'], inplace=True)

main = pd.merge(main,factor, on='Product')
main['Product'] = main['Product'].astype('category')

del factor
del temp
del fcutoff
del fincrease

print ('DS Parameteres Loaded:', "{0:.2f}".format(time.time()-start), 'seconds.')


# --------------------------------------------------------------------------------------------------------
# Calculate Total Contribution

#main['TOTCONTR'] = (main['SalesV'].groupby([main['Product'],main['Time']]).transform('sum')/
#                        main['SalesV'].groupby(main['Product']).transform('sum')).round(4)


print ('5 Processing time:', "{0:.2f}".format(time.time()-start), 'seconds.')

# --------------------------------------------------------------------------------------------------------
# Add Expected SellOff

temp = pd.melt(gso, id_vars=['Product','Time'], value_vars=['GRADE1SELLOFF','GRADE2SELLOFF','GRADE3SELLOFF','GRADE4SELLOFF','GRADE5SELLOFF','GRADE6SELLOFF'])

temp['variable'] = temp['variable'].str.split("SELLOFF", expand=True)
temp['variable'] = temp['variable'].str.replace('GRADE','')
temp.rename(columns={'value':'ExpSellOff' }, inplace=True)
temp['variable'] = temp['variable'].astype('int64')



main = pd.merge(main, temp, left_on=['Product','Time','Grade'], right_on=['Product','Time','variable'])

main.drop(columns=['variable'], inplace=True)

del temp

# --------------------------------------------------------------------------------------------------------
# Add MLQ

temp = gso.drop(columns=['Version','GRADE1SELLOFF','GRADE2SELLOFF','GRADE3SELLOFF','GRADE4SELLOFF','GRADE5SELLOFF','GRADE6SELLOFF'])

main = pd.merge(main, temp, on=['Product','Time'])
del temp

main['Product'] = main['Product'].astype('category')
main['Time'] = main['Time'].astype('category')


# --------------------------------------------------------------------------------------------------------
# Start of real Lost Sales Calculation

conditions = [
    (main['SellOff'] > main['ExpSellOff']),
    (main['STCSTKU'] < main['MLQ'])
]
choices = [1,1]

main['ls1'] = np.select(conditions, choices, default=0)


print ('6 Processing time:', "{0:.2f}".format(time.time()-start), 'seconds.')


# Count the Weeks with Lost Sales
main['totalls1'] = main['ls1'].groupby([main['Store'],main['Product']]).transform('sum')

# Check if number of Weeks with LS is higher than MAX

main['UseCG'] = np.where(main['totalls1'] >= main['MAXWEEKS'],1,0)



print ('7 Processing time:', "{0:.2f}".format(time.time()-start), 'seconds.')

# Check Lost Sales Condition 2 - LS_S2 matrix and AR

main['STRPCT'].replace([np.inf],0,inplace=True)

main['ls2'] = np.where(np.logical_and(main['ls1'] == 1,(main['CGPCT']>=main['STRPCT'])),0,main['SalesV'])
main['mix'] = np.where(np.logical_and(main['ls1'] == 1,(main['CGPCT']>=main['STRPCT'])),0,main['CGPCT'])
#print(main[main.Store =='S1442'][main.Time=='Y19WK05'][main.Product=='P1_1_1_8_1_1_3'])
#
#main[main.Store =='S1442'][main.Time=='Y19WK05'][main.Product=='P1_1_1_8_1_1_3'].to_csv('09012019.csv')

print ('7.1 Processing time:', "{0:.2f}".format(time.time()-start), 'seconds.')


#merged['SALESV_ACT'] = merged['SALESV_ACT'].groupby([merged['SCAT'],merged['STR']]).transform('sum')
main['sales_adj'] = (main['ls2'].groupby([main['Product'],main['Store']]).transform('sum')/
                        main['mix'].groupby([main['Product'],main['Store']]).transform('sum'))
print ('7.2 Processing time:', "{0:.2f}".format(time.time()-start), 'seconds.')


gc.collect()

cond2 = [
    np.logical_and(main['ls2'] == 0,main['ls1'] == 1)
]
cho2 = [main['CGPCT'] * main['sales_adj']-main['SalesV']]

main['ls3'] = np.select(cond2, cho2, default=0)



print ('8 Processing time:', "{0:.2f}".format(time.time()-start), 'seconds.')
#merged['ls3'] = np.where((merged['ls2'] == 1 & merged['ls1'] > 0),(merged['CGContribution'] * merged['sales_adj']-merged['Sales Retail']),0)

main['ls4'] = np.where(np.logical_and(main['ls1'] == 1,main['CGPCT'] < main['STRPCT']),main['SalesV'] * main['inc'],0)

main['Sales AUP'] = main['SalesV']/main['SalesU']
main['ls4_q'] = ((main['ls3']+main['ls4'])/main['Sales AUP']).round(1)



main['SalesVLS'] = main['ls3']+main['ls4']
main['sales_adj_r'] = (main['SalesV'] + main['SalesVLS']).round(6)
main['sales_adj_q'] = main['SalesU'] + main['ls4_q']
main['SalesAupDS'] = (main['sales_adj_r'] / main['sales_adj_q']).round(6)

print ('8.1 Processing time:', "{0:.2f}".format(time.time()-start), 'seconds.')

main.rename(columns={'sales_adj_r': 'SalesVDS', 'sales_adj_q': 'SalesUDS', 'Grade': 'TurnOverGRpDS', 'STRPCT': 'StrContrDS', 'CGPCT': 'CtyGrpContrDS'},inplace=True)
print ('8.2 Processing time:', "{0:.2f}".format(time.time()-start), 'seconds.')

def CountryGroupLS():

    temp = main.groupby(['Product','CGroup','Time'])['SalesVDS'].agg(sum)
    temp = temp.reset_index()

    temp['CGPCTLS'] = (temp['SalesVDS'] / temp.groupby(['Product','CGroup'])['SalesVDS'].transform('sum')).round(17)
    temp.drop(columns='SalesVDS', inplace=True)

    return temp


temp = CountryGroupLS()

main = pd.merge(main,temp, on=['Product','CGroup','Time'])
main['SalesSeason'] = main.groupby(['Product','Store'])['SalesVDS'].transform('sum')
main['SalesVDS'] = np.where(main['totalls1'] >= main['MAXWEEKS'],main['SalesSeason']*main['CGPCTLS'],main['SalesVDS'])

main.drop(columns=['SellOff','inc','mix','CGroup','SalesSeason','CGPCTLS','sales_adj','STCSTKU','SalesU','SalesV','MAXWEEKS','ExpSellOff','MLQ','ls1','totalls1','UseCG','ls2','ls3','ls4','Sales AUP','ls4_q'], inplace=True)


main['Product'] = main['Product'].astype('category')
main['Version'] = main['Version'].astype('category')
main['Store'] = main['Store'].astype('category')
main['Time'] = main['Time'].astype('category')


#main.to_csv('C:/Planning/Temp/LS/kamil.csv', index=False)

# Function to Calculate Country Group Contribution again, after Lost Sales are done and Sales is adjusted.


def FinalOutput():

    final = pd.melt(main, id_vars=['Product','Store','Time'], value_vars=['SalesVDS','SalesVLS','SalesAupDS','TurnOverGRpDS','StrContrDS','CtyGrpContrDS'])

    final['Product'] = final['Product'].astype('category')
    final['Store'] = final['Store'].astype('category')
    final['Time'] = final['Time'].astype('category')
    final['variable'] = final['variable'].astype('category')

    print ('8.3 Processing time:', "{0:.2f}".format(time.time()-start), 'seconds.')
    final['version'] = final['variable'].str[-2:]
    final['variable'] = final['variable'].str[:-2]
    print ('8.4 Processing time:', "{0:.2f}".format(time.time()-start), 'seconds.')

    final['key']= final['Product'].str.rsplit('_',3).str[0]

    final['value'] = final['value'].round(2)

    print ('Total processing time:', "{0:.2f}".format(time.time()-start), 'seconds.')

    str.to_csv(r'C:\Planning\Temp\LS\StoreList.csv', index=False)

    for key, final in final.groupby('key'):

        final.to_csv(f'C:/Planning/Temp/LS/{key}.csv', index=False, header=None, columns=['Product','Store','Time','version','variable','value'])

#FinalOutput()


#print(main[['Product','Store','Time','CtyGrpContrDS','CGPCTLS']])
#main.to_csv('C:/Planning/Temp/LS/kamil2.csv', index=False)

FinalOutput()


print ('Total processing time after Save:', "{0:.2f}".format(time.time()-start), 'seconds.')
