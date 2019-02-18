#!/usr/bin/env python
# coding: utf-8

# In[124]:


from skimage import external
from IPython.display import display
import japanize_matplotlib
from matplotlib import pyplot
pyplot.style.use('kotaro')
import pandas as pd
import scipy as sc
import numpy as np
import os
import imageio
import zipfile

srcRoot = ("src/10_4231_R7RX991C")
srcRoot2 = ("src/TokumaShimizu")


# In[125]:


with zipfile.ZipFile('src/10_4231_R7RX991C.zip') as existing_zip:
    existing_zip.extract('10_4231_R7RX991C/bundle.zip','src')
    existing_zip.extract('10_4231_R7RX991C/documentation/Site3_Project_and_Ground_Reference_Files.zip','src')

with zipfile.ZipFile('src/10_4231_R7RX991C/bundle.zip') as existing_zip:
    existing_zip.extract('aviris_hyperspectral_data/19920612_AVIRIS_IndianPine_Site3.tif', srcRoot)
get_ipython().system('rm -Rf src/10_4231_R7RX991C/bundle.zip')

with zipfile.ZipFile('src/10_4231_R7RX991C/documentation/Site3_Project_and_Ground_Reference_Files.zip') as existing_zip:
    existing_zip.extract('Site3_Project_and_Ground_Reference_Files/19920612_AVIRIS_IndianPine_Site3_gr.tif',srcRoot)
get_ipython().system('rm -Rf src/10_4231_R7RX991C/documentation')


# In[126]:


pd.options.display.precision = 2
# Hyper 220bands
#=========
hypTif =  ("aviris_hyperspectral_data/19920612_AVIRIS_IndianPine_Site3.tif") 
srcimg = external.tifffile.imread(os.path.join(srcRoot,hypTif)) # (bands,w,h)
srcimg = srcimg.transpose(1,2,0) # (w,h,bands)
srcimg = srcimg.reshape(-1,220) # (w*h, bands)
columns=[]
for s in range(220):
    columns = columns + ["#{}".format(s)]
feature_df = pd.DataFrame(srcimg, columns=columns)
display(feature_df.describe())


# In[127]:


from matplotlib import colors

# Target RGB
#==============
grp17Tif = ("Site3_Project_and_Ground_Reference_Files/19920612_AVIRIS_IndianPine_Site3_gr.tif")
targetimg17 = external.tifffile.imread(os.path.join(srcRoot,grp17Tif)) # (w,h,bands)
targetimg17 = targetimg17.reshape(-1,3) # (w*h,bands)
targetimg17 = np.uint8(targetimg17 /256) # uint16->uint8
targethex17 = pd.Series()
for i in range(0,21025):
    #print("({r},{g},{b})".format(r=targetimg17[i,0],g=targetimg17[i,1],b=targetimg17[i,2]))
    targethex17 = targethex17.append(pd.Series(format(targetimg17[i,0]<<16|targetimg17[i,1]<<8|targetimg17[i,2],'06x')))

# Label number
#=========
labelpgm = ("true.pgm")
pgmlabels = pd.read_csv(os.path.join(srcRoot2,labelpgm), delim_whitespace=True, header=None, skiprows=3)
labels = pd.Series(np.ravel(pgmlabels.values),name='Categolies') # or pgmlabels.values.reshape(-1,1), reshape to 1-columns  
labels = labels.dropna() # delete last few Nan samples

# Label names
#========
## 17 classes
cat17 = ['BackGround','Alfalfa','Corn-notill','Corn-min','Corn',
                                                 'Grass/Pasture','Grass/Trees','Grass/pasture-mowed',
                                                 'Hay-windrowed','Oats','Soybeans-notill','Soybeans-min',
                                                 'Soybean-clean','Wheat','Woods','Bldg-Grass-Tree-Drives',
                                                 'Stone-steel towers']
dict17_for17 = {0.0:'BackGround', 1.0:'Alfalfa', 2.0:'Corn-notill', 3.0:'Corn-min', 4.0:'Corn',
                        5.0:'Grass/Pasture', 6.0:'Grass/Trees', 7.0:'Grass/pasture-mowed',
                        8.0:'Hay-windrowed', 9.0:'Oats', 10.0:'Soybeans-notill', 11.0:'Soybeans-min', 12.0:'Soybean-clean',
                        13.0:'Wheat', 14.0:'Woods', 15.0:'Bldg-Grass-Tree-Drives', 16.0:'Stone-steel towers'}
