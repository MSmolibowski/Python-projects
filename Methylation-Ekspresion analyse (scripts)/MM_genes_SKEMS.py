#-------------Description-----------------


#------------Libraries--------------------
import pandas as pd

#------------Functions--------------------

#------------Load data--------------------
MM_WT = pd.read_csv("Metylacja/Przygotowane arkusze dla skryptu/AX-AZ/MM_SKMES_WT.csv", delimiter=';')
MM_shLUC = pd.read_csv("Metylacja/Przygotowane arkusze dla skryptu/AX-AZ/MM_SKMES_shLUC.csv", delimiter=';')

#-------Select rows without nan value----------
MM_WT = MM_WT[~MM_WT['GencodeBasicV12_NAME'].isnull()]       #copy rows without 'NaN' in gene names col ['UCSC_RefGene_Name']~FOR AL-AZ; AL-AN;['GencodeBasicV12_NAME']~FOR AX-AZ
MM_WT = MM_WT[~MM_WT['annotation'].isnull()]  #copy rows without 'NaN' in annotation(localization)

MM_shLUC = MM_shLUC[~MM_shLUC['GencodeBasicV12_NAME'].isnull()]
MM_shLUC = MM_shLUC[~MM_shLUC['annotation'].isnull()]
#MM_shLUC_fl = MM_shLUC_noNaN.loc[MM_shLUC_noNaN['annotation'].isin(['TSS1500', 'TSS200'])] #not working as I thought

#-----save and load--------
MM_WT.to_csv("Metylacja/Przygotowane arkusze dla skryptu/pomocnicze/WT_help.csv", sep = ';', header = True)
MM_WT = pd.read_csv("Metylacja/Przygotowane arkusze dla skryptu/pomocnicze/WT_help.csv", delimiter= ';')
del MM_WT['Unnamed: 0']

MM_shLUC.to_csv("Metylacja/Przygotowane arkusze dla skryptu/pomocnicze/shLUC_help.csv", sep = ';', header= True)
MM_shLUC = pd.read_csv("Metylacja/Przygotowane arkusze dla skryptu/pomocnicze/shLUC_help.csv", delimiter= ';')
del MM_shLUC['Unnamed: 0']

#----------NOW DF HAS CORRECT INDEX-----------------
WT_targetID = MM_WT['TargetID'].tolist()                     #get probes ID
shLUC_targetID = MM_shLUC['TargetID'].tolist()

shared_probes_ID_list = list()   #genes lists

print('Start finding shared probes_ID')

#select sharing and non sharing genes_ID (probes_ID)
for x in WT_targetID:
    if x in shLUC_targetID:
        shared_probes_ID_list.append(x)

print('Found all shared ID')

#------------CREATE NEW DF (of sharing genes)--------
col_names = MM_WT.columns.tolist()
col_names.append('metylacja_value')
col_names.append('metylacja_comment')
MM_shared = pd.DataFrame(columns = col_names)
print('Start copy values')
row_counte = 0                                                      #count in witch row insert values
for x in shared_probes_ID_list:
    WT_snd_IX = MM_WT.index[(MM_WT['TargetID']==x)].tolist()          #get index of probesID in MM_WT df.
    shLUC_snd_IX = MM_shLUC.index[(MM_shLUC['TargetID']==x)].tolist() #get index of probesID in MM_shLUC df.
    values_to_insert_list = list()                                    #list for values to insert

    if WT_snd_IX != []:
        WT_snd_IX = WT_snd_IX[0]
        for WT_cn in col_names[:5]:                 #get name of column
            val_WT = MM_WT.iloc[WT_snd_IX][WT_cn]  # get val from WT df
            values_to_insert_list.append(val_WT)  # insert val to list

    if shLUC_snd_IX != []:
        shLUC_snd_IX = shLUC_snd_IX[0]
        for shLUC_cn in col_names[5:]:
            val_shLUC = MM_shLUC.iloc[shLUC_snd_IX][shLUC_cn]  # get val from shLUC df
            values_to_insert_list.append(val_shLUC)  # insert val to list
    MM_shared.loc[row_counte] = values_to_insert_list #insert row
    row_counte += 1


hlp_col_nms = MM_shared.columns.tolist()                #get col nms
new_col_nms = list()
cnt = 0
for x in hlp_col_nms:
    if cnt < 5:
        temp1 = x + '-WT'
        new_col_nms.append(temp1)
    if cnt >= 5:
        temp2 = x + '-shLUC'
        new_col_nms.append(temp2)
    cnt+=1
MM_shared.columns = new_col_nms                         #assign col nms

#---------------SAVE DF's------------------
MM_shared.to_csv('Metylacja/Results/Results AX-AZ/MM_shared_full_data(AX-AZ).csv', sep=';', header=True)
print('Program END')