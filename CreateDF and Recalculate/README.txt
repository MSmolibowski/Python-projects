Why i created this code?
---------------------------------------------------------------------------
I had many names of bacteria with many test. Concentration presented between the same test were different.
To present clear data in article I had to unify them.
---------------------------------------------------------------------------
This code was designed for:
1. Creating dataframe with names of bacteria with test name, concentration and unit (as column name) of substance that were tested against them.
2. Select columns were concentration was presented not as 'uM' and 'mM'
3. Calculate concentartion from 'mM' to 'uM'
4. Calculate concentration from 'uM' to 'ug/mL
5. Create one dataframe with all concentrations
6. Create dataframe where all bacteria and substance concentration are presented as string
---------------------------------------------------------------------------

Program is separated to 4 files. Each file must by compiled separatly 
(creating main file in progress)

1.CreatePythonDataFrame.py <----- create dataframe from data saved as string, 
---------------------------------------------------------------------------
- It takes '.csv' file (!!! values separated by ';') (example file 'UsedSubstances.csv') 
and create dataframe where names of bacteria+test+units create column,
- insert concentration of used substances in to cells,
- create '.csv' file (values separated by ';') --> 'Bacteria_FullDataFrame.csv',
- create '.csv' file (values separated by ';') --> 'mM_to_uM.csv' (only with column names where units are different than 'ug/mL'),
(this columns I want to recalculate)
---------------------------------------------------------------------------

2.ChangeTo uM.py <- change units from mM to uM
---------------------------------------------------------------------------
- It takes file named 'mM_to_uM.csv',
- find values in cells and multiply them by 1000 (1mM it is 1000uM),
- save values as dataframe 'Bacteria_test_uM.csv' (values separated by ';'),
---------------------------------------------------------------------------

3.Recalculate.py <- recalculate 
---------------------------------------------------------------------------
- It takes files named: 'Bacteria_FullDataFrame.csv', 'Bacteria_test_uM.csv', 
'MolarMassOfSubstance.csv' (this one is preppared by me, It contains molar mass of used subtance which will be recalculate) 
- find values to recalculate and recalculate units in 'uM' to 'ug/mL'
- insert recalculated values from columns 'uM' to columns wih 'ug/mL',
- create '.csv' files (values separated by ';'):
	> 'RecalculatedData.csv' (recalculated values),
	> 'FinallData.csv' (All values in one file),

4.Create_Finall_String.py <- combine name columns and values to string
---------------------------------------------------------------------------
- It takes 'FinallData.csv' and create diffent dataframes for each test,
- takes single test dataframe and combine all values in row with bacteria names and create string with test name at the end of string,
- create new column and insert created strings,
- copy columns with strings (from all tests) to new dataframe,
- create '.csv' files (values separated by ';') named: 'All_data_as_string.csv'

--------------------------EXTRA---------------------------------------

ShowMeData.py <--- It's code I wrote to check If values from string are corectly transformed and saved in columns
---------------------------------------------------------------------------
- It takes file named: 'user input file name',
- check if there is file with this name in folder,
- code allows to show column names, column values and show value of specific substance (ex. AB.44) in column 'XYZ'


















