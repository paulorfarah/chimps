import csv
import itertools
import os

import numpy as np
import tensorflow as tf
import pandas as pd
from imblearn.over_sampling import RandomOverSampler, SMOTE, ADASYN
from imblearn.under_sampling import RandomUnderSampler, EditedNearestNeighbours, TomekLinks
from matplotlib import pyplot as plt
from numpy import arange
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, roc_auc_score, f1_score, accuracy_score
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


def plot_confusion_matrix(cm, dataset,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    #    print("Normalized confusion matrix")
    # else:
    #    print('Confusion matrix, without normalization')

    # print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    # tick_marks = np.arange(len(classes))
    # plt.xticks(tick_marks, classes, rotation=45)
    # plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'f'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    plt.savefig('results/cpmp/cf-' + dataset + '.png')
    plt.close()


def get_scores(y_test, y_pred, dataset, algorithm, rs, model, ws, params=[]):
    scores = []
    scores.append(dataset)
    scores.append(algorithm)
    scores.append(ws)
    scores.append(model)
    scores.append(rs)

    scores.append(f1_score(y_test, y_pred, average='micro'))
    print("F1-Score(micro): " + str(scores[-1]))

    scores.append(f1_score(y_test, y_pred, average='macro'))
    print("F1-Score(macro): " + str(scores[-1]))

    scores.append(f1_score(y_test, y_pred, average='weighted'))
    print("F1-Score(weighted): " + str(scores[-1]))

    scores.append(f1_score(y_test, y_pred, average=None))
    print("F1-Score(None): " + str(scores[-1]))

    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

    # ACC
    scores.append(accuracy_score(y_test, y_pred, normalize=True))
    print("Accuracy: " + str(scores[-1]))

    # precision
    precision = tp / (tp + fp)
    scores.append(precision)
    print("Precision: " + str(scores[-1]))

    # Sensitivity / recall
    sensitivity = tp / (tp + fn)
    scores.append(sensitivity)
    print("Sensitivity: " + str(scores[-1]))

    # Specificity
    specificity = tn / (tn + fp)
    scores.append(specificity)
    print("Specificity: " + str(scores[-1]))

    # Confusion Matrix
    cnf_matrix = confusion_matrix(y_test, y_pred)
    cnf_matrix = cnf_matrix.astype('float') / cnf_matrix.sum(axis=1)[:, np.newaxis]
    print("Confusion Matrix: [" + str(cnf_matrix[0][0]) + ", " + str(round(cnf_matrix[1][1], 2)) + "]")
    plot_confusion_matrix(cnf_matrix, dataset)

    # ROC_AUC
    scores.append(roc_auc_score(y_test, y_pred))
    print("ROC AUC score: " + str(scores[-1]))

    scores.append([tn, fp, fn, tp])
    head = ['Dataset', 'Algoritm', 'window', 'model', 'resample', 'F1-Score(micro)', 'F1-Score(macro)',
            'F1-Score(weighted)', 'F1-Score(None)', 'Accuracy', 'precision', 'Sensitivity', 'Specificity',
            'ROC AUC score',
            'Confusion matrix']

    if not os.path.exists('results/cpmp/' + dataset + '-hist-model1-3.csv'):
        f = open("results/cpmp/" + dataset + "-hist-model1-3.csv", "a")
        writer = csv.writer(f)
        writer.writerow(head)
        f.close()

    f = open("results/cpmp/" + dataset + "-hist-model1-3.csv", "a")
    writer = csv.writer(f)
    writer.writerow(scores)
    f.close()

    # if params:
    #     params = scores.append(params)
    #     f = open("results/cpmp/" + dataset + "-hist-params.csv", "a")
    #     writer = csv.writer(f)
    #     writer.writerow(params)
    #     f.close()

    return scores

def create_model(c, parameters, kf, Xtrain, Xtest, Ytrain, Ytest,  algorithm, dataset, rs, model, ws ):
    parameters = {}
    grid = GridSearchCV(estimator=c, param_grid=parameters, cv=kf, verbose=0, scoring='roc_auc')
    grid.fit(Xtrain, Ytrain)
    best_model = grid.best_estimator_
    print(grid.best_params_)
    best_model.fit(Xtrain, Ytrain)
    score = roc_auc_score(Ytest, best_model.predict(Xtest))
    print('ROC AUC score:', score)
    print("\nTEST SET:")
    get_scores(Ytest, best_model.predict(Xtest), dataset, algorithm, rs, model, ws, grid.best_params_)

def LogisticRegr_(Xtrain, Ytrain, Xtest, Ytest, dataset, rs, model, ws):
    print("\nLOGISTIC REGRESSION")
    parameters = {}
    c = LogisticRegression(random_state=42, n_jobs=-1)
    create_model(c, parameters, kf, Xtrain, Xtest, Ytrain, Ytest, 'LogisticRegression', dataset, rs, model, ws)


def RandomForest_(Xtrain, Ytrain, Xtest, Ytest, dataset, rs, model, ws):
    print("RANDOM FOREST")
    parameters = {
        'n_estimators': [int(x) for x in np.linspace(start=100, stop=2000, num=200)],
        'max_depth': [int(x) for x in np.linspace(10, 110, num=11)],
    }
    c = RandomForestClassifier(random_state=42, class_weight='balanced', n_estimators=100, n_jobs=-1)
    create_model(c, parameters, kf, Xtrain, Xtest, Ytrain, Ytest, 'RandomForest', dataset, rs, model, ws)


def NN_(Xtrain, Ytrain, Xtest, Ytest, dataset, rs, model, ws):
    print("NEURAL NETWORK")
    print("TRAIN AND VALIDATION SETS:")
    parameters = {
        'hidden_layer_sizes': [(1,), (2,), (5,), (10,), (50,), (100,), (50, 50)],
        'activation': ['relu', 'tanh'],
        'solver': ['adam', 'sgd'],
        'learning_rate': ['constant', 'adaptive'],
    }
    c = MLPClassifier(random_state=42)
    create_model(c, parameters, kf, Xtrain, Xtest, Ytrain, Ytest, 'MLP', dataset, rs, model, ws)


def DecisionTree_(Xtrain, Ytrain, Xtest, Ytest, dataset, rs, model, ws):
    print("\nDECISION TREE")
    print("TRAIN AND VALIDATION SETS:")

    parameters = {'max_depth': range(1, 11, 2)}
    c = DecisionTreeClassifier(random_state=42, class_weight='balanced')
    create_model(c, parameters, kf, Xtrain, Xtest, Ytrain, Ytest, 'DT', dataset, rs, model, ws)


def AdaBoost_(Xtrain, Ytrain, Xtest, Ytest, dataset, rs, model, ws):
    print('\nADABOOST')
    print("TRAIN AND VALIDATION SETS:")

    parameters = {'n_estimators': [10, 50, 100, 500, 1000, 5000], 'learning_rate': arange(0.1, 2.1, 0.1)}
    svc = SVC(probability=True, kernel='linear')
    c = AdaBoostClassifier(base_estimator=svc)
    create_model(c, parameters, kf, Xtrain, Xtest, Ytrain, Ytest, 'AB', dataset, rs, model, ws)


def generateStandardTimeSeriesStructure(all_releases_df, window_size, featureList):
    df = all_releases_df[all_releases_df['release'] != all_releases_df['release'].max()]
    df.drop(columns=["project", "commit", "TOTAL_CHANGES", "release", "will_change"])

    method_names_list = df['method_name'].unique().tolist()
    methodes_to_drop_list = list()
    for method_name in method_names_list:
        if len(df[df['method_name'] == method_name].iloc[::-1]) <= window_size:
            for drop_method in df.index[df['method_name'] == method_name].tolist():
                methodes_to_drop_list.append(drop_method)

    df = df.drop(methodes_to_drop_list, axis=0)
    df = df.iloc[::-1]

    method_names_list = df['method_name'].unique().tolist()
    timeseries_list = list()
    timeseries_labels = list()
    for method_name in method_names_list:
        method_sequence = df[df['method_name'] == method_name].reset_index()
        for row in range(len(method_sequence) - 1):
            window = list()
            if row + window_size < len(method_sequence) + 1:
                for i in range(window_size):
                    window.extend(method_sequence.loc[row + i, featureList].values.astype(np.float64))
                timeseries_labels.append(method_sequence.loc[row + 1, 'will_change'])
                timeseries_list.append(window)

    timeseries_X = np.array(timeseries_list)
    timeseries_X = timeseries_X[:, ~np.isnan(timeseries_X).any(axis=0)]
    timeseries_labels = np.array(timeseries_labels).astype(np.bool)
    return timeseries_X, timeseries_labels


if __name__ == '__main__':
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
    if tf.test.gpu_device_name():
        print('GPU found')
    else:
        print("No GPU found")

    # datasets = ['commons-bcel','commons-io','junit4','pdfbox','wro4j']
    # datasets = ['all']
    datasets = ['commons-bcel']

    resamples= ['NONE','RUS','ENN','TL','ROS','SMOTE','ADA']
    # resamples= ['RUS','ENN','TL','ROS','SMOTE','ADA']
    # resamples = ['NONE', 'ROS', 'SMOTE', 'ADA']
    # resamples = ['RUS', 'ENN', 'TL']

    structural_metrics = ['line', 'cbo', 'cboModified', 'fanin', 'fanout', 'wmc',
                          'rfc', 'loc', 'returnsQty', 'variablesQty', 'parametersQty', 'methodsInvokedQty',
                          'methodsInvokedLocalQty', 'methodsInvokedIndirectLocalQty', 'loopQty', 'comparisonsQty',
                          'tryCatchQty', 'parenthesizedExpsQty', 'stringLiteralsQty', 'numbersQty', 'assignmentsQty',
                          'mathOperationsQty', 'maxNestedBlocksQty', 'anonymousClassesQty', 'innerClassesQty',
                          'lambdasQty',
                          'uniqueWordsQty', 'modifiers', 'logStatementsQty', 'hasJavaDoc',
                          "AvgCyclomatic", "AvgCyclomaticModified", "AvgCyclomaticStrict",
                          "AvgEssential", "AvgLine", "AvgLineBlank", "AvgLineCode", "AvgLineComment", "CountClassBase",
                          "CountClassCoupled", "CountClassDerived", "CountDeclClass", "CountDeclClassMethod",
                          "CountDeclClassVariable", "CountDeclFile", "CountDeclFunction", "CountDeclInstanceMethod",
                          "CountDeclInstanceVariable", "CountDeclMethod", "CountDeclMethodAll",
                          "CountDeclMethodDefault",
                          "CountDeclMethodPrivate", "CountDeclMethodProtected", "CountDeclMethodPublic", "CountInput",
                          "CountLine", "CountLineBlank", "CountLineCode", "CountLineCodeDecl", "CountLineCodeExe",
                          "CountLineComment", "CountOutput", "CountPath", "CountSemicolon", "CountStmt",
                          "CountStmtDecl",
                          "CountStmtExe", "Cyclomatic", "CyclomaticModified", "CyclomaticStrict", "Essential",
                          "MaxCyclomatic", "MaxCyclomaticModified", "MaxCyclomaticStrict", "MaxEssential",
                          "MaxInheritanceTree", "MaxNesting", "PercentLackOfCohesion", "RatioCommentToCode",
                          "SumCyclomatic", "SumCyclomaticModified", "SumCyclomaticStrict", "SumEssential"]
    evolutionary_metrics = [
        'BOC', 'TACH', 'FCH', 'LCH', 'CHO', 'FRCH', 'CHD', 'WCH', 'WCD', 'WFR', 'ATAF', 'LCA', 'LCD', 'CSB', 'CSBS',
        'ACDF',
    ]
    change_distiller_metrics = [
        "TOTAL_CHANGES"
        "will_change"
    ]

    model1 = structural_metrics
    model2 = structural_metrics + evolutionary_metrics
    model3 = evolutionary_metrics

    main_columns = [
        # ck
        'file', 'class', 'method', 'constructor', 'line', 'cbo', 'cboModified', 'fanin', 'fanout', 'wmc',
        'rfc', 'loc', 'returnsQty', 'variablesQty', 'parametersQty', 'methodsInvokedQty',
        'methodsInvokedLocalQty', 'methodsInvokedIndirectLocalQty', 'loopQty', 'comparisonsQty',
        'tryCatchQty', 'parenthesizedExpsQty', 'stringLiteralsQty', 'numbersQty', 'assignmentsQty',
        'mathOperationsQty', 'maxNestedBlocksQty', 'anonymousClassesQty', 'innerClassesQty', 'lambdasQty',
        'uniqueWordsQty', 'modifiers', 'logStatementsQty', 'hasJavaDoc',

        # added
        'method_name', 'current_hash',
        # understand
        "Kind", "Name", "File", "AvgCyclomatic", "AvgCyclomaticModified", "AvgCyclomaticStrict",
        "AvgEssential", "AvgLine", "AvgLineBlank", "AvgLineCode", "AvgLineComment", "CountClassBase",
        "CountClassCoupled", "CountClassDerived", "CountDeclClass", "CountDeclClassMethod",
        "CountDeclClassVariable", "CountDeclFile", "CountDeclFunction", "CountDeclInstanceMethod",
        "CountDeclInstanceVariable", "CountDeclMethod", "CountDeclMethodAll", "CountDeclMethodDefault",
        "CountDeclMethodPrivate", "CountDeclMethodProtected", "CountDeclMethodPublic", "CountInput",
        "CountLine", "CountLineBlank", "CountLineCode", "CountLineCodeDecl", "CountLineCodeExe",
        "CountLineComment", "CountOutput", "CountPath", "CountSemicolon", "CountStmt", "CountStmtDecl",
        "CountStmtExe", "Cyclomatic", "CyclomaticModified", "CyclomaticStrict", "Essential",
        "MaxCyclomatic", "MaxCyclomaticModified", "MaxCyclomaticStrict", "MaxEssential",
        "MaxInheritanceTree", "MaxNesting", "PercentLackOfCohesion", "RatioCommentToCode",
        "SumCyclomatic", "SumCyclomaticModified", "SumCyclomaticStrict", "SumEssential",

        # evometrics
        'project', 'commit',
        'commitprevious', 'release', 'file', 'method', 'BOC', 'TACH', 'FCH', 'LCH', 'CHO',
        'FRCH', 'CHD', 'WCH', 'WCD', 'WFR', 'ATAF', 'LCA', 'LCD', 'CSB', 'CSBS', 'ACDF',
        # change distiller
        "PROJECT_NAME", "PREVIOUS_COMMIT", "CURRENT_COMMIT", "CLASS_CURRENTCOMMIT", "CLASS_PREVIOUSCOMMIT",
        "CLASS_CURRENTNAME", "CLASS_PREVIOUSNAME",
        "STATEMENT_DELETE", "STATEMENT_INSERT", "STATEMENT_ORDERING_CHANGE",
        "STATEMENT_PARENT_CHANGE", "STATEMENT_UPDATE", "TOTAL_STATEMENTLEVELCHANGES",
        "PARENT_CLASS_CHANGE", "PARENT_CLASS_DELETE", "PARENT_CLASS_INSERT", "CLASS_RENAMING",
        "TOTAL_CLASSDECLARATIONCHANGES",
        "RETURN_TYPE_CHANGE", "RETURN_TYPE_DELETE", "RETURN_TYPE_INSERT", "METHOD_RENAMING",
        "PARAMETER_DELETE", "PARAMETER_INSERT", "PARAMETER_ORDERING_CHANGE", "PARAMETER_RENAMING",
        "PARAMETER_TYPE_CHANGE", "TOTAL_METHODDECLARATIONSCHANGES",
        "ATTRIBUTE_RENAMING", "ATTRIBUTE_TYPE_CHANGE", "TOTAL_ATTRIBUTEDECLARATIONCHANGES",
        "ADDING_ATTRIBUTE_MODIFIABILITY", "REMOVING_ATTRIBUTE_MODIFIABILITY",
        "REMOVING_CLASS_DERIVABILITY", "REMOVING_METHOD_OVERRIDABILITY",
        "ADDING_CLASS_DERIVABILITY", "ADDING_CLASS_DERIVABILITY", "ADDING_METHOD_OVERRIDABILITY",
        "TOTAL_DECLARATIONPARTCHANGES", "TOTAL_CHANGES", "will_change"
    ]

    windowsize = [2, 3, 4]
    models = [{'key': 'model1', 'value': model1}, {'key': 'model2', 'value': model2},
              {'key': 'model3', 'value': model3}]
    for dataset in datasets:
        for ws in windowsize:
            for rs in resamples:
                for model in models:
                    all_releases_df = pd.read_csv(
                        '../6.join_metrics/results/' + dataset + '-all-releases.csv')
                    all_releases_df.columns = main_columns
                    all_releases_df = all_releases_df.fillna(0)

                    X, y = generateStandardTimeSeriesStructure(all_releases_df, ws, model.get('value'))

                    print("Declaring a dictionary to save results...")
                    results_dict = dict()
                    print("... DONE!")

                    print("Splitting dataset into train and test sets...")
                    X_train, X_test, y_train, y_test = train_test_split(
                        X, y, test_size=0.30, random_state=42)
                    print("General information:")
                    print("X Train set:",
                          X_train.shape[0], "X Test set:", X_test.shape[0])
                    print("y Train set:",
                          y_train.shape[0], "y Test set:", y_test.shape[0])
                    print("... DONE!")

                    print("Scaling features...")
                    scaler = MinMaxScaler()
                    X_train = scaler.fit_transform(X_train)
                    X_test = scaler.fit_transform(X_test)

                    print("... DONE!")

                    print("Setting stratified k-fold...")
                    k = 10
                    kf = StratifiedKFold(n_splits=k, shuffle=True)
                    print("k =", k)
                    print("... DONE!\n")
                    y_test = pd.DataFrame(y_test)
                    y_train = pd.DataFrame(y_train)
                    if rs == 'RUS':
                        X_train, y_train = RandomUnderSampler(random_state=42).fit_resample(X_train, y_train.values.ravel())
                    elif rs == 'ENN':
                        X_train, y_train = EditedNearestNeighbours().fit_resample(X_train,
                                                                                              y_train.values.ravel())
                    elif rs == 'TL':
                        X_train, y_train = TomekLinks().fit_resample(X_train, y_train.values.ravel())
                    elif rs == 'ROS':
                        ros = RandomOverSampler(random_state=42)
                        X_train, y_train = ros.fit_resample(X_train, y_train)
                    elif rs == 'SMOTE':
                        sm = SMOTE(random_state=42)
                        X_train, y_train = sm.fit_resample(X_train, y_train)
                    elif rs == 'ADA':
                        ada = ADASYN(random_state=42)
                        X_train, y_train = ada.fit_resample(X_train, y_train)

                    #train models
                    RandomForest_(X_train, y_train, X_test, y_test, dataset, rs, model.get('key'), ws)
                    DecisionTree_(X_train, y_train, X_test, y_test, dataset, rs, model.get('key'), ws)
                    LogisticRegr_(X_train, y_train, X_test, y_test, dataset, rs, model.get('key'), ws)
                    NN_(X_train, y_train, X_test, y_test, dataset, rs, model.get('key'), ws)
                    # AdaBoost_(X_train, y_train, X_test, y_test, dataset, rs, model.get('key'), ws)
