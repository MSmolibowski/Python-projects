#-----------------Description--------------------
import numpy as np
#-----------------Libraries----------------------
import pandas as pd
import functools
import operator
import numpy as np
#----------------Functions-----------------------

#---------------Load Data------------------------
MM_shLuc = pd.read_csv('Arkusze/SKMES sh714 (Ekspr+MM)/Macierze Metylacji/MM_SKMES_sh714_vs_shLUC_MS.csv', delimiter= ';')
MM_shLuc = MM_shLuc[~MM_shLuc['Gene_Symbol'].isnull()]        #copy all rows with values in col Genes
MM_shLuc = MM_shLuc[~MM_shLuc['Localization'].isnull()] #copy all rows with values in col Genes

MM_WT = pd.read_csv('Arkusze/SKMES sh714 (Ekspr+MM)/Macierze Metylacji/MM_SKMES_sh714_vs_WT_MS.csv', delimiter= ';')
MM_WT = MM_WT[~MM_WT['Gene_Symbol'].isnull()]
MM_WT = MM_WT[~MM_WT['Localization'].isnull()]

#------save and load to reindex-----
MM_shLuc.to_csv('Arkusze/SKMES sh714 (Ekspr+MM)/Macierze Metylacji/temp/reindex/MM_shLUC_temp.csv', sep= ';', header= True)
MM_shLuc = pd.read_csv('Arkusze/SKMES sh714 (Ekspr+MM)/Macierze Metylacji/temp/reindex/MM_shLUC_temp.csv', delimiter=';')
del MM_shLuc['Unnamed: 0']              #del column name ['Unnamed: 0']

MM_WT.to_csv('Arkusze/SKMES sh714 (Ekspr+MM)/Macierze Metylacji/temp/reindex/MM_WT_temp.csv', sep= ';', header= True)
MM_WT = pd.read_csv('Arkusze/SKMES sh714 (Ekspr+MM)/Macierze Metylacji/temp/reindex/MM_WT_temp.csv', delimiter= ';')
del MM_WT['Unnamed: 0']

#---------------CODE-----------------------------
print(f'--------------------------------------')
print(f'START: FIND NON TSS1500 AND TSS200 INDEX')

#---find me shLUC to del---
shLUC_row_nmb = len(MM_shLuc.index)
shLUC_TSS_indx = list()     #get rows indx with TSS1500 or TSS200
shLUC_del = list()          #get row index without TSS1500 or TSS200

for row in range(0, shLUC_row_nmb):
    chck_loc = MM_shLuc.at[row, 'Localization']
    if 'TSS1500' in chck_loc:
        shLUC_TSS_indx.append(row)
    else:
        if 'TSS200' in chck_loc:
            shLUC_TSS_indx.append(row)
        else:
            shLUC_del.append(row)
#---find me shLUC to del----
WT_row_nmb = len(MM_WT.index)
WT_TSS_indx = list()     #get rows indx with TSS1500 or TSS200
WT_del = list()          #get row index without TSS1500 or TSS200

for row in range(0, WT_row_nmb):
    chck_loc = MM_WT.at[row, 'Localization']
    if 'TSS1500' in chck_loc:
        WT_TSS_indx.append(row)
    else:
        if 'TSS200' in chck_loc:
            WT_TSS_indx.append(row)
        else:
            WT_del.append(row)
print(f'END: FIND NON TSS1500 AND TSS200 INDEX')
print(f'--------------------------------------')

#---------------TEST-----------------------
TEST_shLuc = MM_shLuc.copy()
TEST_WT = MM_WT.copy()

TEST_shLuc.drop(shLUC_TSS_indx, axis = 0, inplace= True)
TEST_WT.drop(WT_TSS_indx, axis = 0, inplace= True )

TEST_shLuc.to_csv('Arkusze/SKMES sh714 (Ekspr+MM)/Macierze Metylacji/temp/NO TSS/MM_shLuc_NO_TSS.csv', sep=';', header=True)
TEST_WT.to_csv('Arkusze/SKMES sh714 (Ekspr+MM)/Macierze Metylacji/temp/NO TSS/MM_WT_NO_TSS.csv', sep=';', header=True)
#---------------TEST-----------------------

#-------DEL NON TSS1500 OR TSS200 ROWS----------
print(f'START: DEL NON TSS ROWS')
MM_shLuc.drop(shLUC_del, axis = 0, inplace= True)
MM_WT.drop(WT_del, axis = 0, inplace= True )
print(f'END: DEL NON TSS ROWS')
print(f'--------------------------------------')

#---------------SAVE TSS1500 and TSS200 filtered------------------------
MM_shLuc.to_csv('Arkusze/SKMES sh714 (Ekspr+MM)/Macierze Metylacji/temp/TSS_filtered/MM_shLuc_TSS_filtered.csv', sep=';', header=True)
MM_WT.to_csv('Arkusze/SKMES sh714 (Ekspr+MM)/Macierze Metylacji/temp/TSS_filtered/MM_WT_TSS_filtered.csv', sep=';', header=True)

#--------------LOAD and Del first col---------------------
MM_shLuc = pd.read_csv('Arkusze/SKMES sh714 (Ekspr+MM)/Macierze Metylacji/temp/TSS_filtered/MM_shLuc_TSS_filtered.csv', delimiter = ';')
del MM_shLuc['Unnamed: 0']
MM_WT = pd.read_csv('Arkusze/SKMES sh714 (Ekspr+MM)/Macierze Metylacji/temp/TSS_filtered/MM_WT_TSS_filtered.csv', delimiter= ';')
del MM_WT['Unnamed: 0']

#========================EDIT VALUES==========================================
print('START: DEL GENES WITH LOC != TSS1500 AND TSS200')
MM_shLuc['Gene_Symbol'] = MM_shLuc['Gene_Symbol'].apply(lambda x: x.split(';')) #create list from string by split string by ';'
MM_shLuc['Localization'] = MM_shLuc['Localization'].apply(lambda x: x.split(';'))

MM_WT['Gene_Symbol'] = MM_WT['Gene_Symbol'].apply(lambda x: x.split(';'))
MM_WT['Localization'] = MM_WT['Localization'].apply(lambda x: x.split(';'))

loc_merg_lst = functools.reduce(operator.iadd, MM_shLuc['Localization'].tolist(), []) #get list of list from ['Localization'] col and merge all to one list
#also we can use operator.iconcat than operator.iadd, both equal fast with many small list, or few long lists
loc_merg_lst = np.unique(loc_merg_lst)              #get uniq values from list, now it is numpy array !!!
loc_del = [x  for x in loc_merg_lst if (x != 'TSS1500' and x != 'TSS200')]  #get values to del from loc (values different than TSS1500 and TSS200)
print(f'\tval different than TSS1500, TSS200: {loc_del}')

#=====================IT WILL BE FUNCTION=========================

row_nmb = len(MM_shLuc.index)
for row in range(0, row_nmb):
    loc_val = MM_shLuc.at[row, 'Localization']
    check = any(item in loc_del for item in loc_val)
    if check == True:
        edit_cell





#---------------SAVE FILE------------------------
# MM_shLuc.to_csv('', sep=';', header=True)
# MM_WT.to_csv('', sep=';', header=True)