#------------Library----------------------
import pandas as pd

#---------Functions-----------------------
#     row_counter = 0                                     #which row we insert
#     col_names_list = df_to_create.columns.tolist()      #names of columns
#     #loop to create list of values that have to be insert to df
#     for x in index_list:
#         values_to_insert_list = list()
#         for z in col_names_list:
#             val = df_to_search.iloc[x][z]       #get val
#             values_to_insert_list.append(val)   #ionsert val to list
#         #print(x,'---',values_to_insert_list)
#         df_to_create.loc[row_counter] = values_to_insert_list   #insert values to specific row
#         row_counter+=1                                          #next row
#
#     return df_to_create

#------------Load data--------------------
SKMES_WT = pd.read_csv("Ekspresja/Przygotowane arkusze dla skryptu/SKMES_sh714_vs_WT.csv", delimiter= ';')
SKMES_shLUC = pd.read_csv("Ekspresja/Przygotowane arkusze dla skryptu/SKMES_sh714_vs_shLUC.csv", delimiter = ';')

#------------Create DF for shared genes---------------------
SKMES_col_names = SKMES_WT.columns.tolist()                 #get col names
SKMES_col_names.append('Zmiana poziomu ekspresji-WT')
SKMES_shared = pd.DataFrame(columns=SKMES_col_names)        #create new DF with same col names
SKMES_shared.rename(columns= {'Zmiana poziomu ekspresji':'Zmiana poziomu ekspresji-shLUC'}, inplace=True)
#print(SKMES_shared.columns.tolist())
SKMES_WT_genes_id = SKMES_WT['Gene_ID'].tolist()            #get list of genes in SKMES_WT

#Get genes names shared between WT-LUC, and not shared
WT_genes = SKMES_WT['Gene_Symbol'].tolist()
LUC_genes = SKMES_shLUC['Gene_Symbol'].tolist()

genes_in_both = list()
genes_only_in_WT = list()
genes_only_in_shLUC = list()

for x in WT_genes:
    if x in LUC_genes:
        genes_in_both.append(x)
    elif x not in LUC_genes:
        genes_only_in_WT.append(x)
for z in LUC_genes:
    if z not in WT_genes:
        genes_only_in_shLUC.append(z)

shLUC_genes_index_list = list()                                   #create list for gene index
WT_gene_index_list = list()
#find gene name index in both DF
for x in genes_in_both:
    shLUC_gene_index = SKMES_shLUC.index[(SKMES_shLUC['Gene_Symbol']==x)].tolist()    #find gene index in Luc df
    WT_gene_index = SKMES_WT.index[(SKMES_WT['Gene_Symbol']==x)].tolist()             #find gene index in WT df
    if shLUC_gene_index != []:
        shLUC_gene_index = shLUC_gene_index[0]                                          #extract index from list
        shLUC_genes_index_list.append(shLUC_gene_index)                                 #add intex to gene_index_list
    if WT_gene_index != []:
        WT_gene_index = WT_gene_index[0]
        WT_gene_index_list.append(WT_gene_index)

#-------------Find values and insert them to new DF---------------------------------
row_counter = 0
for (shLUC_ix, WT_ix) in zip(shLUC_genes_index_list, WT_gene_index_list):               #iterating on two lists
    #print(shLUC_ix, WT_ix)
    values_to_insert_list = list()
    for cn in SKMES_col_names[:-1]:      #exclude 'Zmiana poziomu ekspresji-WT' from list
        val_shLUC = SKMES_shLUC.iloc[shLUC_ix][cn]  # get val from shLUC df
        values_to_insert_list.append(val_shLUC)  # insert val to list
    val_WT = SKMES_WT.iloc[WT_ix]['Zmiana poziomu ekspresji']
    values_to_insert_list.append(val_WT)            #copy value of expression from WT df
    SKMES_shared.loc[row_counter] = values_to_insert_list  # insert values to specific row
    row_counter += 1

#----find lenght of gene names lists
lB, lW, lL = len(genes_in_both), len(genes_only_in_WT), len(genes_only_in_shLUC)
max_len = max(lB, lW, lL)
#print(max_len)

#create list with the same lenght as the longest list
if not max_len == lB:
    genes_in_both.extend(['']*(max_len-lB))
if not max_len == lW:
    genes_only_in_WT.extend(['']*(max_len-lW))
if not max_len == lL:
    genes_only_in_shLUC.extend(['']*(max_len-lL))

#Create DF with names of genes shared and not shared between WT-Luc
sv_genes_lists = pd.DataFrame({'Shared_Genes': genes_in_both, 'Only_in_WT': genes_only_in_WT, 'Only_in_shLUC': genes_only_in_shLUC}) #create DF

#------------------------SAVE DF-------------------------------------
sv_genes_lists.to_csv('SKMES_Shared_onlyWT_onlyshLUC_genes.csv', sep=';', header= True)                                                   #save DF
SKMES_shared.to_csv('SKMES_shared_genes_full_data.csv', sep=';', header= True)

# Check copied values from WT and LUC DF to new DF
# row_numb = len(SKMES_shared.index.tolist())
# row_range = range(0,row_numb)
# for (x, L, W) in zip(row_range,shLUC_genes_index_list, WT_gene_index_list):
#     col_WT = 'Zmiana poziomu ekspresji-WT'
#     col_Luc = 'Zmiana poziomu ekspresji-shLUC'
#     col_GN = 'Gene_Symbol'
#     temp = 'Zmiana poziomu ekspresji'
#     print(f'GN from Created DF: {SKMES_shared.iloc[x][col_GN]}>>>{SKMES_shLUC.iloc[L][col_GN]} Gene name from LUC >>>> {SKMES_WT.iloc[W][col_GN]} Gene name from WT')
#     print(f'val from Created DF_LUC: {SKMES_shared.iloc[x][col_Luc]}>>>{SKMES_shLUC.iloc[L][temp]} Gene name from LUC')
#     print(f'val from Created DF_WT: {SKMES_shared.iloc[x][col_WT]}>>>{SKMES_WT.iloc[W][temp]} Gene name from WT')
#     print(f'---------------')


#-----------do metylacji wyciaganie wierszy bez nan--------------------
# WT_noNaN = WT[~WT['UCSC_RefGene_Name_WT'].isnull()]
# WT_genes = WT_noNaN['UCSC_RefGene_Name_WT'].tolist()
# shLUC_noNaN = shLUC[~shLUC['UCSC_RefGene_Name_shLUC'].isnull()]
# shLUC_genes = shLUC_noNaN['UCSC_RefGene_Name_shLUC'].tolist()

# for x in WT_genes:
#     print(shLUC_noNaN.index[(shLUC_noNaN['UCSC_RefGene_Name_shLUC']==x)].tolist())
#     WT_genes = WT_genes.remove(x)


