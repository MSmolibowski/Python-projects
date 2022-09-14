#Library
import pandas as pd

#---------------------FUNKCJE--------------------
def recalculate(mol, val):

    if '>' in val:
        old_conc = val.replace('>', '')
        old_conc = float(old_conc)
        molar_mass = float(mol)  # molar mass of substance1

        used_subst_mass = old_conc * molar_mass  # weight in grams;   #how many substance was used to create solution with molar concentration
        used_subst_mass = (used_subst_mass) / 1000  # to get ug/mL we need to divide by 1000mL (volume of used liquid to create solution with conc 1M)

        if used_subst_mass < 0.1:
            used_subst_mass = round(used_subst_mass, 4)
        else:
            used_subst_mass = round(used_subst_mass, 2)  # round

        used_subst_mass = '>'+ str(used_subst_mass)

    else:
        old_conc = float(val)
        molar_mass = float(mol)  # molar mass of substance1

        used_subst_mass = old_conc * molar_mass  # weight in grams;   #how many substance was used to create solution with molar concentration
        used_subst_mass = (used_subst_mass) / 1000  # to get ug/mL we need to divide by 1000mL (volume of used liquid to create solution with conc 1M)

        if used_subst_mass < 0.1:
            used_subst_mass = round(used_subst_mass, 4)
        else:
            used_subst_mass = round(used_subst_mass, 2)  # round

        used_subst_mass =  ' ' + str(used_subst_mass)

    return used_subst_mass          #returned value is string

#----Function to find if there is value to copy in row-----
def check_row(i):
    row_check = recalculate_data.iloc[i]  # get whole row (index x)
    row_check = row_check[3:]  # del first 3 columns, only col with test left

    for rc in row_check:
        if '-' != rc:           #check if there is diff value than '-'
            return True
    return False

#------------------------------------------------
main_data = pd.read_csv('Bacteria_FullDataFrame.csv', delimiter=';')
recalculate_data = pd.read_csv('Bacteria_test_uM.csv', delimiter= ';')      #load data
molar_mass_data = pd.read_csv('MolarMassOfSubstance.csv', delimiter=';')

del main_data['Unnamed: 0']
del recalculate_data['Unnamed: 0']                                          #del uneccecary column

molar_row_numb = len(molar_mass_data.index.tolist())                         #get number of rows
recalculate_col_number = len(recalculate_data.columns.tolist())              #get row number

recalculate_col_names = recalculate_data.columns.tolist()
recalculate_col_names = recalculate_col_names[3:]

#---------loop to recalculate uM concentration to ug/mL
for x in range(0, molar_row_numb):
      molar_check = molar_mass_data.iloc[x, 3]                               #search in column 'Molar mass'
      if molar_check != '-':                                                 #Check if value in cell is different than '-'
           for n in recalculate_col_names:
                recal_value = recalculate_data.at[recalculate_data.index[x], n] #get value from cell by index 'x' and name of column 'n'
                if recal_value != '-':                                          #work only with cells with value diff than '-'
                    subst_in_mL = recalculate(molar_check, recal_value)         #use function and recalculate valu

                    recalculate_data.at[recalculate_data.index[x], n] = subst_in_mL

#--------rename col names in recalculate_data
NEW_recalculate_col_names = recalculate_data.columns.tolist()

for nm in range(0, recalculate_col_number):
    if 'uM' in NEW_recalculate_col_names[nm]:
        temp1 = NEW_recalculate_col_names[nm]
        NEW_recalculate_col_names[nm] = temp1.replace('uM', 'ug/mL')

recalculate_data.columns = NEW_recalculate_col_names

#------------copy columns from oryginal df with 'ug/mL' in name----------
finall_data = pd.DataFrame()
finall_data['ref'] = main_data['ref']
finall_data['Number'] = main_data['Number']
finall_data['Cation'] = main_data['Cation']

main_data_col_names = main_data.columns.tolist()
main_data_col_names = main_data_col_names[3:]
#---------copy columns  ug/mL----------------
for x in main_data_col_names:
    if 'ug/mL' in  x:
        finall_data[x] = main_data[x]

#--------copy columns from rec_data with 'ug/mL'
rec_col_name_to_find = recalculate_data.columns.tolist()
rec_col_name_to_find = rec_col_name_to_find[3:]         #gec col name from rec_data
row_numb = len(recalculate_data.index)                  #get number of columns of rec_data

finall_dt_col_names = finall_data.columns.tolist()
columns_to_cp_value = list()

for x in rec_col_name_to_find:
    if x in finall_dt_col_names:
        columns_to_cp_value.append(x)       #create list columns that values need to me copied to existing columns
    elif x not in finall_dt_col_names:
        finall_data[x] = recalculate_data[x]

#---------copy values from columns in rec_dt to existing columns in finall_dt
for cn in columns_to_cp_value:
    for rn in range(0, row_numb):
        cell_check = recalculate_data.iloc[rn, recalculate_data.columns.get_loc(cn)]
        if cell_check != '-':
            #print(cn,'------',cell_check,'   index: ', rn)
            finall_data.iloc[rn, finall_data.columns.get_loc(cn)] = cell_check

recalculate_data.to_csv('RecalculatedData.csv', sep = ';', header= True)        #contains only recalculated data
finall_data.to_csv('FinallData.csv', sep= ';', header= True)                    #contains all data (this which werent recalculated and this which were recalculated)



