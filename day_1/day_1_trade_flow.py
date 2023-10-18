import pandas as pd

# read the CSV file with utf-8 encoding
df = pd.read_csv('day_1\RFM_TRAD_FLOW.csv', encoding='gbk')
df['cumid'] = df['cumid'].astype(int)
df['transID'] = df['transID'].astype(int)

F = df.groupby(['cumid','type'])[['transID']].count()



# pivot the table
F_trans = pd.pivot_table(F,index='cumid', columns='type', values='transID')


#fill special_offer
F_trans['Special_offer'] = F_trans['Special_offer'].fillna(0)

#calculate interest rate
F_trans['interest'] = F_trans['Special_offer']/(F_trans['Special_offer']+F_trans['Normal'])
print(F_trans.head())

#2.2 通过计算M反应客户的价值信息
M = df.groupby(['cumid','type'])[['amount']].sum()


#pivot table
M_trans = M.pivot_table(index='cumid',columns='type',values='amount')

M_trans['Special_offer'] = M_trans['Special_offer'].fillna(0)
M_trans['returned_goods'] = M_trans['returned_goods'].fillna(0)
M_trans['value'] = M_trans['Special_offer'] + M_trans['returned_goods'] + M_trans['Normal']
print(M_trans.head())

#function to conver time
import time 
def to_time(t):
    time_out = time.mktime(time.strptime(t,'%d%b%y:%H:%M:%S'))
    return time_out

df['new_time'] = df.time.apply(to_time)

R = df.groupby(['cumid'])[['new_time']].max()

#
from sklearn import preprocessing

threshold = pd.qcut(F_trans['interest'],2,retbins=True)[1][1]
binarizer = preprocessing.Binarizer(threshold=threshold)
q_interest = pd.DataFrame(binarizer.transform(F_trans['interest'].values.reshape(-1,1)))
q_interest.index = F_trans.index
q_interest.columns = ['interest']

threshold = pd.qcut(R['new_time'],2,retbins=True)[1][1]
binarizer = preprocessing.Binarizer(threshold=threshold)
q_R = pd.DataFrame(binarizer.transform(R['new_time'].values.reshape(-1,1)))
q_R.index = R.index
q_R.columns = ['new_time']


threshold = pd.qcut(M_trans['value'],2,retbins=True)[1][1]
binarizer = preprocessing.Binarizer(threshold=threshold)
q_M = pd.DataFrame(binarizer.transform(M_trans['value'].values.reshape(-1,1)))
q_M.index = M_trans.index
q_M.columns = ['value']

#
analysis = pd.concat([q_interest,q_M,q_R],axis=1)
analysis = analysis[['interest','value','new_time']]
label = {
    (0,0,0):'无兴趣-低价值-沉默',
    (1,0,0):'有兴趣-低价值-沉默',
    (1,0,1):'有兴趣-低价值-活跃',
    (0,0,1):'无兴趣-低价值-活跃',
    (0,1,0):'无兴趣-高价值-沉默',
    (1,1,0):'有兴趣-高价值-沉默',
    (1,1,1):'有兴趣-高价值-活跃',
    (0,1,1):'无兴趣-高价值-活跃'
}

analysis['label'] = analysis.apply(lambda x:label[(x[0], x[1],x[2])],axis = 1)
print(analysis.head())






