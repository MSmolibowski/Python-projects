#libraries
import pandas as pd

#load csv file
data_to_recalculate = pd.read_csv('mM_to_uM.csv', delimiter=';')
row_number = len(data_to_recalculate.index)
col_names = data_to_recalculate.columns.tolist()
del data_to_recalculate['Unnamed: 0']
col_names = data_to_recalculate.columns.tolist()

#copy data to new dataframe and change names of column to uM and calculate units to uM
help_df_mM = pd.DataFrame()
help_df_mM['ref'] = data_to_recalculate['ref']
help_df_mM['Number'] = data_to_recalculate['Number']
help_df_mM['Cation'] = data_to_recalculate['Cation']

#change name of columns
for sel_col in col_names:
    if 'mM' in sel_col:
        new_col_name = sel_col.replace('mM', 'uM')
        help_df_mM[new_col_name] = data_to_recalculate[sel_col] #create new named column with values from data_to_recalculate
#help_df_mM.to_csv('check1.csv', sep=';', header=True)

#change mM to uM in columns
col_names_uM = help_df_mM.columns.tolist()  #get headers
for c_n in col_names_uM:
     if 'uM' in c_n:        #work only with columns with values to change
         for x in range(0, row_number):     #iterate row by row
             temp_value = help_df_mM.iloc[x,help_df_mM.columns.get_loc(c_n)]    #save value from row x col c_n
             if temp_value != '-':                                              #check if there is value to change
                 if '>' in temp_value:                                          #check if there was character '>' in value from cell
                     temp_value = temp_value.replace('>', '')              #delete '>'
                     temp_val_float = float(temp_value) * 1000             #convert to float and multiply by 1000 (1mM = 1000uM)
                     temp_value_string = '>'+str(temp_val_float)           #add '>'
                 else:
                    temp_val_float = float(temp_value) * 1000               #if there is no '>', convert value to float and * 1000
                    temp_value_string = ' '+str(temp_val_float)                 #convert float to string again
                 help_df_mM.iloc[x, help_df_mM.columns.get_loc(c_n)] = temp_value_string     #insert new walue to cell [x, c_n]
#help_df_mM.to_csv('check2.csv', sep=';', header=True)


uM_data = pd.DataFrame()
uM_data['ref'] = help_df_mM['ref']
uM_data['Number'] = help_df_mM['Number']
uM_data['Cation'] = help_df_mM['Cation']

for x in col_names:     #copy column names with uM value
    if 'uM' in x:
        uM_data[x] = data_to_recalculate[x]
#uM_data.to_csv('uM_data_check1.csv', sep=';', header=True)

uM_col_names = uM_data.columns.values.tolist()         #get col names in uM_data
help_df_col_names = help_df_mM.columns.values.tolist() #get col names in help_df_mM

for x in help_df_col_names:         #find column that is not in uM_column
    if x not in uM_col_names:
        uM_data[x] = help_df_mM[x]  #add column to uM_data
        del help_df_mM[x]           #delete copied collumn

#uM_data.to_csv('uM_data_check2.csv', sep=';', header=True)
#help_df_mM.to_csv('help_df_mM_check2.csv', sep=';', header=True)

value_col_names_to_copy = help_df_mM.columns.tolist()   #get list of columns that need to be copy to existing columns
uM_df_row_numb = len(uM_data.index)                     #get row name
#print(value_col_names_to_copy)
for vcn in value_col_names_to_copy:
     if 'uM' in vcn:
         for i in range(0, uM_df_row_numb):
             cell_val = help_df_mM.iloc[i, help_df_mM.columns.get_loc(vcn)]
             if cell_val != '-':
                 uM_data.iloc[i, uM_data.columns.get_loc(vcn)] = cell_val

temp_col = data_to_recalculate.columns.tolist()

uM_data.to_csv('Bacteria_test_uM.csv', sep=';', header=True)
#temp_value = help_df_mM.iloc[x,help_df_mM.columns.get_loc(c_n)]
#uM_data.to_csv('uM_data_check1.csv', sep=';', header=True)
