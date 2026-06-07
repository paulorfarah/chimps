import sys

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statistical_analysis

def resampling_results():
    datasets = ['commons-bcel', 'commons-csv', 'commons-io', 'easymock', 'Openfire', 'pdfbox', 'wro4j']
    # algs = ['DT', 'LogisticRegression', 'MLP', 'RandomForest']
    # models = ['model1', 'model2', 'model3']
    res = pd.DataFrame(columns=['resample', 'F1-Score(None)', 'Accuracy', 'Sensitivity', 'ROC AUC score'])
    for dataset in datasets:
        df = pd.read_csv('results/cpmp/' + dataset + '-results-tradicional-no-feature-selection-model1-3.csv')
        df['F1-Score(None)'] = df['F1-Score(None)'].values[0].split(' ', 1)[0].replace('[', '')
        res = pd.concat([res, df[['resample', 'F1-Score(None)', 'Accuracy', 'Sensitivity', 'ROC AUC score']]])
    res.columns = ['resample', 'F1-Score', 'Accuracy', 'Sensitivity', 'AUC']
    res.sort_values(by=['resample'])
    res.to_csv('results/resampling.csv', index=False)

def best_resampling_results():
    df = pd.read_csv('results/cpmp/best_auc.csv')

def best_scores():
    datasets = ['commons-bcel', 'commons-csv', 'commons-io', 'easymock', 'pdfbox', 'wro4j', 'Openfire']
    # datasets = ['wro4j']

    algs = ['DT', 'LogisticRegression', 'MLP', 'RandomForest']
    # algs = ['LogisticRegression']
    models = ['model1', 'model2', 'model3']
    # models = ['model1']
    scores_trad = pd.DataFrame(columns=['Proj', 'Fs', 'App', 'F1', 'Acc', 'Sen', 'AUC', 'RS', 'F1', 'Acc', 'Sen', 'AUC', 'RS'
        , 'F1', 'Acc', 'Sen', 'AUC', 'RS', 'F1', 'Acc', 'Sen', 'AUC', 'RS'])
    for dataset in datasets:
        df = pd.read_csv('../8.traditional_ml/results/cpmp/' + dataset + '-results-traditional-no-feature-selection-model1-3.csv')
        df = df.replace('LogistRegression', 'LogisticRegression')
        for model in models:
            row_res = [dataset, model, 'trad']
            for alg in algs:
                # try:
                id = df[(df['Algoritm'] == alg) & (df['model'] == model)]['ROC AUC score'].idxmax()
                row = df.iloc[[id]]
                f1 = row['F1-Score(None)'].values[0].split(' ', 1)[0].replace('[', '')
                acc = row['Accuracy'].values[0]
                sen = row['Sensitivity'].values[0]
                auc = row['ROC AUC score'].values[0]
                res = row['resample'].values[0]
                row_res += [f1, acc, sen, auc, res]
                # except:
                #     print('ERROR: ' + str(sys.exc_info()))
                #     row_res += [0, 0, 0, 0, 0]
            scores_trad.loc[len(scores_trad)] = row_res
    # print(res.head())
    # scores_trad.to_csv('results/cpmp/best_auc.csv', index=False)

    scores_slw = pd.DataFrame(columns=['Proj', 'Fs', 'App', 'F1', 'Acc', 'Sen', 'AUC', 'RS', 'F1', 'Acc', 'Sen', 'AUC', 'RS'
        , 'F1', 'Acc', 'Sen', 'AUC', 'RS', 'F1', 'Acc', 'Sen', 'AUC', 'RS'])
    for dataset in datasets:
        df = pd.read_csv('results/cpmp/' + dataset + '-hist-model1-3.csv')
        df = df.replace('LogistRegression', 'LogisticRegression')
        for model in models:
            row_res = [dataset, model, 'slw']
            for alg in algs:
                # try:
                print(dataset)
                print(alg)
                print(model)
                if alg == 'LogisticRegression' and model == 'model1':
                    print('aqui')

                id = df[(df['Algoritm'] == alg) & (df['model'] == model)]['ROC AUC score'].idxmax()
                row = df.iloc[[id]]
                f1 = row['F1-Score(None)'].values[0].split(' ', 1)[0].replace('[', '')
                acc = row['Accuracy'].values[0]
                sen = row['Sensitivity'].values[0]
                auc = row['ROC AUC score'].values[0]
                res = row['resample'].values[0]
                row_res += [f1, acc, sen, auc, res]
                # except:
                #     print('ERROR: ' + str(sys.exc_info()))
                #     row_res += [0, 0, 0, 0, 0]
            scores_slw.loc[len(scores_slw)] = row_res
    # print(res.head())
    scores_slw.to_csv('results/cpmp/best_auc_slw.csv', index=False)

    scores = pd.concat([scores_trad, scores_slw])

    scores = scores.sort_values(['Proj', 'Fs', 'App'], ascending=[True, True, False])
    scores.to_csv('results/cpmp/best_auc_trad_slw.csv', index=False)


def best_scores_pic():
    datasets = ['commons-bcel', 'commons-csv', 'easymock', 'jgit', 'Openfire']
    # datasets = ['wro4j']

    algs = ['DT', 'LogisticRegression', 'MLP', 'RandomForest']
    # algs = ['LogisticRegression']
    models = ['model1', 'model2', 'model3']
    # models = ['model1']
    scores_trad = pd.DataFrame(columns=['Proj', 'Fs', 'App', 'F1', 'Acc', 'Sen', 'AUC', 'RS', 'F1', 'Acc', 'Sen', 'AUC', 'RS'
        , 'F1', 'Acc', 'Sen', 'AUC', 'RS', 'F1', 'Acc', 'Sen', 'AUC', 'RS'])
    for dataset in datasets:
        df = pd.read_csv('../8.traditional_ml/results/perf/' + dataset + '-results-traditional-no-feature-selection-model1-3-perf.csv')
        df = df.replace('LogistRegression', 'LogisticRegression')
        for model in models:
            row_res = [dataset, model, 'trad']
            for alg in algs:
                id = df[(df['Algoritm'] == alg) & (df['model'] == model)]['ROC AUC score'].idxmax()
                row = df.iloc[[id]]
                f1 = row['F1-Score(None)'].values[0].split(' ', 1)[0].replace('[', '')
                acc = row['Accuracy'].values[0]
                sen = row['Sensitivity'].values[0]
                auc = row['ROC AUC score'].values[0]
                res = row['resample'].values[0]
                row_res += [f1, acc, sen, auc, res]

            scores_trad.loc[len(scores_trad)] = row_res

    scores_slw = pd.DataFrame(columns=['Proj', 'Fs', 'App', 'F1', 'Acc', 'Sen', 'AUC', 'RS', 'F1', 'Acc', 'Sen', 'AUC', 'RS'
        , 'F1', 'Acc', 'Sen', 'AUC', 'RS', 'F1', 'Acc', 'Sen', 'AUC', 'RS'])
    for dataset in datasets:
        df = pd.read_csv('results/perf/' + dataset + '-hist-model1-3-perf.csv')
        df = df.replace('LogistRegression', 'LogisticRegression')
        for model in models:
            row_res = [dataset, model, 'slw']
            for alg in algs:
                # try:
                print(dataset)
                print(alg)
                print(model)
                if alg == 'LogisticRegression' and model == 'model1':
                    print('aqui')

                id = df[(df['Algoritm'] == alg) & (df['model'] == model)]['ROC AUC score'].idxmax()
                row = df.iloc[[id]]
                f1 = row['F1-Score(None)'].values[0].split(' ', 1)[0].replace('[', '')
                acc = row['Accuracy'].values[0]
                sen = row['Sensitivity'].values[0]
                auc = row['ROC AUC score'].values[0]
                res = row['resample'].values[0]
                row_res += [f1, acc, sen, auc, res]
                # except:
                #     print('ERROR: ' + str(sys.exc_info()))
                #     row_res += [0, 0, 0, 0, 0]
            scores_slw.loc[len(scores_slw)] = row_res
    # print(res.head())
    scores_slw.to_csv('results/perf/best_auc_slw-perf.csv', index=False)

    scores = pd.concat([scores_trad, scores_slw])

    scores = scores.sort_values(['Proj', 'Fs', 'App'], ascending=[True, True, False])
    scores.to_csv('results/perf/best_auc_trad_slw-perf.csv', index=False)

