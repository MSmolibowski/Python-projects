#--------Library------------
import pandas as pd

MM_data = pd.read_csv('Metylacja/Results/Results AX-AZ/MM_shared_full_data(AX-AZ).csv', delimiter= ';' )        #load data
del MM_data['Unnamed: 0']                                                                                       #del unnececary column

col_nms = MM_data.columns.tolist()                  #get col names
MM_data_TSS = pd.DataFrame(columns=col_nms)         #create new DF

annot_list = MM_data['annotation-WT']               #get localization
row_nmb = len(MM_data.index)                        #get numb of rows
row_cnt = 0                                         #in which row data are insert
for x in range(0, row_nmb):                         #loop
    chck_val = MM_data.iloc[x]['annotation-WT']
    chck_val = chck_val.split(';')
    if 'TSS1500' in chck_val or 'TSS200' in chck_val:
        MM_data_TSS.loc[row_cnt] = MM_data.loc[x]
    row_cnt+=1

MM_data_TSS.to_csv('Metylacja/Results/Results AX-AZ/MM_shared_TSS_only(AX-AZ).csv', sep= ';', header= True)
