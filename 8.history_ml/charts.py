import pandas as pd
from matplotlib import pyplot as plt

pd.set_option('display.max_columns', None)

metrics = ['F1', 'Acc', 'Sen', 'ROC']
df = pd.read_csv('results/perf/best_auc_trad_slw_win-perf.csv', decimal=",")
print(df.columns)

df['F1'] = pd.to_numeric(df['F1'], errors='raise')
df['Acc'] = pd.to_numeric(df['Acc'], errors='raise')
df['Sen'] = pd.to_numeric(df['Sen'], errors='raise')
df['ROC'] = pd.to_numeric(df['AUC'], errors='raise')
# df.query("window == 0 | window == 3", inplace=True)

for metric in metrics:

    # df.columns = ['Dataset', 'Algoritm', 'window', 'model', 'resample', 'F1-Score(micro)',
    #    'F1-Score(macro)', 'F1-Score', 'F1-Score(None)', 'Accuracy',
    #    'Sensitivity', 'Specificity', 'ROC AUC score', 'Confusion matrix']
    # df.columns = ['Proj', 'Fs', 'App', 'F1', 'Acc', 'Sen', 'AUC', 'RS', 'F1' ,'Acc', 'Sen' , 'AUC',
    #               'RS', 'F1', 'Acc', 'Sen', 'AUC', 'RS', 'F1', 'Acc', 'Sen', 'AUC', 'RS']
    print('######### ' + metric)

    # approach

    # all feature sets
    # dfApp = df.query("Fs == 'Str'")
    # dfApp['window'] = dfApp['window'].replace({0: 'trad', 3: 'our'})
    # dfAvg = dfApp.groupby(['Dataset', 'window'])[metric].mean()

    ax = pd.pivot_table(df, index='Proj', columns='App', values=metric).plot.bar(alpha=0.75, rot=0)
    # ax = pd.pivot_table(dfApp, index='Dataset', columns='window')[metric].plot.bar(alpha=0.75, rot=0)

    # for p in ax.patches:
    #     ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    ax.set_ylabel(metric)
    ax.set_xlabel('')
    plt.legend(title='Method', loc='lower right')
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.2)
    plt.savefig('results/charts/window-all-' + metric + '-perf.pdf')
    # plt.show()

    # Str
    dfApp = df.query("Fs == 'Str'")
    # dfApp['window'] = dfApp['window'].replace({0: 'trad', 3: 'our'})
    # dfAvg = dfApp.groupby(['Dataset', 'window'])[metric].mean()

    ax = pd.pivot_table(dfApp, index='Proj', columns='App', values=metric).plot.bar(alpha=0.75, rot=0)
    # ax = pd.pivot_table(dfApp, index='Dataset', columns='window')[metric].plot.bar(alpha=0.75, rot=0)

    # for p in ax.patches:
    #     ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    ax.set_ylabel(metric)
    ax.set_xlabel('')
    plt.legend(title='Approach', loc='lower right')
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.2)
    plt.savefig('results/charts/window-Str-' + metric + '-perf.pdf')
    # plt.show()

    # -- set 2
    dfApp = df.query("Fs == 'StrEvo'")
    # dfApp['window'] = dfApp['window'].replace({0: 'trad', 3: 'our'})
    # dfAvg = dfApp.groupby(['Dataset', 'window'])[metric].mean()
    # print(dfAvg)
    dfApp['F1'] = pd.to_numeric(dfApp['F1'], errors='raise')
    dfApp['Acc'] = pd.to_numeric(dfApp['Acc'], errors='raise')
    dfApp['Sen'] = pd.to_numeric(dfApp['Sen'], errors='raise')
    dfApp['AUC'] = pd.to_numeric(dfApp['AUC'], errors='raise')

    ax = pd.pivot_table(dfApp, index='Proj', columns='App', values=metric).plot.bar(alpha=0.75, rot=0)
    # for p in ax.patches:
    #     ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    ax.set_ylabel(metric)
    ax.set_xlabel('')
    plt.legend(title='Approach', loc='lower right')
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.2)
    plt.savefig('results/charts/window-StrEvo-' + metric + '-perf.pdf')

    # dfApp['App'] = df['App'].replace({0: 'trad', 3: 'our'})
    # dfAvg = dfApp.groupby(['Dataset', 'window'])[metric].mean()
    # print(dfAvg)

    ax = pd.pivot_table(dfApp, index='Proj', columns='App', values=metric).plot.bar(alpha=0.75, rot=0)
    # for p in ax.patches:
    #     ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    ax.set_ylabel(metric)
    ax.set_xlabel('')
    plt.legend(title='Approach', loc='lower right')
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.2)
    plt.savefig('results/charts/window-sets1_2_6_7' + metric + '-perf.pdf')

    # feature sets
    dfSet = df.query("App == 'slw'")
    print(dfSet.dtypes)
    dfSet['F1'] = pd.to_numeric(dfSet['F1'], errors='raise')
    dfSet['Acc'] = pd.to_numeric(dfSet['Acc'], errors='raise')
    dfSet['Sen'] = pd.to_numeric(dfSet['Sen'], errors='raise')
    dfSet['AUC'] = pd.to_numeric(dfSet['AUC'], errors='raise')
    # dfSet['Fs'] = dfSet['Fs'].replace({'model1': 'set1', 'model2': 'set2','model3': 'set3','model4': 'set4','model6': 'set5','model7': 'set6'})
    dfAvg = dfSet.groupby(['Proj', 'Fs'])[metric].mean()
    # print(dfAvg)

    ax = pd.pivot_table(dfSet, index='Proj', columns='Fs', values=metric).plot.bar(alpha=0.75, rot=0)
    # for p in ax.patches:
    #     ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    ax.set_ylabel(metric)
    ax.set_xlabel('')
    plt.legend(loc='lower right')
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.2)
    plt.savefig('results/charts/sets' + metric + '-perf.pdf')

    # algorithms
    dfAlg = df.query("App == 'slw'")
    dfAlg = dfAlg.query("Fs == 'Str'")
    # dfSet['window'] = dfSet['window'].replace({0: 'trad', 3: 'our'})
    dfAvg = dfAlg.groupby(['Proj', 'Algorithm'])[metric].mean()
    # print(dfAvg)

    ax = pd.pivot_table(dfAlg, index='Proj', columns='Algorithm', values=metric).plot.bar(alpha=0.75, rot=0)
    # for p in ax.patches:
    #     ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    ax.set_ylabel(metric)
    ax.set_xlabel('')
    plt.legend(loc='lower right')
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.2)
    plt.savefig('results/charts/algs-Str' + metric + '-perf.pdf')

    dfAlg = df.query("App == 'slw'")
    dfAlg = dfAlg.query("Fs == 'StrEvo'")
    # dfSet['window'] = dfSet['window'].replace({0: 'trad', 3: 'our'})
    dfAvg = dfAlg.groupby(['Proj', 'Algorithm'])[metric].mean()
    # print(dfAvg)

    ax = pd.pivot_table(dfAlg, index='Proj', columns='Algorithm', values=metric).plot.bar(alpha=0.75, rot=0)
    # for p in ax.patches:
    #     ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    ax.set_ylabel(metric)
    ax.set_xlabel('')
    plt.legend(loc='lower right')
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.2)
    plt.savefig('results/charts/algs-StrEvo' + metric + '-perf.pdf')

    dfAlg = df.query("App == 'slw'")
    dfAlg = dfAlg.query("Fs == 'Evo'")
    # dfSet['window'] = dfSet['window'].replace({0: 'trad', 3: 'our'})
    dfAvg = dfAlg.groupby(['Proj', 'Algorithm'])[metric].mean()
    # print(dfAvg)

    ax = pd.pivot_table(dfAlg, index='Proj', columns='Algorithm', values=metric).plot.bar(alpha=0.75, rot=0)
    # for p in ax.patches:
    #     ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    ax.set_ylabel(metric)
    ax.set_xlabel('')
    plt.legend(loc='lower right')
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.2)
    plt.savefig('results/charts/algs-Evo' + metric + '-perf.pdf')

    dfAlg = df.query("App == 'slw'")
    dfAvg = dfAlg.groupby(['Proj', 'Algorithm'])[metric].mean()
    # print(dfAvg)

    ax = pd.pivot_table(dfAlg, index='Proj', columns='Algorithm', values=metric).plot.bar(alpha=0.75, rot=0)
    # for p in ax.patches:
    #     ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    ax.set_ylabel(metric)
    ax.set_xlabel('')
    plt.legend(loc='lower right')
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.2)
    plt.savefig('results/charts/algs-all' + metric + '-perf.pdf')

    plt.show()
