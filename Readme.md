# Indian Pine datasets

高分光センサーを搭載した航空画像AVIRISで撮影した IndianPine Site3 の[データセット]をscikit-learnで読めるようにした．

[データセット]:https://purr.purdue.edu/publications/1947/1

## module install

```{shell}
pip install git+https://github.com/helmenov/IndianPines
```

## provides

- *Readme.md* : この文書
- *setup.py* : pipで導入するために必要なスクリプト
- *dataset.py* : 主メソッド"*load_IndianPine*"（だけ）が入っているスクリプト．
- *make_datasets.py* : データセット提供元（Purdue大学）からダウンロードしてきた巨大なzipファイルから，CSVファイルを作るスクリプト
- *example.py*: 使用例
- *data/*
  - *IndianPines.csv* : 作ったデータベースCSVファイル
  - *recategorize17to10.csv* : 元はクラス数16（＋ラベル無し1）のアノテーションがあるが，いくつかのクラスは極端にサイズが小さいので，いくつかのクラスをまとめてクラス数9（＋ラベル無し）にするとよい．そのための対応表．元は {BackGround,Alfalfa,Corn-notill,Corn-min,Corn,Grass/Pasture,Grass/Trees,Grass/pasture-mowed,Hay-windrowed,Oats,Soybeans-no
till,Soybeans-min,Soybean-clean,Wheat,Woods,Bldg-Grass-Tree-Drives,Stone-steel towers}, カテゴリ修正後は {BackGround,Alfalfa,Corn,Grass,Hay-windrowed,Soybeans,Wheat,Woods,Bldg-Grass-Tree-Drives,Stone-steel towers}. カテゴリ修正後のクラスに対する16進数形式のカラーマップも提供する．
- *descr/*
  - *IndianPines.rst* : データセットの説明

## ```from IndianPines import dataset```

```{python}
Bunch dataset.load_IndianPine(pca = 2, recategorize = True, background = True)
```

- Inputs
  - **pca** : 元は220次元の高分光情報で構成されるため，主成分分析で次元圧縮する．圧縮後の次元数（N>=1），または寄与率（0<N<1），元のまま（N=0）．
  - **recategorize** : 元の17クラスから10クラスへのまとめ直し．Falseで元のまま
  - **background** : feature,targetなどにBackGroundクラスを含める．Falseで含めない（座標によってデータレコードが無くなる）
- Outputs
  - Bunch形式（scikit-learn互換）
    - **.features** : 独立変数，説明変数，分光情報（または主成分）
    - **.target** ：従属変数，目的変数，カテゴリクラス
    - **.cordinates** ：座標情報
    - **.feature_names**：各説明変数の名前
    - **.target_names**：目的変数のカテゴリクラスの名前
    - **.cordinate_names**：座標情報の名前
    - **.hex_names**：目的変数のカテゴリクラスに対応する16進数カラー
    - **.DESCR**：データセットの説明
    - **.filename**：データセットのCSVファイル名
