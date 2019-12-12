#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dataset
from matplotlib import colors
from matplotlib import pyplot
import pandas as pd
import numpy as np

pca = 5
recategorize=True
background=False
IndianPines = dataset.load_IndianPines(pca, recategorize, background)


# In[2]:


dir(IndianPines)


# In[3]:


cordinates_df = pd.DataFrame(IndianPines.cordinates, columns=IndianPines.cordinate_names)
features_df = pd.DataFrame(IndianPines.features, columns=IndianPines.feature_names)
target_df = pd.DataFrame(IndianPines.target_names[IndianPines.target],columns=['category'])
hex_df = pd.DataFrame(IndianPines.hex_names[IndianPines.target],columns=['hex-color'])
data_df = pd.concat([cordinates_df,features_df,target_df,hex_df],axis=1)
data_df = data_df.set_index(['column#','line#'])
data_df.info()


# In[4]:


# Variable 'PC2'  of  head 5 samples
display(data_df['PC2'].head(10))


# In[5]:


# datas of  sample cordicates(10,30) 
display(data_df.loc[(10,30)])


# In[6]:


display(pd.DataFrame(target_df['category'].value_counts()))


# In[7]:


if background == False:
   new_cordinates = pd.DataFrame([(x, y) for x in range(0,145) for y in range(0,145)],columns=['column#','line#'])
   hex_old_cordinates = pd.concat([cordinates_df,hex_df],axis=1)
   cordinates_hex = pd.merge(new_cordinates, hex_old_cordinates,on=['column#','line#'],how='left')
   cordinates_hex = cordinates_hex.fillna('#ffffff')
   hex_df = cordinates_hex

pyplot.imshow(colors.to_rgba_array(hex_df['hex-color'].values).reshape([145,145,4]))
                                                                


# In[8]:


Traininglist='data/TrainingSampleExample.csv'
trlist_df = pd.read_csv(Traininglist)
mapcordinates_df = pd.DataFrame([(x, y) for x in range(0,145) for y in range(0,145)],columns=['column#','line#'])
trlist_df = pd.concat([mapcordinates_df,trlist_df],axis=1)
trlist_df = trlist_df.set_index(['column#','line#'])
tr_df = pd.merge(data_df,trlist_df,on=['column#','line#'],how='left')

# sampled by tr05
trdata_df = tr_df.query('tr05>0') 

# incredients
display(pd.DataFrame(trdata_df['category'].value_counts()))

# map
tr_cordinates_hex = pd.merge(mapcordinates_df,trdata_df['hex-color'],on=['column#','line#'],how='left')
tr_cordinates_hex = tr_cordinates_hex.fillna('#ffffffff')
pyplot.imshow(colors.to_rgba_array(tr_cordinates_hex['hex-color'].values).reshape([145,145,4]))