labels17 = labels.map(dict17_for17)


# In[128]:


# label vs RGBmap
#===================
## 17 classes
RGBvslabel17 = pd.DataFrame(np.array([labels17.values,targethex17.values]).T,columns=['label17','hex'])
RGBvslabel17['label17'] = RGBvslabel17['label17'].astype("category",categories=cat17, ordered=False)
display(pd.DataFrame(RGBvslabel17['label17'].value_counts()))

RGBvslabels17 = pd.concat([
    RGBvslabel17[RGBvslabel17['label17']=='BackGround'].head(1),
    RGBvslabel17[RGBvslabel17['label17']=='Alfalfa'].head(1),
    RGBvslabel17[RGBvslabel17['label17']=='Corn-notill'].head(1),
    RGBvslabel17[RGBvslabel17['label17']=='Corn-min'].head(1),
    RGBvslabel17[RGBvslabel17['label17']=='Corn'].head(1),
    RGBvslabel17[RGBvslabel17['label17']=='Grass/Pasture'].head(1),
    RGBvslabel17[RGBvslabel17['label17']=='Grass/Trees'].head(1),
    RGBvslabel17[RGBvslabel17['label17']=='Grass/pasture-mowed'].head(1),
    RGBvslabel17[RGBvslabel17['label17']=='Hay-windrowed'].head(1),
    RGBvslabel17[RGBvslabel17['label17']=='Oats'].head(1),
    RGBvslabel17[RGBvslabel17['label17']=='Soybeans-notill'].head(1),
    RGBvslabel17[RGBvslabel17['label17']=='Soybeans-min'].head(1),
    RGBvslabel17[RGBvslabel17['label17']=='Soybean-clean'].head(1),
    RGBvslabel17[RGBvslabel17['label17']=='Wheat'].head(1),
    RGBvslabel17[RGBvslabel17['label17']=='Woods'].head(1),
    RGBvslabel17[RGBvslabel17['label17']=='Bldg-Grass-Tree-Drives'].head(1),
    RGBvslabel17[RGBvslabel17['label17']=='Stone-steel towers'].head(1)
],axis=0)

hex17 = RGBvslabels17['hex'].values
RGBvslabel17['hex'] = RGBvslabel17['hex'].astype("category",categories=hex17, ordered=False)


# In[133]:


cordinate_df = pd.DataFrame([(x, y) for x in range(0,145) for y in range(0,145)],
                            columns=['column#','line#'])

#cordinate_df = cordinate_df.set_index(['column#','line#'])

labels17 = pd.Series(labels17).astype('category',categories=cat17,ordered=False)
labels17.name = 'categories#'
labels10 = pd.Series(labels10).astype('category',categories=cat10,ordered=False)
labels10.name = 'categories#'

file_name = 'data/IndianPines'

file_name = file_name+'.csv'
data = pd.concat([cordinate_df,feature_df],axis=1)
df = pd.concat([data,labels17],axis=1)
target_names = cat17
for i,v in enumerate(hex17):
    hex_names[i] = '#{code}'.format(code=v)

data = df.loc[:,df.columns!='categories#']
feature_names = data.columns
target = df[['column#','line#','categories#']] 
target['categories#'] = target['categories#'].cat.codes
n_samples = data.shape[0]
n_features = data.shape[1]

display(data)
display(feature_names)
display(target)
display(target_names)
display(hex_names)
display(n_samples)
display(n_features)

df1 = pd.DataFrame([[n_samples, n_features]])
df1.to_csv(file_name,header=False,index=False)
df2 = pd.DataFrame([target_names])
df2.to_csv(file_name,header=False,index=False,mode='a')
df3 = pd.DataFrame([hex_names])
df3.to_csv(file_name,header=False,index=False,mode='a')
df4 = pd.DataFrame([feature_names])
df4.to_csv(file_name,header=False,index=False,mode='a')
df5 = df
df5['categories#'] = df5['categories#'].cat.codes
df5.to_csv(file_name,header=False,index=False,mode='a')

        


