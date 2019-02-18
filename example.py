#!/usr/bin/env python
# coding: utf-8

# In[44]:


import dataset
from matplotlib import colors
from matplotlib import pyplot
import pandas as pd
import numpy as np

pca = 5
recategorize = True
background = False

IndianPines = dataset.load_IndianPines(pca=pca, recategorize=recategorize, background=background)

dir(IndianPines)


# In[45]:


cordinates_df = pd.DataFrame(IndianPines.cordinates, columns=IndianPines.cordinate_names)
features_df = pd.DataFrame(IndianPines.features, columns=IndianPines.feature_names)
target_df = pd.DataFrame(IndianPines.target_names[IndianPines.target],columns=['category'])
hex_df = pd.DataFrame(IndianPines.hex_names[IndianPines.target],columns=['hex-color'])
data_df = pd.concat([cordinates_df,features_df,target_df,hex_df],axis=1)
display(data_df.head(5))
display(pd.DataFrame(target_df['category'].value_counts()))

if background == False:
   new_cordinates = pd.DataFrame([(x, y) for x in range(0,145) for y in range(0,145)],columns=['column#','line#'])
   hex_old_cordinates = pd.concat([cordinates_df,hex_df],axis=1)
   cordinates_hex = pd.merge(new_cordinates, hex_old_cordinates,on=['column#','line#'],how='left')
   cordinates_hex = cordinates_hex.fillna('#ffffff')
   hex_df = cordinates_hex

pyplot.imshow(colors.to_rgba_array(hex_df['hex-color'].values).reshape([145,145,4]))
                                                                           


# In[ ]:




