import pandas as pd
import json, os,pprint

data = pd.read_csv('organisational-units_00000.csv',dtype=str)
data.loc[:,'name'] = [str(data.loc[item,'name']).replace('.','').replace(' ','_') for item in data.index]
data.loc[:,'parent_name'] = [str(data.loc[item,'parent_name']).replace('.','').replace(' ','_') for item in data.index if data.loc[item,'parent_name']]

#print(data.groupby('parent_name').head())
out =pd.DataFrame(columns=['id','value'])
print(data.loc[21,'parent_name'] in ['nan','NAN',''])
start = [ind for ind in data.index if data.loc[ind,'parent_name']in ['nan','NAN','']][0]

temp = pd.DataFrame(columns=['id','value'],index=range(0,1))
temp.loc[0,['id','value']] = [data.loc[start,'name'],None]
out = pd.concat([out,temp],ignore_index=True,axis=0)

data.loc[:,'read']=0
data.loc[start,'read']=1

indices = [ind for ind in data.index if data.loc[ind,'read']==1]

level=1

searchout = [item for item in out['id'] if len(item.split('.'))==level]
while len(searchout)!=0:
    for id in searchout:
        item = id.split('.')[-1]
        temp_list =data[data['parent_name']==item]
        #print(level, temp_list['child_short'].tolist())
        data.loc[temp_list.index,'read']=1
        temp_df = pd.DataFrame(columns=['id','value'],index=range(0,len(temp_list)))
        temp_df.loc[:,'id'] = [id+'.'+list_item for list_item in temp_list['name']]
        out =pd.concat([out,temp_df],ignore_index=True,axis=0)
    level+=1
    searchout = [item for item in out['id'] if len(item.split('.')) == level]



data.to_csv('org_flat_annotated.csv',index=None)
out.to_csv('org_tree.csv',index=None)