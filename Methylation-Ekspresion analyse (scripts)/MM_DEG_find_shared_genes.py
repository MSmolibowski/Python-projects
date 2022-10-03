#-----------------Libraries----------------------
import pandas as pd
import numpy as np
#----------------Functions-----------------------


#---------------Load Data------------------------
DEG_data = pd.read_csv('Ekspresja/Results/SKMES_shared_genes_full_data.csv', delimiter=';')
del DEG_data['Unnamed: 0']
MM_data = pd.read_csv('Metylacja/Results/Results AL-AN/MM_shared_TSS_only(AL-AN).csv', delimiter=';')
del MM_data['Unnamed: 0']
#---------------CODE-----------------------------
DEG_genes = DEG_data['Gene_Symbol'].tolist()
MM_genes = MM_data['UCSC_RefGene_Name-WT'].tolist()          #!!! IF using AX-AZ cols to sel TS1500 TS200 change col label

#-------create list of genes from MM_genes (multiple genes in cells, split them bny ';')
temp_genes = list()           #declar list
for x in MM_genes:               #selec val from MM_genes
    temp_split = x.split(';')    #split it
    for z in temp_split:         #add genes which are not in gene list to list
        if z not in temp_genes:
            temp_genes.append(z)
MM_genes = temp_genes
#--------Find shared genes between DEG and MM-------
shared_genes = list()
for x in DEG_genes:
    if x in MM_genes:
        shared_genes.append(x)

#----- Create DF for shared DEG and MM genes ------
##------Shared DEG genes
DEG_col_nms = DEG_data.columns.tolist()
DEG_shared_df = pd.DataFrame(columns= DEG_col_nms)

row_cnt = 0
for x in shared_genes:                                             #get gene name from list
    DEG_gen_idx = DEG_data.index[(DEG_data['Gene_Symbol']==x)].tolist()     #find gene index
    DEG_gen_idx = DEG_gen_idx[0]                                   #extract index to numb val
    DEG_shared_df.loc[row_cnt] = DEG_data.loc[DEG_gen_idx]         #copy row[gene_index] to row[row_cnt]
    #print(f'{x}---{DEG_gen_idx}')
    row_cnt += 1

##--------Shared MM genes----------------
MM_col_nms = MM_data.columns.tolist()
MM_shared_df = pd.DataFrame(columns=MM_col_nms)

MM_index_list = list()                                                                              #declar index list
for shg in shared_genes:                                                                            #take shared gene name
    for mm_lst in MM_data['UCSC_RefGene_Name-WT'].tolist():                                         #take each string with genes in USC_Ref column
        if shg in mm_lst:                                                                           #if shared gene name is in string
            mm_lst_idx = MM_data.index[(MM_data['UCSC_RefGene_Name-WT'] == mm_lst)].tolist()        #find index of this string
            if mm_lst_idx not in MM_index_list:                                                     #if found string index is not in index list, add it to list
                MM_index_list.append(mm_lst_idx)

#---copy by index to MM_shared_df---
row_cnt_2 = 0
for index_list in MM_index_list:        #take index_list (list of index) from MM_index_list
    for index in index_list:            #take single index from index_list
        MM_shared_df.loc[row_cnt_2] = MM_data.loc[index]
        row_cnt_2+=1

#----MM_shared_df <- del genes (USC column) that are not shared AND their localization is diffferent than TSS1500 or TSS200
MM_shared_df['UCSC_RefGene_Name-WT'] = MM_shared_df['UCSC_RefGene_Name-WT'].apply(lambda x: x.split(';'))   #convert strings in col ['UCSC_RefGene_Name-WT'] to list
MM_shared_df['annotation-WT'] = MM_shared_df['annotation-WT'].apply(lambda x: x.split(';'))





#-----------------------------START FOR LOOP----------------------------------------------------------
empty_cells_list = list()
for ID, genes_lst, annot_lst in zip(MM_shared_df['TargetID-WT'].tolist(), MM_shared_df['UCSC_RefGene_Name-WT'].tolist(), MM_shared_df['annotation-WT'].tolist()):         #take list with gens names from list created from MM_shared_df['UCSC_RefGene_Name-WT']
    gne_lst_len = len(genes_lst)                                       #take lenght of gene_lst
    del_gen_index = list()
    if gne_lst_len > 1:                                                  #work only with gn_lst with len > 1, because if ==1 then annotation is TSS1550
        #-------FIND EL INDX to DEL--------------
        for gne_nm_idx in range(0, gne_lst_len):                         #iterate by index in gene list
            gene_check = genes_lst[gne_nm_idx]                           #get gene name by index
            if gene_check not in shared_genes:                           #check if the gene name is not shared gene
                del_gen_index.append(gne_nm_idx)
        ##------DEL EL (gene) BY INDEX-----------------
        genes_lst = np.delete(genes_lst, del_gen_index)                      #del items with index == del_index
        annot_lst = np.delete(annot_lst, del_gen_index)

        #-------FIND EL (annot) INDX to DEL--------------
        annot_lst_len = len(annot_lst)                                    #get len of list after del non sharing genes
        del_annot_index = list()                                          #declar list for annot non matching index
        #print(f'genes: {genes_lst} --------annot: {annot_lst}')
        for annot_idx in range(0, annot_lst_len):                         # iterate by index in annot list
            #print(f'annot: {annot_idx} - {annot_lst_len}--- {annot_lst}')
            annot_check = annot_lst[annot_idx]  # get annot val by index
            if annot_check != 'TSS1500' and annot_check != 'TSS200':  # check if the gene name is not shared gene
                del_annot_index.append(annot_idx)
        ##------DEL EL (gene) BY INDEX-----------------
        genes_lst = np.delete(genes_lst, del_annot_index)  # del items with index == del_index
        annot_lst = np.delete(annot_lst, del_annot_index)
    #----------------END OF DEL NON SHARING GENES AND NON TSS1500 TSS200 ANNOT--------------------
    #----------------Insert values to proper cells-column-----------------------------------------
        row_indx = MM_shared_df.index[(MM_shared_df['TargetID-WT']==ID)].tolist()       #get index list of row in df which was checked
        row_indx = row_indx[0]                                                          #get only nmb
        MM_shared_df.loc[row_indx]['UCSC_RefGene_Name-WT'] = genes_lst  # insert gene list to propoer cell and column
        MM_shared_df.loc[row_indx]['annotation-WT'] = annot_lst  # insert annot list to propoer cell and column

        if len(genes_lst) == 0:         #remember witch row has empty cells in gene name and annot column
            empty_cells_list.append(row_indx)
        # else:
        #     #print(f'ID: {row_indx} ---- genes: {genes_lst} --------annot: {annot_lst}')
#-----------------------------END FOR LOOP----------------------------------------------------------

#----------------------------DEL ROWS WITH EMPTY GENE AND ANNOT COLUMNS-----------------------------
MM_shared_df.drop(empty_cells_list, axis = 0, inplace=True)                         #Del rows by index (index's of rows with empty cells in gene name and annot column






#---------------SAVE FILE------------------------
DEG_shared_df.to_csv('DEG-MM shared/DEG_MM_shared.csv', sep= ';', header= True)
MM_shared_df.to_csv('DEG-MM shared/MM_DEG_shared.csv', sep=';', header=True)