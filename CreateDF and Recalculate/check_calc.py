import pandas as pd

data = pd.read_csv('MolarMassOfSubstance.csv', delimiter=';')

menu = ''

while menu != '0':
    menu = input('Podaj numer zwiazku: ')
    if menu != '0':
        conc = input('Podaj st. zw w uM: ')

        row_to_show_index = data.index[data['Number'] == menu].tolist()  # get index of matching value in row in specific column
        row_to_show_index = row_to_show_index[0]
        molar_mass = data.iloc[row_to_show_index, 3]

        used_subst_mass = float(conc) * float(molar_mass)
        used_subst_mass = used_subst_mass/1000
        if used_subst_mass < 0.1:
            used_subst_mass = round(used_subst_mass, 4)
        else:
            used_subst_mass = round(used_subst_mass, 2)  # round

        print(f'Nr: zw.: {menu}, st. (mol): {conc}-------NOWE st: {used_subst_mass}')
