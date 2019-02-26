from sklearn.datasets.base import Bunch
import numpy as np
import pandas as pd
import csv

def load_IndianPines(pca=2,  recategorize=True, background=True):
    fname_csv = 'data/IndianPines.csv'

    with open(fname_csv,'r') as csv_file:
        reader = csv.reader(csv_file)
        temp = next(reader) # line1
        n_samples = int(temp[0])
        n_features = int(temp[1])
        temp = next(reader) # line2
        target_names = np.array(temp)
        
        temp = next(reader) # line3
        hex_names = np.array(temp)
        
        temp = next(reader) 
        data_names = np.array(temp)

        data = np.empty((n_samples, n_features))
        target = np.empty((n_samples,), dtype=np.int)
        for i, ir in enumerate(reader):
            data[i] = np.asarray(ir[:-1], dtype=np.float64)
            target[i] = np.asarray(ir[-1], dtype=np.int)

    ## data: 220features +(x,y)cordinates
    ## target: 17categories include 'BackGround'
    cordinates = data[:,0:2]
    features = data[:,2:]
    cordinate_names = data_names[0:2]
    feature_names = data_names[2:]

    #==========================================================================
    #
    # dimension reduction
    #
    if pca>0: 
        from sklearn.decomposition import PCA
        
        n_components = pca
        model = PCA(n_components=n_components, whiten=True)
        
        model.fit(features)
        features = model.transform(features)
        feature_names =[]
        for s in range(model.n_components_):
            feature_names = feature_names + ["PC{}".format(s+1)]
  
    #
    # 17categories -> 10categories
    #
    if recategorize==True:
        fname_recategorize = 'data/recategorize17to10.csv'
        with open(fname_recategorize,'r') as f:
            reader = csv.reader(f)
            temp = next(reader)
            target_names = np.array(temp)
            temp = next(reader)
            hex_names = np.array(temp)
            temp = next(reader)
            recategorize_map = np.array(temp)
        target = recategorize_map[target]
    
    #
    # remove 'BackGround' categorized data
    #
    if background == False:
        # DataFrame
        cordinates_df = pd.DataFrame(cordinates, columns=cordinate_names,dtype='int')
        features_df = pd.DataFrame(features, columns=feature_names)
        target_df = pd.DataFrame(target,columns=['category#'],dtype='int')
        temp_df = pd.concat([cordinates_df, features_df, target_df], axis=1)
        #
        temp_df = temp_df[temp_df['category#'] !=  0]

        #
        cordinates = temp_df[cordinate_names].values
        features = temp_df[feature_names].values
        target = temp_df['category#'].values
    
   ## DESCR 
    fname_descr = 'descr/IndianPines.rst'
    with open(fname_descr,'r') as rst_file:
        DESCR = rst_file.read()

    return Bunch(features=features, target=target.astype('int'), cordinates=cordinates.astype('int'), 
                 feature_names=list(feature_names), target_names=target_names, cordinate_names=list(cordinate_names), hex_names=hex_names,
                 DESCR=DESCR,  filename=fname_csv)