def plot_boxplot_best_auc():
    df = pd.read_csv('results/cpmp/best_auc.csv')
    fig, ax = plt.subplots()
    df2 = df.iloc[:, [2, 7, 12, 17]]
    df2.columns = ['DT', 'LR', 'MLP', 'RF']
    df_melted = pd.melt(df2)
    # print(df_melted.head())
    # df2 = df.iloc[:, [1, 3, 4]]

    sns.boxplot(x='variable', y='value', data=df_melted)
    box = sns.boxplot(x='variable', y='value', data=df_melted, ax=ax).set(xlabel='ML Algorithm', ylabel='F1-Score')
    # fig = box.get_figure()
    plt.savefig('results/charts/f1-boxplot.png')
    plt.close()

    fig, ax = plt.subplots()
    df2 = df.iloc[:, [3, 8, 13, 18]]
    df2.columns = ['DT', 'LR', 'MLP', 'RF']
    df_melted = pd.melt(df2)
    # print(df_melted.head())
    # df2 = df.iloc[:, [1, 3, 4]]

    sns.boxplot(x='variable', y='value', data=df_melted)
    box = sns.boxplot(x='variable', y='value', data=df_melted, ax=ax).set(xlabel='ML Algorithm', ylabel='Accuracy')
    # fig = box.get_figure()
    plt.savefig('results/charts/acc-boxplot.png')
    plt.close()

    fig, ax = plt.subplots()
    df2 = df.iloc[:, [5, 10, 15, 20]]
    df2.columns = ['DT', 'LR', 'MLP', 'RF']
    df_melted = pd.melt(df2)

    sns.boxplot(x='variable', y='value', data=df_melted)
    box = sns.boxplot(x='variable', y='value', data=df_melted, ax=ax).set(xlabel='ML Algorithm', ylabel='ROC AUC')
    plt.savefig('results/charts/auc-boxplot.png')
    plt.close()


def concatenate_datasets(col1, col2):
    datasets = ['commons-bcel', 'commons-csv', 'commons-io', 'easymock', 'Openfire', 'pdfbox', 'wro4j']
    algs = ['DT', 'LogisticRegression', 'MLP', 'RandomForest']
    models = ['model1', 'model2', 'model3']
    scores = pd.DataFrame(columns=['AP', 'MS', 'F1', 'Acc', 'Sen', 'AUC', 'RS', 'F1', 'Acc', 'Sen', 'AUC', 'RS'
        , 'F1', 'Acc', 'Sen', 'AUC', 'RS', 'F1', 'Acc', 'Sen', 'AUC', 'RS'])

    df_res = pd.DataFrame()
    for dataset in datasets:
        df = pd.read_csv('results/cpmp/' + dataset + '-results-traditional-no-feature-selection-model1-3.csv')
        df_res = pd.concat([df_res, df[[col1, col2]]])
    return df_res


def plot_boxplot_all():
    # cols: Dataset,Algoritm,window,model,resample,F1-Score(micro),F1-Score(macro),F1-Score(weighted),F1-Score(None),
    # Accuracy,Sensitivity,Specificity,ROC AUC score,Confusion matrix
    cols1 = ['Dataset', 'Algoritm', 'model', 'resample']
    cols2 = ['F1-Score(None)', 'Accuracy', 'Sensitivity', 'Specificity', 'ROC AUC score']
    for col1 in cols1:
        for col2 in cols2:
            df = concatenate_datasets(col1, col2)
            # df.loc[df[col1] == 'LogistRegression', df[col1]] = 'LogisticRegression'
            if col1 == 'Algoritm':
                df['Algoritm'] = df['Algoritm'].replace(['LogistRegression'], 'LogisticRegression')
            if col2 == 'F1-Score(None)':
                df['F1-Score(None)'] = df['F1-Score(None)'].str.split(' ').str[0]
                df['F1-Score(None)'] = df['F1-Score(None)'].str.replace('[', '')
                df['F1-Score(None)'] = df['F1-Score(None)'].astype(float)
            print(df.head())
            fig, ax = plt.subplots()
            # sns.boxplot(x='variable', y='value', data=df)
            box = sns.boxplot(x=col1, y=col2, data=df, ax=ax).set(xlabel=col1, ylabel=col2)
            # fig = box.get_figure()
            plt.xticks(rotation=15)
            plt.savefig('results/charts/' + col1 + '-' + col2 + '-boxplot.png')
            plt.close()

def plot_metrics():
    print('todo')

def join_results_perf():
    datasets = ['commons-bcel', 'commons-csv', 'easymock', 'jgit', 'Openfire']
    # datasets = ['wro4j']
    header = ["Dataset", "Algoritm", "Approach", "window", "model", "resample", "F1-Score", "Accuracy", "Sensitivity",
              "Specificity", "ROC AUC score"]
    res = pd.DataFrame()
    for dataset in datasets:
        df = pd.read_csv(
            '../8.traditional_ml/results/perf/' + dataset + '-results-traditional-no-feature-selection-model1-3-perf.csv')
        df['F1-Score'] = df['F1-Score(None)'].values[0].split(' ', 1)[0].replace('[', '')
        df['Approach'] = 'trad'
        dfh = pd.read_csv('results/perf/' + dataset + '-hist-model1-3-perf.csv')
        dfh['F1-Score'] = dfh['F1-Score(None)'].values[0].split(' ', 1)[0].replace('[', '')
        dfh['Approach'] = 'slw'
        res = pd.concat([res, df, dfh])

    # res.sort_values(['Dataset', 'model', 'window'], ascending=[True, True, False])
    res = res.replace('LogistRegression', 'LogisticRegression')
    res = res.replace('model1', 'Str')
    res = res.replace('model2', 'StrEvo')
    res = res.replace('model3', 'Evo')
    file = 'results/perf/all_results_trad_slw-perf.csv'
    res.to_csv(file, columns=header, index=False)
    return file

