import pandas as pd
import os.path

menu = ''
while menu != "0":
    print("---------MENU----------")
    print("Enter the number to start:")
    print("1 - Load data.")
    print("2 - Show column names.")
    print("3 - Show column values.")
    print("4 - Show row values.")
    print("5 - Show specific value (specific row + specific column)") #NOT DONE
    print("0 - EXIT.")
    print("-----------------------")
    menu = input()
    #------------------------LOAD DATA-------------------------------
    if menu == '0':
        print("Have a nice day.")
        print("-----------------------")
    if menu == '1':
        csv_name = input("Type name of csv that you want to read: ")  # get csv file name from user
        print("-----------------------")
        while csv_name == "":                                       # If user don't enter file name,
            print("You didn't enter csv file name or your file do not exist.")
            print("If you want EXIT type: 0.")
            csv_name = input("Type name of csv that you want read: ")

            if csv_name == '0':                                     # Exit loop
                csv_name = ""
                break
            print("-----------------------")

            if csv_name != "":                                      # If user enter file name
                csv_name = csv_name + '.csv'                        # create csv file name to load data
                file_exist = os.path.exists(csv_name)               # Check if there is file with this name
                if file_exist == False:                             # If there is no file with this name
                    print(f'File {csv_name}, do not exist in this folder')
                    print("-----------------------")
                    csv_name = ""
                if file_exist == True:                              #If there is file with this name
                    data_to_show = pd.read_csv(csv_name, delimiter=';')  # load data
                    if 'Unnamed: 0' in data_to_show.columns:  # del Unnamed: 0 column if in dataframe
                        del data_to_show['Unnamed: 0']
                        print(f'Loaded data head: \n {data_to_show.head()}')
        if csv_name != "":
            csv_name = csv_name + '.csv'  # create csv file name to load data
            file_exist = os.path.exists(csv_name)  # Check if there is file with this name

            if file_exist == False:  # If there is no file with this name
                print(f'File {csv_name}, do not exist in this folder')
                print("-----------------------")
                csv_name = ""
            if file_exist == True:  # If there is file with this name
                data_to_show = pd.read_csv(csv_name, delimiter=';')  # load data
                if 'Unnamed: 0' in data_to_show.columns:  # del Unnamed: 0 column if in dataframe
                    del data_to_show['Unnamed: 0']
                    print(f'Loaded data head: \n {data_to_show.head()}')
                    print("-----------------------")
    #------------------------SHOW COLUMN NAMES-------------------------------
    if menu == '2':
        data_to_show_col_names = data_to_show.columns.tolist()
        print(f'Column names of loaded data:\n {data_to_show_col_names}')
    #------------------------SHOW VALUES IN COLUMN NAMES-------------------------------
    if menu == '3':
        column_to_show = input("Type name of column that you want to see: ")
        print(f'Selected column: {column_to_show} -values: \n {data_to_show[column_to_show].tolist()}')
        print("-----------------------")

    #------------------------SHOW COLUMN NAMES-------------------------------
    if menu == '4':
        column_row_search = input("Type name of column: ")
        row_to_show = input("Type name of row that you want to see: ")
        column_numbers = len(data_to_show.columns.tolist())                                                 #get column numbers
        row_to_show_index = data_to_show.index[data_to_show[column_row_search] == row_to_show].tolist()     #get index of matching value in row in specific column
        row_to_show_index = row_to_show_index[0]                                                               #get index (as int)
        print(f'Column: {column_row_search}')
        print(f'Row: {row_to_show}')
        print("-----------------------")
        for i in range(0, column_numbers):                                                  #in every column
             row_value = data_to_show.iloc[row_to_show_index, i]                            #story value
             if row_value != '-':
                print(data_to_show.columns[i],'---->>', row_value)



## DOPISAĆ KOMENTARZE
# WPROWADZIĆ MOŻLIWOŚĆ WIELOKROTNEGO WYBORU ZWIĄZKÓW I WYŚWIETLANIA ICH WARTOŚCI