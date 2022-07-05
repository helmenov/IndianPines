# IndianPines Dataset

IndianPine Site3 [dataset] taken by AVIRIS, an aerial imaging camera equipped with a high-resolution sensor, can be read by scikit-learn.

[dataset]:https://purr.purdue.edu/publications/1947/1

## module install

```{shell}
pip install git+https://github.com/helmenov/IndianPines
```

## provides

- *Readme.md* : This document self
- *setup.py* : Script required for installing the package by pip
- *__init__.py* : constructor for the provided modules
- *dataset.py* : Main module includes two function `load` and `make_dataset`
- *example.py*: sample code
- *resource/*
  - *IndianPines.rst*: Description for dataset

## usage

```
import IndianPines as pines
```

### IndianPines.load

```
load(
  pca = 0,
  include_background = True,
  recategorize_rule = None,
  exclude_WaterAbsorptionChannels = True,
)
```

#### Inputs

- `pca` : Parameter for PCA (default: `0`)
  - `pca` == 0: No compression
  - 0 < `pca` < 1 (float): contribution ratio
  - `pca` >= 1 (int): number of dimensions after compression
  - it effects the bunch shape (if >0, ($145 * 145$, $220$)->($145 * 145$, #_of_features))

- `include_background` : whether the background (un-registered) samples are included in the Bunch or not. (default: `True`)
  - it effects the bunch shape (if False, ($145 * 145$, $220$)->(#_of_samples, $220$))

- `recategorize_rule` : (default: None)
  - original data is categorized 16-category and background. But some categories are very few counted. Therefore you can reserve Transform Table as following format, and set it in this option.
  
  if you recategorize in following new categories

  |BackGround|Alfalfa|Corn|Grass|Hay-windrowed|Soybeans|Wheat|Woods|Bldg-Grass-Tree-Drives|Stone-steel towers|
  |---|---|---|---|---|---|---|---|---|---|
  |#ffffff|#ff0088|#0000ff|#007f7f|#a2b5cd|#da70d6|#ffa500|#884428|#00ff00|#ffff00|

  in following transform rule

  |original|0|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|
  |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
  |recategorized|0|1|2|2|2|3|3|0|4|0|5|5|5|6|7|8|9|

  , you should write following CSV file.

  ```
  BackGround,Alfalfa,Corn,Grass,Hay-windrowed,Soybeans,Wheat,Woods,Bldg-Grass-Tree-Drives,Stone-steel towers
  #ffffff,#ff0088,#0000ff,#007f7f,#a2b5cd,#da70d6,#ffa500,#884428,#00ff00,#ffff00
  0,1,2,2,2,3,3,0,4,0,5,5,5,6,7,8,9
  ```
  
- exclude_WaterAbsorptionChannels: (default: True)
  - some original channels are effected by water absorption. Gualtieri and Cromp [SC99] have suggested to reduce [104-108], [150-163], and 220 -th channel (20-channels) for Analysis.
  - [SC99] J.A. Gualtieri, R.F. Cromp, ``Support vector machines for hyperspectral remote sensing classification,'' 27th AIPR workshop: Advances in Computer-assisted Recognition, vol. 3584, pp. 221-232. SPIE, 1999.

- gt_gic: (default: True)
  - ground truth labels from GIC's MAT-file
  - if False, from original bundle's TIF-file


#### Outputs
  - Bunch（compatiple with scikit-learn）
    - **.features** : ($145 * 145$, #-features) numpy arrays in float raw
    - **.feature_names**：columns name of each features 
    - **.target** ：($145 * 145$, ) numpy array in integer (indexed in 'target_names')
    - **.target_names**：(#-categories, ) numpy array in strings. category names corresponding with indexes
    - **.cordinates** ：($145 * 145$, 2) numpy arrays in integer. x-y cordinates: column-numbers and row-numbers, for each samples 
    - **.cordinate_names**：(2,) numpy array in strings. cordinates name: ['#columns', '#rows']
    - **.hex_names**：(#-categories,) numpy array in strings. hex-color format (ex, '#0000' for black) for each category indexed in 'target_names'
    - **.DESCR**：description for dataset
    - **.filename**：CSV file name saved features and targets

### IndianPines.make_dataset

Input and Output are None.

This function called from IndianPines.load if you haven't download the original bundles from Pardue University yet. (to guard redundant downloads)

It also make CSV-format dataset.
