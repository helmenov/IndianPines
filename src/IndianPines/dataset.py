from importlib import resources
from sklearn.utils import Bunch
import tifffile
import numpy as np
import pandas as pd
import csv
import os
import os.path
import requests
import zipfile
import shutil
from tqdm import tqdm
from PIL import Image
from scipy import io as sio
from colormap import rgb2hex

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_data")
resource_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "resource"
)

recategorize17to10_csv = os.path.join(
    resource_dir, "recategorize_rules", "recategorize17to10.csv"
)


def load(
    pca=0,
    include_background=True,
    recategorize_rule=None,
    exclude_WaterAbsorptionChannels=True,
    gt_gic=True,
):
    """IndianPines.dataset.load

    load IndianPines's raw feature data (145 x 145 image shape, and 220 hyper-spectral channels) and return the sklearn format Bunch data.

    Args:
        - pca (float, optional): if integer pca >= 1, required dimensions in PCA. if float 0<pca<1, it mean the contribution ratio in PCA. if pca==0, it means no compression. Defaults to 0.
        - include_background (bool, optional): Bunch includes background(un-studied) features and label-categories.  Defaults to True.
        - recategorize_rule (str, optional): Some original categories are too small samples. this opt. select the recategorize rule file(CSV). Defaults to None.
        - exclude_WaterAbsorptionChannels (bool, optional): Original Data includes the channels of water absorption. Gualtieri, et.al. remove those channels(AIPR1999), and the removed data has broadly used in now. Defaults to True.
        - gt_gip (bool, optional): whether labels used from gip's gt.mat or original gt.tif. (default: True, use gip's mat)

    Returns:
        sklearn format Bunch: it include following attributes.

        - features (float array(nsamples,nch)): features. `nsamples` varied depends on whether includes background or not. `nch` varied depends on whether excludes WaterAbsorptionChannels or not.
        - feature_names (str array(nch,)): column names of feature
        - target (integer arrays(nsamples,)): ground truth categories' number labeled.
        - target_names (str array(ncategories,)): Category Name indexed range(0:ncategories). `ncategories` varied depend on the recategorize_rule
        - cordinates (integer arrays(nsamples,2)): cordinates (x,y) for each samples
        - cordinate_names (str array['column#', 'row#'])
        - hex_names (str array(ncategories,)): Hex names for each category
        - DESCR
        - filename
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))

    data_dir = os.path.join(root_dir, "_data")

    if gt_gic == True:
        fname_csv = os.path.join(data_dir, "IndianPines_gic.csv")
    else:
        fname_csv = os.path.join(data_dir, "IndianPines_org.csv")
    if os.path.exists(fname_csv) == False:
        make_dataset()

    with open(fname_csv, "r") as csv_file:
        reader = csv.reader(csv_file)
        temp = next(reader)  # line1
        n_samples = int(temp[0])
        n_features = int(temp[1])
        temp = next(reader)  # line2
        target_names = np.array(temp)

        temp = next(reader)  # line3
        hex_names = np.array(temp)

        temp = next(reader)
        data_names = np.array(temp)

        data = np.empty((n_samples, n_features))
        target = np.empty((n_samples,), dtype=int)
        for i, ir in enumerate(reader):
            data[i] = np.asarray(ir[:-1], dtype=np.float64)
            target[i] = np.asarray(ir[-1], dtype=int)

    ## data: 220features +(x,y)coordinates
    ## - coordinates(x,y) for y in height(n_rows) for x in width(n_height)
    ## target: 17categories include 'BackGround'
    coordinates = data[:, 0:2]
    coordinate_names = data_names[0:2]
    features = data[:, 2:]
    feature_names = data_names[2:]

    # ==========================================================================
    #
    # Reduce Water Absorption Channels
    # [Cite] J.A. Gualtieri, R.F. Cromp, ``Support vector machines for hyperspectral remote sensing classification,'' 27th AIPR workshop: Advances in Computer-assisted Recognition, vol. 3584, pp. 221-232. SPIE, 1999.
    # ==========================================================================
    if exclude_WaterAbsorptionChannels == True:
        features = np.concatenate(
            [features[:, :103], features[:, 108:149], features[:, 163:219]],
            axis=1,
        )
        feature_names = np.concatenate(
            [
                feature_names[:103],
                feature_names[108:149],
                feature_names[163:219],
            ],
            axis=0,
        )
        n_features = feature_names.size

    # ==========================================================================
    #
    # dimension reduction
    #
    if pca > 0:
        from sklearn.decomposition import PCA

        n_components = pca
        model = PCA(n_components=n_components, whiten=True)

        model.fit(features)
        features = model.transform(features)
        feature_names = []
        for s in range(model.n_components_):
            feature_names = feature_names + ["PC{}".format(s + 1)]
    elif pca < 0:
        from sklearn.decomposition import PCA

        n_components = n_features
        model = PCA(n_components=n_components, whiten=True)

        model.fit(features)
        features = model.transform(features)
        feature_names = []
        for s in range(model.n_components_):
            feature_names = feature_names + ["PC{}".format(s + 1)]

    #
    # 17categories -> 10categories
    #
    if recategorize_rule is not None:
        fname_recategorize = recategorize_rule
        with open(fname_recategorize, "r") as f:
            reader = csv.reader(f)
            temp = next(reader)
            target_names = np.array(temp)
            temp = next(reader)
            hex_names = np.array(temp)
            temp = next(reader)
            recategorize_map = np.array(temp)
        target = recategorize_map[target].astype("int")

    #
    # remove 'BackGround' categorized data
    #
    if include_background == False:
        # DataFrame
        coordinates_df = pd.DataFrame(
            coordinates, columns=coordinate_names, dtype="int"
        )
        features_df = pd.DataFrame(features, columns=feature_names)
        target_df = pd.DataFrame(target, columns=["category#"], dtype="int")
        temp_df = pd.concat([coordinates_df, features_df, target_df], axis=1)
        #
        temp_df = temp_df[temp_df["category#"] != 0]

        #
        coordinates = temp_df[coordinate_names].values
        features = temp_df[feature_names].values
        target = temp_df["category#"].values

    ## DESCR
    descr_dir = os.path.join(root_dir, "resource")
    fname_descr = os.path.join(descr_dir, "IndianPines.rst")
    with open(fname_descr, "r") as descr_file:
        DESCR = descr_file.read()

    if gt_gic == True:
        fname_labels_descr = os.path.join(descr_dir, "LabelsFromMAT.rst")
    else:
        fname_labels_descr = os.path.join(descr_dir, "LabelsFromTIF.rst")
    with open(fname_labels_descr, "r") as labels_descr_file:
        DESCR = DESCR + labels_descr_file.read()

    if exclude_WaterAbsorptionChannels == True:
        fname_GC99 = os.path.join(descr_dir, "ReduceWaterAbsorption.rst")
        with open(fname_GC99, "r") as GC99_file:
            DESCR = DESCR + GC99_file.read()

    return Bunch(
        features=features,
        target=target.astype("int"),
        coordinates=coordinates.astype("int"),
        feature_names=list(feature_names),
        target_names=target_names,
        coordinate_names=list(coordinate_names),
        hex_names=hex_names,
        DESCR=DESCR,
        filename=fname_csv,
    )


def make_dataset():

    bundle_url = (
        "https://purr.purdue.edu/publications/1947/serve/1?render=archive"
    )
    gic_url = "https://www.ehu.eus/ccwintco/uploads/c/c4/"
    root_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(root_dir, "_data")
    print(f"{data_dir=}")
    prefix = "19920612_AVIRIS_IndianPine_Site3"
    HypTif = os.path.join(data_dir, prefix + ".tif")
    GrTif = os.path.join(data_dir, prefix + "_gr.tif")
    ClrTsv = os.path.join(data_dir, prefix + "_gr.clr")
    gt_gic_Mat = os.path.join(data_dir, "Indian_pines_gt.mat")

    if (
        os.path.exists(HypTif)
        is False | os.path.exists(GrTif)
        is False | os.path.exists(ClrTsv)
        is False | os.path.exists(gt_gic_Mat)
        is False
    ):
        if os.path.exists(data_dir) is False:
            os.mkdir(data_dir)
        file_size = int(requests.head(bundle_url).headers["content-length"])

        res = requests.get(bundle_url, stream=True)
        pbar = tqdm(total=file_size, unit="B", unit_scale=True)
        with open(
            os.path.join(data_dir, "10_4231_R7RX991C.zip"), "wb"
        ) as file:
            for chunk in res.iter_content(chunk_size=1024):
                file.write(chunk)
                pbar.update(len(chunk))
            pbar.close()

        # 配布されている 10_4231_R7RX991C.zip を解凍して，
        # ハイパースペクトル画像TIFFデータとGR画像TIFFデータをsrcRootに置く．不要なものは削除する．
        with zipfile.ZipFile(
            os.path.join(data_dir, "10_4231_R7RX991C.zip")
        ) as existing_zip:
            existing_zip.extract("10_4231_R7RX991C/bundle.zip", data_dir)
            existing_zip.extract(
                "10_4231_R7RX991C/documentation/Site3_Project_and_Ground_Reference_Files.zip",
                data_dir,
            )
        os.remove(os.path.join(data_dir, "10_4231_R7RX991C.zip"))

        with zipfile.ZipFile(
            os.path.join(data_dir, "10_4231_R7RX991C", "bundle.zip")
        ) as existing_zip:
            existing_zip.extract(
                "aviris_hyperspectral_data/19920612_AVIRIS_IndianPine_Site3.tif",
                os.path.join(data_dir, "10_4231_R7RX991C"),
            )
        os.remove(os.path.join(data_dir, "10_4231_R7RX991C", "bundle.zip"))

        with zipfile.ZipFile(
            os.path.join(
                data_dir,
                "10_4231_R7RX991C",
                "documentation",
                "Site3_Project_and_Ground_Reference_Files.zip",
            )
        ) as existing_zip:
            existing_zip.extract(
                "Site3_Project_and_Ground_Reference_Files/19920612_AVIRIS_IndianPine_Site3_gr.tif",
                os.path.join(data_dir, "10_4231_R7RX991C", "documentation"),
            )
            existing_zip.extract(
                "Site3_Project_and_Ground_Reference_Files/19920612_AVIRIS_IndianPine_Site3_gr.clr",
                os.path.join(data_dir, "10_4231_R7RX991C", "documentation"),
            )
        os.remove(
            os.path.join(
                data_dir,
                "10_4231_R7RX991C",
                "documentation",
                "Site3_Project_and_Ground_Reference_Files.zip",
            )
        )
        shutil.move(
            src=os.path.join(
                data_dir,
                "10_4231_R7RX991C",
                "aviris_hyperspectral_data",
                "19920612_AVIRIS_IndianPine_Site3.tif",
            ),
            dst=HypTif,
        )
        shutil.move(
            src=os.path.join(
                data_dir,
                "10_4231_R7RX991C",
                "documentation",
                "Site3_Project_and_Ground_Reference_Files",
                "19920612_AVIRIS_IndianPine_Site3_gr.tif",
            ),
            dst=GrTif,
        )
        shutil.move(
            src=os.path.join(
                data_dir,
                "10_4231_R7RX991C",
                "documentation",
                "Site3_Project_and_Ground_Reference_Files",
                "19920612_AVIRIS_IndianPine_Site3_gr.clr",
            ),
            dst=ClrTsv,
        )
        shutil.rmtree(os.path.join(data_dir, "10_4231_R7RX991C"))

        res_mat = requests.get(gic_url).content
        with open(gt_gic_Mat, "wb") as file:
            file.write(res_mat)

    #
    # now cannot download mat-file from gic
    #
    try:
        sio.loadmat(gt_gic_Mat)
    except ValueError as e:
        print(e)
        gt_gic_Mat = os.path.join(resource_dir, "Indian_pines_gt.mat")

    # %%　この時点で以下が揃う
    # 1. ハイパースペクトル画像データ 19920612_AVIRIS_IndianPine_Site3.tif
    # 2. 土地被覆色付け画像データ 19920612_AVIRIS_IndianPine_Site3_gr.tif
    # 3. 「カテゴリ番号, 2のRGB値, カテゴリ名」の表　19920612_AVIRIS_IndianPine_Site3_gr.clr

    # Hyper 220bands
    # =========
    srcimg = tifffile.imread(HypTif)  # (bands,w,h)
    srcimg = srcimg.transpose(1, 2, 0)  # (w,h,bands)
    srcimg = srcimg.reshape(-1, 220)  # (w*h, bands)
    columns = []
    for s in range(220):
        columns = columns + [f"c{s:03d}"]
    feature_df = pd.DataFrame(srcimg, columns=columns)

    # display(feature_df.describe())

    # from matplotlib import colors

    # targethex17: Ground-Truth RGB
    # ==============
    grimg = Image.open(GrTif)
    targetimg17 = np.array(grimg.convert("RGB"))  # (w,h,rgb)
    targetimg17 = targetimg17.reshape(-1, 3)  # (w*h,rgb)
    # targetimg17 = np.uint8(targetimg17 /256) # uint16->uint8
    targethex17 = pd.Series(dtype="str")
    for i in range(0, 21025):
        # print("({r},{g},{b})".format(r=targetimg17[i,0],g=targetimg17[i,1],b=targetimg17[i,2]))
        targethex17 = pd.concat(
            [
                targethex17,
                pd.Series(
                    rgb2hex(targetimg17[i,0],targetimg17[i,1],targetimg17[i,2]).lower()
                ),
            ]
        )
    # os.remove('_data/10_4231_R7RX991C.zip')

    Clr = pd.read_csv(ClrTsv, sep=":", skipinitialspace=True, header=None)
    n_rgb = Clr[0].str.split(expand=True)
    n_rgb.columns = ["CatNo", "R", "G", "B", "_"]
    n_rgb = n_rgb[["CatNo", "R", "G", "B"]]
    n_rgb = n_rgb.astype("uint8")
    CatName = Clr[1].str[:-1]
    CatName.columns = ["CategoryName"]
    Clr = pd.concat([n_rgb, CatName], axis=1)
    Clr.columns = ["Category#", "R", "G", "B", "CategoryName"]
    nR = Clr["R"].values
    nG = Clr["G"].values
    nB = Clr["B"].values
    lHex = [rgb2hex(nR[i], nG[i], nB[i]) for i in range(17)]
    nHex = np.array(lHex)
    SHex = pd.Series(nHex)
    hex_df = pd.DataFrame(SHex, columns=["hex"])
    Clr = pd.concat([Clr, hex_df], axis=1)
    Clr = Clr.drop(["R", "G", "B"], axis=1)

    # hex2catno = lambda x: Clr[Clr['hex'==x]]['CategoryNo']

    labels17 = list()
    cat17 = Clr["Category#"].values.tolist()
    target17 = targethex17.values
    for i in range(21025):
        for j, val in enumerate(Clr["hex"].values.tolist()):
            if target17[i] == val:
                labels17.append(cat17[j])
    labels17 = pd.Series(labels17, dtype="int")
    labels17 = pd.DataFrame(labels17, columns=["Category#"])
    labels17_org = labels17

    labels17_gic = sio.loadmat(gt_gic_Mat)["indian_pines_gt"]

    labels17_gic = pd.DataFrame(
        labels17_gic.reshape(
            145 * 145,
        ),
        columns=["Category#"],
    )

    # coordinate_df: Coordinates
    # ==========
    coordinate_df = pd.DataFrame(
        [(x, y) for y in range(0, 145) for x in range(0, 145)],
        columns=["column#", "row#"],
    )

    file_name_gic = "IndianPines_gic.csv"
    file_name_org = "IndianPines_org.csv"

    file_name_gic = os.path.join(data_dir, file_name_gic)
    file_name_org = os.path.join(data_dir, file_name_org)

    data_p = pd.concat([coordinate_df, feature_df], axis=1)
    df_gic = pd.concat([data_p, labels17_gic], axis=1)
    df_org = pd.concat([data_p, labels17_org], axis=1)

    target_names = Clr["CategoryName"]

    hex_names = list()
    for i, v in enumerate(Clr["hex"].values.tolist()):
        hex_names.append("{code}".format(code=v))
    # print(hex_names)

    data_gic = df_gic.loc[:, df_gic.columns != "Category#"]
    # print(data)
    data_org = df_org.loc[:, df_org.columns != "Category#"]

    feature_names = data_gic.columns

    n_samples = data_gic.shape[0]
    n_features = data_gic.shape[1]

    # display(data)
    # display(feature_names)
    # display(target)
    # display(target_names)
    # display(hex_names)
    # display(n_samples)
    # display(n_features)

    df1 = pd.DataFrame([[n_samples, n_features]])
    df1.to_csv(file_name_gic, header=False, index=False)
    df2 = pd.DataFrame([target_names])
    df2.to_csv(file_name_gic, header=False, index=False, mode="a")
    df3 = pd.DataFrame([hex_names])
    df3.to_csv(file_name_gic, header=False, index=False, mode="a")
    df4 = pd.DataFrame([feature_names])
    df4.to_csv(file_name_gic, header=False, index=False, mode="a")
    df_gic.to_csv(file_name_gic, header=False, index=False, mode="a")

    df1 = pd.DataFrame([[n_samples, n_features]])
    df1.to_csv(file_name_org, header=False, index=False)
    df2 = pd.DataFrame([target_names])
    df2.to_csv(file_name_org, header=False, index=False, mode="a")
    df3 = pd.DataFrame([hex_names])
    df3.to_csv(file_name_org, header=False, index=False, mode="a")
    df4 = pd.DataFrame([feature_names])
    df4.to_csv(file_name_org, header=False, index=False, mode="a")
    df_org.to_csv(file_name_org, header=False, index=False, mode="a")

if __name__ == "__main__":
    pines = load()
    count = list()
    c_all = 0
    for t,name in enumerate(pines.target_names):
        c = pines.target[pines.target==t].size
        count.append(c)
        c_all += c
    count.append(c_all)
    count = np.array(count, dtype=int)

    df_pines = pd.DataFrame(dict(target_names=np.hstack([pines.target_names,'SUM']),count=count))
    print(df_pines)
