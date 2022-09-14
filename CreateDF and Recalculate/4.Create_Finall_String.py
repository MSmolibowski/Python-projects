import pandas as pd
#-------Functions-----------------
def string_maker(df_used, test_name):
    test_string = ''
    test_string_list = list()
    temp_DF = df_used
    temp_DF_col_nms = temp_DF.columns.tolist()
    temp_DF_col_nms = temp_DF_col_nms[3:]
    temp_DF_row_numb = len(temp_DF.index.tolist())


    for rn in range(0, temp_DF_row_numb):
        for cn in  temp_DF_col_nms:
            cell_v = temp_DF.loc[rn][cn]

            if cell_v != '-':
                cell_v = cell_v.replace(' ', '')
                temp_str = f'{cn}:{cell_v};'
                test_string += temp_str

        test_string_list.append(test_string+test_name)
        test_string = ''
    return test_string_list

def IZD_string_maker(df, col_names, test_name):
    temp_str = ''
    temp_str_list = list()
    IZD_df_funct = df



data = pd.read_csv('FinallData.csv', delimiter= ';')    #load data
del data['Unnamed: 0']
dt_col_names = data.columns.tolist()

row_numb = len(data.index.tolist())
#print(row_numb)

MIC_col_nms = list()
MIC_dt = pd.DataFrame()
MIC_dt['ref'] = data['ref']
MIC_dt['Number'] = data['Number']
MIC_dt['Cation'] = data['Cation']
#
MBC_col_nms = list()
MBC_dt = pd.DataFrame()
MBC_dt['ref'] = data['ref']
MBC_dt['Number'] = data['Number']
MBC_dt['Cation'] = data['Cation']
#
EC50_col_nms = list()
EC50_dt = pd.DataFrame()
EC50_dt['ref'] = data['ref']
EC50_dt['Number'] = data['Number']
EC50_dt['Cation'] = data['Cation']
#
IZO_col_nms = list()
IZD_dt = pd.DataFrame()
IZD_dt['ref'] = data['ref']
IZD_dt['Number'] = data['Number']
IZD_dt['Cation'] = data['Cation']

#create lists of test and sort them
for x in dt_col_names:
    if 'MIC' in x:
        MIC_col_nms.append(x)
    elif 'MBC' in x:
        MBC_col_nms.append(x)
    elif 'EC50' in x:
        EC50_col_nms.append(x)
    elif  'IZD' in x:
        IZO_col_nms.append(x)

# #------sorting col names--------
MIC_col_nms = sorted(MIC_col_nms)
MBC_col_nms = sorted(MBC_col_nms)
EC50_col_nms = sorted(EC50_col_nms)
IZD_col_nms = sorted(IZO_col_nms)

#------copy columns-------------
for x in MIC_col_nms:
    temp1 = x.replace('--MIC(ug/mL)', '')
    MIC_dt[temp1] = data[x]
for x in MBC_col_nms:
    temp1 = x.replace('--MBC(ug/mL)', '')
    MBC_dt[temp1] = data[x]
for x in EC50_col_nms:
    temp1 = x.replace('--EC50(ug/mL)', '')
    EC50_dt[temp1] = data[x]
for x in IZD_col_nms:
    IZD_dt[x] = data[x]


#---------Create one string--------------
created_string_list = list()
#MIC string:
created_string = string_maker(MIC_dt, 'MIC(ug/mL)')
MIC_dt['Antimicrobial'] = created_string
#MBC string:
created_string = string_maker(MBC_dt, 'MBC(ug/mL)')
MBC_dt['Antimicrobial'] = created_string
#EC50 string:
created_string = string_maker(EC50_dt, 'EC50(ug/mL)')
EC50_dt['Antimicrobial'] = created_string
#IZD
IZD_string = ''
IZD_string_list = list()
#-----------IZD  string----------------
IZD_400 = list()
IZD_1000 = list()

for x in IZD_col_nms:
    if '400' in x:
        IZD_400.append(x)
    elif '1000' in x:
        IZD_1000.append(x)

IZD_400_str = ''
IZD_400_str_list = list()

IZD_1000_str = ''
IZD_1000_str_list = list()
#---------------IZD 400 string-----------------
for rn in range(0,row_numb):
    for cn in IZD_400:
        temp_val = IZD_dt.loc[rn][cn]
        split_IZD = cn.split('--')
        if temp_val != '-':
            temp_val = temp_val.replace(' ', '')
            temp_400_str = f'{split_IZD[0]}:{temp_val};'
            IZD_400_str+= temp_400_str
            #print(cn, '---', {temp_val})

    IZD_400_str_list.append(IZD_400_str+'IZD(mm)(400ug/mL)')
    IZD_400_str = ''

#---------------IZD 1000 string-----------------
for rn in range(0,row_numb):
    for cn in IZD_1000:
        temp_val = IZD_dt.loc[rn][cn]
        split_IZD = cn.split('--')
        if temp_val != '-':
            temp_val = temp_val.replace(' ', '')
            temp_1000_str = f'{split_IZD[0]}:{temp_val};'
            IZD_1000_str+= temp_1000_str
            #print(cn, '---', {temp_val})

    IZD_1000_str_list.append(IZD_1000_str+'IZD(mm)(1000ug/mL)')
    IZD_1000_str = ''

IZD_dt['Antimicrobial-IZD(mm)(1000ug/mL)'] = IZD_1000_str_list
IZD_dt['Antimicrobial-IZD(mm)(400ug/mL)'] = IZD_400_str_list

#---------Add column to final dataframe and save---------------
last_DF = pd.DataFrame()
last_DF = pd.DataFrame()
last_DF['ref'] = data['ref']
last_DF['Number'] = data['Number']
last_DF['Cation'] = data['Cation']
last_DF['Antimicrobial-MIC'] = MIC_dt['Antimicrobial']
last_DF['Antimicrobial-MBC'] = MBC_dt['Antimicrobial']
last_DF['Antimicrobial-EC50'] = EC50_dt['Antimicrobial']
last_DF['Antimicrobial-IZD(mm)(1000ug/mL)'] = IZD_dt['Antimicrobial-IZD(mm)(1000ug/mL)']
last_DF['Antimicrobial-IZD(mm)(400ug/mL)'] = IZD_dt['Antimicrobial-IZD(mm)(400ug/mL)']
last_DF.to_csv('All_data_as_string.csv', sep=';', header=True)

# MIC_dt.to_csv('MIC.csv', sep=';', header= True)
# MBC_dt.to_csv('MBC.csv', sep=';', header= True)
# EC50_dt.to_csv('EC50.csv', sep=';', header= True)
# IZD_dt.to_csv('IZD.csv', sep=';', header= True)





