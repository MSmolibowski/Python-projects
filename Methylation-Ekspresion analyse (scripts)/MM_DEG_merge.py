#-----------------Libraries----------------------
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np

#----------------Functions-----------------------


#---------------Load Data------------------------
DEG_data = pd.read_csv('DEG-MM shared/DEG_MM_shared.csv', delimiter= ';')
del DEG_data['Unnamed: 0']
MM_data = pd.read_csv('DEG-MM shared/MM_DEG_shared.csv', delimiter= ';')
del MM_data['Unnamed: 0']
col_names = pd.read_csv('DEG-MM shared/Nazwy kolumn do finalnego arkusza.csv', delimiter= ';') #read file with prepared col names
col_names = col_names.columns.tolist()                                                              #extract column names
col_names = col_names[8:]             #select only col names that are not in DEG_df

#---------------CODE-----------------------------
#add new columns to DEG_df and fill cells with '-'
for x in col_names:         #take name of column from list,
    DEG_data[x] = '-'       #create column, fill with '-'

#-------'Ekspresja up/down'------
eksp_shLUC = DEG_data['Zmiana poziomu ekspresji-shLUC'].apply(lambda x: x.replace(',', '.')) #!!!! remember to check how numbers are writen,
eksp_shLUC = eksp_shLUC.tolist()
eksp_WT = DEG_data['Zmiana poziomu ekspresji-WT'].apply(lambda x: x.replace(',', '.'))      #in PYTHON '4,5 is incorect, '4.5' is corect !!!
eksp_WT = eksp_WT.tolist()
#print(DEG_data.columns.tolist())
DEG_row_nmb = len(DEG_data.index)
DEG_row_nmb_range = list(range(0, DEG_row_nmb))
#print(DEG_row_nmb_range)
for idx, ex_Luc, exp_WT in zip(DEG_row_nmb_range, eksp_shLUC, eksp_WT):   #iterare in 3 lists
    ud_Luc = 'up' if float(ex_Luc) > 0 else 'down'          #if in one line
    ud_WT = 'up' if float(exp_WT) > 0 else 'down'
    # print(ex_Luc, '--', exp_WT)
    # print(ud_Luc,'---',ud_WT)
    DEG_data.at[idx,'Ekspresja up/down (shLuc | WT)'] = f'{ud_Luc} | {ud_WT}' #insert new value to existing cell
print('END: Check expression up-down')
print('-----------------------------')

#----------Number of probes (total)------
print('START: Create lists and copy values')

for row, gen_name in zip(DEG_row_nmb_range, DEG_data['Gene_Symbol'].tolist()):                                               #take gene name from DEG_data
    genes_indx_lst = MM_data.index[(MM_data['UCSC_RefGene_Name-WT'] == gen_name)].tolist()      #find this gene index in MM_data
    #--------LISTS FOR VALUE's------------------
    probe_ID_lst = list()
    annotation_lst = list()
    shLUC_hyper_probe_lst = list()
    shLUC_hypo_probe_lst = list()
    shLUC_met_val_lst = list()
    WT_hyper_probe_lst = list()
    WT_hypo_probe_lst = list()
    WT_met_val_lst = list()

    for g_indx in genes_indx_lst:                                                                 #find probes ID by index of gene
        #-----------GET PROBE ID-------------
        probeID = MM_data.at[g_indx, 'TargetID-WT']                                               #find probeID val
        probe_ID_lst.append(probeID)                                                              #add this ID to list

        #----------GET ANNOTATION------------
        annotation = MM_data.at[g_indx, 'annotation-WT']
        annotation_lst.append(annotation)

        #---------GET hyper/hypo MET COMMENT---
        shLUC_hyp_chck = MM_data.at[g_indx, 'metylacja_comment-shLUC']
        WT_hyp_chck = MM_data.at[g_indx, 'metylacja_comment-WT']

        if shLUC_hyp_chck == 'hyper':
            shLUC_hyper_probe_lst.append(shLUC_hyp_chck)
        elif shLUC_hyp_chck == 'hypo':
            shLUC_hypo_probe_lst.append(shLUC_hyp_chck)

        if WT_hyp_chck == 'hyper':
            WT_hyper_probe_lst.append(WT_hyp_chck)
        elif WT_hyp_chck == 'hypo':
            WT_hypo_probe_lst.append(WT_hyp_chck)

        #-------GET METHYLATION VALUES-----
        shLUC_met_val = MM_data.at[g_indx, 'metylacja_value-shLUC']
        shLUC_met_val_lst.append(shLUC_met_val)

        WT_met_val = MM_data.at[g_indx, 'metylacja_value-WT']
        WT_met_val_lst.append(WT_met_val)

    #--------------------------------------------------------------------------
    #-----------INSERT created lists to correct rows in collumns---------------
    DEG_data.at[row, 'Number of probes (total)'] = f'{len(probe_ID_lst)}'                       #insert numb of probes
    DEG_data.at[row, 'Probes ID'] = probe_ID_lst                                           #insert probeID list
    DEG_data.at[row, 'Annotation'] = annotation_lst
    DEG_data.at[row, 'Hyper probes (shLuc | WT)'] = f'{len(shLUC_hyper_probe_lst)}|{len(WT_hyper_probe_lst)}'
    DEG_data.at[row, 'Hypo probes (shLuc | WT)'] = f'{len(shLUC_hypo_probe_lst)}|{len(WT_hypo_probe_lst)}'
    DEG_data.at[row, 'Hyper : Hypo (shLuc | WT)'] = f'shLUC: {len(shLUC_hyper_probe_lst)}:{len(shLUC_hypo_probe_lst)} | WT: {len(WT_hyper_probe_lst)}:{len(WT_hypo_probe_lst)}'
    DEG_data.at[row, 'metylacja_value-shLUC'] = shLUC_met_val_lst
    DEG_data.at[row, 'metylacja_value-WT'] = WT_met_val_lst
    #print(f'Gene: {gen_name}; Numb of probes: {len(probe_ID_lst)}; Probes_ID: {probe_ID_lst}')
print('END: Create lists and copy values')

#---------------SAVE FILE------------------------
DEG_data.to_csv('DEG-MM shared/Results/DEG_MM_merged_final_df.csv', sep= ';', header= True)