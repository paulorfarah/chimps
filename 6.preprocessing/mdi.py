from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.datasets import load_iris
from sklearn.feature_selection import SelectFromModel
from sklearn.kernel_approximation import RBFSampler
import pandas as pd
import numpy as np

from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, LabelEncoder
from sklearn.model_selection import train_test_split

import gc
from sklearn import preprocessing

import matplotlib
import matplotlib.pyplot as plt

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import SelectFromModel

from sklearn.multiclass import OneVsRestClassifier
from sklearn import svm, datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import csv


def mdi(databases, main_columns, feature_names):
    # databases = ['commons-bcel', 'commons-io', 'junit4', 'pdfbox', 'wro4j']
    class_red_type = 'etc_select'
    res = pd.DataFrame()
    for db in databases:

        all_releases_df = pd.read_csv(
            # '../6.join_metrics/results/' + db + '-all-releases.csv')
        '../6.join_metrics/results/' + db + '-perf-diff-all.csv')
        all_releases_df.columns = main_columns
        all_releases_df = all_releases_df.fillna(0)
        df_filt = all_releases_df[feature_names]

        total_data_X = np.array(df_filt.copy())
        # total_data_Y = np.array(pd.DataFrame(all_releases_df.loc[:, 'will_change']))
        total_data_Y = np.array(pd.DataFrame(all_releases_df.loc[:, 'perf_change']))

        skf = StratifiedKFold(n_splits=10)

        fold_id = 0
        cm_list = []
        cr_list = []
        aucroc_list = []

        fi_list = {x: [] for x in feature_names}

        for train_index, test_index in skf.split(total_data_X, total_data_Y):
            trainX, testX = total_data_X[train_index], total_data_X[test_index]
            trainY, testY = total_data_Y[train_index], total_data_Y[test_index]

            random_state = np.random.RandomState(0)

            # start_time = time.time()
            # class_red_type = 'rbf'

            if class_red_type == 'rbf':
                # f_selector = RBFSampler(gamma=1, random_state=1, n_components=16)
                f_selector = RBFSampler(random_state=1)
                f_selector.fit(trainX)

            if class_red_type == 'etc_select':
                clf = ExtraTreesClassifier(n_estimators=50)
                clf = clf.fit(trainX, trainY.ravel())
                # f_selector = SelectFromModel(clf, prefit=True)
                f_selector = SelectFromModel(clf, prefit=True, max_features=10, threshold=-np.inf)

            if class_red_type == 'pca':
                f_selector = PCA(n_components='mle')
                f_selector.fit(trainX)

            if class_red_type != 'etc_select':
                clf = ExtraTreesClassifier(n_estimators=50)
                clf = clf.fit(trainX, trainY)

            importances = clf.feature_importances_
            std = np.std([tree.feature_importances_ for tree in clf.estimators_], axis=0)

            for fi, fi_std, fn in zip(importances, std, feature_names):
                fi_list[fn].append(fi)

            forest_importances = pd.Series(importances, index=feature_names)
            fig, ax = plt.subplots()
            forest_importances.plot.bar(yerr=std, ax=ax, rot=80, fontsize=7)
            ax.set_title("Feature importance using MDI")
            ax.set_ylabel("Mean decrease in impurity (MDI)")
            fig.tight_layout()
            fig.savefig(f'results/f_import_{db}_fold_{fold_id}-perf.pdf')

            trainX = f_selector.transform(trainX)
            testX = f_selector.transform(testX)

            clf = RandomForestClassifier(random_state=0)  # Pode usar qualquer classificador
            clf.fit(trainX, trainY.ravel())

            predictions = clf.predict(testX)

            y_true = testY
            y_pred = predictions

            cr = classification_report(y_true, y_pred, output_dict=True)
            cr_list.append(cr)
            classifier = clf
            fold_id += 1

        importances = [np.mean(fi_list[fn]) for fn in feature_names]
        std = [np.std(fi_list[fn]) for fn in feature_names]

        top_features = np.array(feature_names)[np.argsort(importances)[-20:][::-1]]

        # print(f"{db}: {top_features}")
        df = pd.DataFrame()
        df['metric'] = feature_names
        df['mdi'] = importances
        df.set_index('metric', inplace=True, drop=False)
        df['rank'] = df['mdi'].rank(method='dense', ascending=False)
        df['application'] = db
        res = pd.concat([res, df])
        top_features_csv = []
        top_features_csv.append(db)
        for tf in top_features:
            top_features_csv.append(tf)
        f = open("results/cpmp/" + db + "-top-features-perf.csv", "a")
        writer = csv.writer(f)
        writer.writerow(top_features_csv)
        f.close()

        importances = [np.mean(fi_list[fn]) for fn in top_features]
        std = [np.std(fi_list[fn]) for fn in top_features]

        forest_importances = pd.Series(importances, index=top_features)

        fig, ax = plt.subplots()
        forest_importances.plot.bar(yerr=std, ax=ax)
        ax.set_title(db)
        ax.set_ylabel("Mean decrease in impurity - MDI")
        fig.tight_layout()
        fig.savefig(f'results/f_import_{db}-perf.pdf')
    return res
