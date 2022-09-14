#librares
import pandas as pd

# functions
def find_test(string):  # find MIC, MBC, EC50 itd
    splited_str = string.split(';') #split string by ';'
    t_u = list()                    #create list for test and units
    for s in splited_str:           #search for test and units
        temp1 = s.split(':')

        if len(temp1) == 1:
            t_u.append(temp1[0])
    return t_u

#load csv file
data = pd.read_csv('UsedSubstances.csv', delimiter= ';')
row_number = len(data.index)    #get data frame row number
#print(data)

#create new data frame
new_dataframe = pd.DataFrame()
new_dataframe['ref'] = data['ref']
new_dataframe['Number'] = data['Number']
new_dataframe['Cation'] = data['Cation']

#create columns based on bacteria name in 'Antimicrobial'
for x in range(0, row_number):
    string_to_split = data.iloc[x, 4]   #get row x from col 4 ('Antimicrobial')
    test_name_units = find_test(string_to_split)    #use function to find test name with units
    test_numb = 0
    test_lenght = len(test_name_units)-1
    string_to_split = string_to_split.split(';') #split this string to list

    for z in string_to_split:   #iterate for created list
        if z in test_name_units and test_numb < test_lenght:
            test_numb+=1
        #print(test_name_units[test_numb])
        bact_value = z.split(':')   #split list object to bact name and value

        if z not in test_name_units:                                        #don't create 'test-test' name column
            new_col_name = bact_value[0]+'--'+test_name_units[test_numb]    #create new col name

        col_names = new_dataframe.columns.values.tolist() #get colum names of dataframe

        if new_col_name not in col_names:       #check if col_name is in dataframe
            new_dataframe[new_col_name] = '-'   #create new column and fill all cells with '-'

        if len(bact_value) > 1:                 #select only bacteria and values; don't take test names
            new_dataframe.iloc[x, new_dataframe.columns.get_loc(new_col_name)] = ' '+bact_value[1] #' ' to not change the value to data time in csv file
    test_name_units.clear()     #cleat list

#--------------------SAVE DATAFRAME-------------------------------------------------------------------------
new_dataframe.to_csv('Bacteria_FullDataFrame.csv', sep= ';', header= True)      # save created dataframe (bateria names with test in different columns)

#--------------------SELECT COLUMNS ONLY WITH UNITS DIFFERENT THAN 'ug/mL'-----------------------------------

data_to_recalculate = pd.DataFrame()    #new dataframe
col_names_to_check = new_dataframe.columns.tolist() #get col names

for c_name in col_names_to_check:
    if 'ug/mL' not in c_name:           #select columns with values different than ug/mL
        data_to_recalculate[c_name] = new_dataframe[c_name]

#--------------------SAVE DATAFRAME-------------------------------------------------------------------------
data_to_recalculate.to_csv('mM_to_uM.csv', header= True, sep= ';')   #save dataframe to csv file,