def join_results():
    projects = ['commons-bcel', 'commons-csv', 'commons-io', 'easymock', 'Openfire', 'pdfbox', 'wro4j']
    # datasets = ['wro4j']
    header = ["Dataset", "Algoritm", "Approach", "window", "model", "resample", "F1-Score", "Accuracy", "Sensitivity",
              "Specificity", "ROC AUC score"]
    res = pd.DataFrame()
    for project in projects:
        df = pd.read_csv(
            '../8.traditional_ml/results/cpmp/' + project + '-results-traditional-no-feature-selection-model1-3.csv')
        df['F1-Score'] = df['F1-Score(None)'].values[0].split(' ', 1)[0].replace('[', '')
        df['Approach'] = 'trad'
        dfh = pd.read_csv('results/cpmp/' + project + '-hist-model1-3.csv')
        dfh['F1-Score'] = dfh['F1-Score(None)'].values[0].split(' ', 1)[0].replace('[', '')
        dfh['Approach'] = 'slw'
        res = pd.concat([res, df, dfh])

    # res.sort_values(['Dataset', 'model', 'window'], ascending=[True, True, False])
    res = res.replace('LogistRegression', 'LogisticRegression')
    res = res.replace('model1', 'Str')
    res = res.replace('model2', 'StrEvo')
    res = res.replace('model3', 'Evo')
    file = 'results/cpmp/all_results_trad_slw.csv'
    res.to_csv(file, columns=header, index=False)
    return file

def best_trad_slw():
    datasets = ['commons-bcel', 'commons-csv', 'commons-io', 'easymock', 'pdfbox', 'wro4j', 'Openfire']
    # datasets = ['wro4j']

    algs = ['DT', 'LogisticRegression', 'MLP', 'RandomForest']
    # algs = ['LogisticRegression']
    models = ['Str', 'StrEvo', 'Evo']

    # models = ['model1']
    scores_trad = pd.DataFrame(
        columns=['Proj', 'Fs', 'App', 'window', 'Algorithm', 'F1', 'Acc', 'Sen', 'AUC', 'RS'])
    for dataset in datasets:
        df = pd.read_csv(
            '../8.traditional_ml/results/cpmp/' + dataset + '-results-traditional-no-feature-selection-model1-3.csv')
        df = df.replace('LogistRegression', 'LogisticRegression')
        df = df.replace('model1', 'Str')
        df = df.replace('model2', 'StrEvo')
        df = df.replace('model3', 'Evo')
        for model in models:
            for alg in algs:
                id = df[(df['Algoritm'] == alg) & (df['model'] == model)]['ROC AUC score'].idxmax()
                row = df.iloc[[id]]
                window = row['window'].values[0]
                f1 = row['F1-Score(None)'].values[0].split(' ', 1)[0].replace('[', '')
                acc = row['Accuracy'].values[0]
                sen = row['Sensitivity'].values[0]
                auc = row['ROC AUC score'].values[0]
                res = row['resample'].values[0]
                row_res = [dataset, model, 'trad', window, alg, f1, acc, sen, auc, res]
                scores_trad.loc[len(scores_trad)] = row_res
    scores_trad.to_csv('results/cpmp/best_auc_trad-win.csv', index=False)

    scores_slw = pd.DataFrame(
        columns=['Proj', 'Fs', 'App', 'window', 'Algorithm', 'F1', 'Acc', 'Sen', 'AUC', 'RS' ])
    for dataset in datasets:
        df = pd.read_csv('results/cpmp/' + dataset + '-hist-model1-3.csv')
        df = df.replace('LogistRegression', 'LogisticRegression')
        df = df.replace('model1', 'Str')
        df = df.replace('model2', 'StrEvo')
        df = df.replace('model3', 'Evo')
        for win in range(2, 5):
            for model in models:
                for alg in algs:
                    id = df[(df['Algoritm'] == alg) & (df['model'] == model) & (df['window'] == win)]['ROC AUC score'].idxmax()
                    row = df.iloc[[id]]
                    window = row['window'].values[0]
                    f1 = row['F1-Score(None)'].values[0].split(' ', 1)[0].replace('[', '')
                    acc = row['Accuracy'].values[0]
                    sen = row['Sensitivity'].values[0]
                    auc = row['ROC AUC score'].values[0]
                    res = row['resample'].values[0]
                    row_res = [dataset, model, 'slw', window, alg, f1, acc, sen, auc, res]
                    scores_slw.loc[len(scores_slw)] = row_res
    # print(res.head())
    scores_slw.to_csv('results/cpmp/best_auc_slw_win.csv', index=False)

    scores = pd.concat([scores_trad, scores_slw])

    scores = scores.sort_values(['Proj', 'Fs', 'App'], ascending=[True, True, False])
    scores.to_csv('results/cpmp/best_auc_trad_slw_win.csv', index=False)


