# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['IndianPines']

package_data = \
{'': ['*'], 'IndianPines': ['resource/*', 'resource/recategorize_rules/*']}

install_requires = \
['importlib>=1.0.4,<2.0.0',
 'numpy>=1.22.4,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'requests>=2.28.0,<3.0.0',
 'scikit-image>=0.19.3,<0.20.0',
 'scikit-learn>=1.1.1,<2.0.0',
 'scipy>=1.8.1,<2.0.0',
 'tifffile>=2022.5.4,<2023.0.0',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'indianpines',
    'version': '0.1.11',
    'description': 'Indian Pines datasets for scikit-learn',
    'long_description': "# IndianPines Dataset\n\nIndianPine Site3 [dataset] taken by AVIRIS, an aerial imaging camera equipped with a high-resolution sensor, can be read by scikit-learn.\n\n[dataset]:https://purr.purdue.edu/publications/1947/1\n\n## module install\n\n```{shell}\npip install git+https://github.com/helmenov/IndianPines\n```\n\n## provides\n\n- *`Readme.md`* : This document self\n- *`setup.py`* : Script required for installing the package by pip\n- *`__init__.py`* : constructor for the provided modules\n- *`dataset.py`* : Main module includes two function `load` and `make_dataset`\n- *`example.py`*: sample code\n- *`resource/`*\n  - *`IndianPines.rst`*: Description for dataset\n  - *`LabelsFromTIF.rst`*: Description for Original Ground Truth\n  - *`LabelsFromMAT.rst`*: Description for GIC Ground Truth\n  - *`ReduceWaterAbsorption.rst`*: Description for Reducing Water Absorption Channels\n  - *`recategorize_rules/`*\n    - *`recategorize17to10.csv`*: recategorize_rule example. which recategorize original 17 categories to 10 categories.\n\n## usage\n\n```\nimport IndianPines as pines\n```\n\nsee [example](example.ipynb)\n\n### IndianPines.load\n\n```\nload(\n  pca = 0,\n  include_background = True,\n  recategorize_rule = None,\n  exclude_WaterAbsorptionChannels = True,\n)\n```\n\n#### Inputs\n\n- `pca` : Parameter for PCA (default: `0`)\n  - `pca` == 0: No analized\n  - 0 < `pca` < 1 (float): contribution ratio\n  - `pca` >= 1 (int): number of dimensions after compression\n  - `pca` < 0 : No compression but analyzed PCs\n  - it effects the bunch shape (if >0, ($145 * 145$, $220$)->($145 * 145$, #_of_features))\n\n- `include_background` : whether the background (un-registered) samples are included in the Bunch or not. (default: `True`)\n  - it effects the bunch shape (if False, ($145 * 145$, $220$)->(#_of_samples, $220$))\n\n- `recategorize_rule` : (default: None)\n  - original data is categorized 16-category and background. But some categories are very few counted. Therefore you can reserve Transform Table as following format, and set it in this option.\n\n  if you recategorize in following new categories\n\n  |BackGround|Alfalfa|Corn|Grass|Hay-windrowed|Soybeans|Wheat|Woods|Bldg-Grass-Tree-Drives|Stone-steel towers|\n  |---|---|---|---|---|---|---|---|---|---|\n  |#ffffff|#ff0088|#0000ff|#007f7f|#a2b5cd|#da70d6|#ffa500|#884428|#00ff00|#ffff00|\n\n  in following transform rule\n\n  |original|0|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|\n  |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n  |recategorized|0|1|2|2|2|3|3|0|4|0|5|5|5|6|7|8|9|\n\n  , you should write following CSV file.\n\n  ```\n  BackGround,Alfalfa,Corn,Grass,Hay-windrowed,Soybeans,Wheat,Woods,Bldg-Grass-Tree-Drives,Stone-steel towers\n  #ffffff,#ff0088,#0000ff,#007f7f,#a2b5cd,#da70d6,#ffa500,#884428,#00ff00,#ffff00\n  0,1,2,2,2,3,3,0,4,0,5,5,5,6,7,8,9\n  ```\n\n- `exclude_WaterAbsorptionChannels`: (default: True)\n  - some original channels are effected by water absorption. Gualtieri and Cromp [SC99] have suggested to reduce [104-108], [150-163], and 220 -th channel (20-channels) for Analysis.\n  - [SC99] J.A. Gualtieri, R.F. Cromp, ``Support vector machines for hyperspectral remote sensing classification,'' 27th AIPR workshop: Advances in Computer-assisted Recognition, vol. 3584, pp. 221-232. SPIE, 1999.\n\n- `gt_gic`: (default: True)\n  - ground truth labels from GIC's MAT-file\n  - if False, from original bundle's TIF-file\n\n\n#### Outputs\n  - Bunch（compatiple with scikit-learn）\n    - **.features** : ($145 * 145$, #-features) numpy arrays in float raw\n    - **.feature_names**：columns name of each features\n    - **.target** ：($145 * 145$, ) numpy array in integer (indexed in 'target_names')\n    - **.target_names**：(#-categories, ) numpy array in strings. category names corresponding with indexes\n    - **.coordinates** ：($145 * 145$, 2) numpy arrays in integer. x-y coordinates: column-numbers and row-numbers, for each samples\n    - **.coordinate_names**：(2,) numpy array in strings. cordinates name: ['#columns', '#rows']\n    - **.hex_names**：(#-categories,) numpy array in strings. hex-color format (ex, '#0000' for black) for each category indexed in 'target_names'\n    - **.DESCR**：description for dataset\n    - **.filename**：CSV file name saved features and targets\n\n  `features`, `target` and `coordinates` is ordered `for row in range(image height) for column in range(image width)`\n\n### IndianPines.make_dataset\n\nInput and Output are None.\n\nThis function called from IndianPines.load if you haven't download the original bundles from Pardue University yet. (to guard redundant downloads)\n\nIt also make CSV-format dataset.\n",
    'author': 'Kotaro SONODA',
    'author_email': 'kotaro1976@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