def best_trad_slw_perf():
    datasets = ['commons-bcel', 'commons-csv', 'easymock', 'jgit', 'Openfire']
    # datasets = ['wro4j']

    algs = ['DT', 'LogisticRegression', 'MLP', 'RandomForest']
    # algs = ['LogisticRegression']
    models = ['Str', 'StrEvo', 'Evo']

    # models = ['model1']
    scores_trad = pd.DataFrame(
        columns=['Proj', 'Fs', 'App', 'window', 'Algorithm', 'F1', 'Acc', 'Sen', 'AUC', 'RS'])
    for dataset in datasets:
        df = pd.read_csv(
            '../8.traditional_ml/results/perf/' + dataset + '-results-traditional-no-feature-selection-model1-3-perf.csv')
        df = df.replace('LogistRegression', 'LogisticRegression')
        df = df.replace('model1', 'Str')
        df = df.replace('model2', 'StrEvo')
        df = df.replace('model3', 'Evo')
        for model in models:
            for alg in algs:
                id = df[(df['Algoritm'] == alg) & (df['model'] == model)]['ROC AUC score'].idxmax()
                row = df.iloc[[id]]
                window = row['window'].values[0]
                f1 = row['F1-Score(None)'].values[0].split(' ', 1)[0].replace('[', '')
                acc = row['Accuracy'].values[0]
                sen = row['Sensitivity'].values[0]
                auc = row['ROC AUC score'].values[0]
                res = row['resample'].values[0]
                row_res = [dataset, model, 'trad', window, alg, f1, acc, sen, auc, res]
                scores_trad.loc[len(scores_trad)] = row_res
    scores_trad.to_csv('results/perf/best_auc_trad-win-perf.csv', index=False)

    scores_slw = pd.DataFrame(
        columns=['Proj', 'Fs', 'App', 'window', 'Algorithm', 'F1', 'Acc', 'Sen', 'AUC', 'RS' ])
    for dataset in datasets:
        df = pd.read_csv('results/perf/' + dataset + '-hist-model1-3-perf.csv')
        df = df.replace('LogistRegression', 'LogisticRegression')
        df = df.replace('model1', 'Str')
        df = df.replace('model2', 'StrEvo')
        df = df.replace('model3', 'Evo')
        for win in range(2, 5):
            for model in models:
                for alg in algs:
                    id = df[(df['Algoritm'] == alg) & (df['model'] == model) & (df['window'] == win)]['ROC AUC score'].idxmax()
                    row = df.iloc[[id]]
                    window = row['window'].values[0]
                    f1 = row['F1-Score(None)'].values[0].split(' ', 1)[0].replace('[', '')
                    acc = row['Accuracy'].values[0]
                    sen = row['Sensitivity'].values[0]
                    auc = row['ROC AUC score'].values[0]
                    res = row['resample'].values[0]
                    row_res = [dataset, model, 'slw', window, alg, f1, acc, sen, auc, res]
                    scores_slw.loc[len(scores_slw)] = row_res
    # print(res.head())
    scores_slw.to_csv('results/perf/best_auc_slw_win-perf.csv', index=False)

    scores = pd.concat([scores_trad, scores_slw])

    scores = scores.sort_values(['Proj', 'Fs', 'App'], ascending=[True, True, False])
    scores.to_csv('results/perf/best_auc_trad_slw_win-perf.csv', index=False)

if __name__ == '__main__':
    # join_results()
    # best_scores()
    # best_scores_pic()
    # best_trad_slw()
    best_trad_slw_perf()
    # plot_boxplot_best_auc()
    # plot_boxplot_all()
    # resampling_results()
