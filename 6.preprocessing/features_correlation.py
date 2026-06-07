import sys

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from numpy import percentile

pd.set_option('display.max_columns', None)


def ck_ownduration_correlation(project_name, file, ck_file, ttype, output):
    print(project_name + ' ck')

    # read trace own duration metric
    df_pd = pd.read_csv(file, sep=',')
    df_pd['project_name'] = project_name
    if ttype == 'diff' or ttype == 'avg':
        df = pd.DataFrame().assign(project_name=df_pd['project_name'], commit_hash=df_pd['commit_hash'],
                                   class_name=df_pd['class_name'], own_duration=df_pd['mean_val'])
        df = df.merge(df_pd[['project_name', 'commit_hash', 'class_name', 'mean_val']].rename(
            columns={'mean_val': 'own_duration'}), how='outer')
    elif ttype == 'median':
        df = pd.DataFrame().assign(project_name=df_pd['project_name'], commit_hash=df_pd['commit_hash'],
                                   class_name=df_pd['class_name'], own_duration=df_pd['mean_val'], perf_changed=df_pd['changed_median'])
        df = df.merge(df_pd[['project_name', 'commit_hash', 'class_name', 'mean_val']].rename(
            columns={'mean_val': 'own_duration'}), how='outer')
        df = df.loc[df['perf_changed'] == 1]


    #read static ck metrics

    ck_metrics_class_and_methods = ['index', 'file', 'class', 'type', 'cbo_x', 'cboModified_x', 'fanin_x', 'fanout_x', 'wmc_x', 'dit',
                  'noc', 'rfc_x', 'lcom', 'lcom*', 'tcc', 'lcc', 'totalMethodsQty', 'staticMethodsQty',
                  'publicMethodsQty', 'privateMethodsQty', 'protectedMethodsQty', 'defaultMethodsQty',
                  'visibleMethodsQty', 'abstractMethodsQty', 'finalMethodsQty', 'synchronizedMethodsQty',
                  'totalFieldsQty', 'staticFieldsQty', 'publicFieldsQty', 'privateFieldsQty', 'protectedFieldsQty',
                  'defaultFieldsQty', 'finalFieldsQty', 'synchronizedFieldsQty', 'nosi', 'loc_x', 'returnQty',
                  'loopQty_x', 'comparisonsQty_x', 'tryCatchQty_x', 'parenthesizedExpsQty_x', 'stringLiteralsQty_x',
                  'numbersQty_x', 'assignmentsQty_x', 'mathOperationsQty_x', 'variablesQty_x', 'maxNestedBlocksQty_x',
                  'anonymousClassesQty_x', 'innerClassesQty_x', 'lambdasQty_x', 'uniqueWordsQty_x', 'modifiers_x',
                  'logStatementsQty_x', 'method', 'constructor', 'line', 'cbo_y', 'cboModified_y', 'fanin_y',
                  'fanout_y', 'wmc_y', 'rfc_y', 'loc_y', 'returnsQty', 'variablesQty_y', 'parametersQty',
                  'methodsInvokedQty', 'methodsInvokedLocalQty', 'methodsInvokedIndirectLocalQty', 'loopQty_y',
                  'comparisonsQty_y', 'tryCatchQty_y', 'parenthesizedExpsQty_y', 'stringLiteralsQty_y', 'numbersQty_y',
                  'assignmentsQty_y', 'mathOperationsQty_y', 'maxNestedBlocksQty_y', 'anonymousClassesQty_y',
                  'innerClassesQty_y', 'lambdasQty_y', 'uniqueWordsQty_y', 'modifiers_y', 'logStatementsQty_y',
                  'hasJavaDoc', 'commit_hash', 'project_name']
    # ck_metrics_class = ['file', 'class', 'type', 'cbo', 'cboModified', 'fanin', 'fanout', 'wmc', 'dit', 'noc', 'rfc',
    #                     'lcom', 'lcom*', 'tcc', 'lcc', 'totalMethodsQty', 'staticMethodsQty', 'publicMethodsQty',
    #                     'privateMethodsQty', 'protectedMethodsQty', 'defaultMethodsQty', 'visibleMethodsQty',
    #                     'abstractMethodsQty', 'finalMethodsQty', 'synchronizedMethodsQty', 'totalFieldsQty',
    #                     'staticFieldsQty', 'publicFieldsQty', 'privateFieldsQty', 'protectedFieldsQty',
    #                     'defaultFieldsQty', 'finalFieldsQty', 'synchronizedFieldsQty', 'nosi', 'loc', 'returnQty',
    #                     'loopQty', 'comparisonsQty', 'tryCatchQty', 'parenthesizedExpsQty', 'stringLiteralsQty',
    #                     'numbersQty', 'assignmentsQty', 'mathOperationsQty', 'variablesQty', 'maxNestedBlocksQty',
    #                     'anonymousClassesQty', 'innerClassesQty', 'lambdasQty', 'uniqueWordsQty', 'modifiers',
    #                     'logStatementsQty', 'commit_hash', 'project_name']


    df_ck = pd.read_csv(ck_file, usecols=ck_metrics_class_and_methods, sep=',',
                        index_col=False)

    df_ck = df_ck[df_ck['project_name'] == project_name]
    if project_name == 'jgit':
        path1 = '/mnt/sda4/software-metrics/static_metrics/' + project_name + '/'
    else:
        path1 = '/groups/ilabt-imec-be/software-performance/ck/' + project_name + '/'
    df_ck['file'] = df_ck['file'].str.replace(path1, '')
    #try:
    #    spl_word = "commons-"
    #    file_str = df_ck[df_ck['file'].str.contains(spl_word)].iloc[0]
    #    res = file_str['file'].split(spl_word, 1)
    #    splitString = res[0]
    #    df_ck['file'] = df_ck.file.str.replace(splitString, '')
    #except:
    #    pass

    df = pd.merge(left=df, right=df_ck, left_on=['project_name', 'commit_hash', 'class_name'],
                  right_on=['project_name', 'commit_hash', 'file'], how='left')

    #plot correlations
    metrics = ['own_duration'] + ck_metrics_class_and_methods[4:52] + ck_metrics_class_and_methods[55:83]
    # metrics = ['own_duration'] + ck_metrics_class[4:51]

    q25, q75 = percentile(df['own_duration'], 25), percentile(df['own_duration'], 75)
    iqr = q75 - q25
    cut_off = iqr * 1.5
    lower, upper = q25 - cut_off, q75 + cut_off
    # identify outliers
    # outliers = [x for x in df['own_duration'] if x < lower or x > upper]
    # print('outliers:')
    # for o in outliers:
    #     print(o)

    # df.loc[(df['Discount'] >= 1000) & (df['Discount'] <= 2000)]
    df_outliers = df.loc[(df['own_duration'] >= lower) & (df['own_duration'] <= upper)]
    # for m in metrics:
    #     if m != 'own_duration':
    #         sns.lmplot(x="own_duration", y=m, data=df_outliers)
    #         plt.savefig('results/correlation/ck/' + project_name + '/' + project_name + '_' + m.replace('*', '_') + '_' + trace_type + '.pdf')
    # plt.show()

    # df_outliers['own_duration'].to_csv('results/own_dur.csv', index=False)
    # df_outliers['synchronizedMethodsQty'].to_csv('results/synchro.csv', index=False)
    # df_outliers[['own_duration', 'synchronizedMethodsQty']].corr().to_csv('results/corr.csv')


    df[metrics].corr().to_csv(output, index=False)
    df_outliers[metrics].corr().to_csv(output.replace('.csv', '_outliers.csv'), index=False)
    return df[metrics].corr()


def und_ownduration_correlation(project_name, file, ttype, output):
    print(project_name + ' und')
    # df_pd = pd.read_csv('../dynamic_metrics/results/' + project_name + '-performance-diff.csv', sep=',')
    df_pd = pd.read_csv(file, sep=',')
    df_pd['project_name'] = project_name

    # if ttype == 'diff' or ttype == 'avg':
    #     df = pd.DataFrame().assign(project_name=df_pd['project_name'], commit_hash=df_pd['commit_hash'],
    #                                class_name=df_pd['class_name'], own_duration=df_pd['mean_val'])
    #     df = df.merge(df_pd[['project_name', 'commit_hash', 'class_name', 'mean_val']], how='outer')
    # elif ttype == 'median':
    #     df = pd.DataFrame().assign(project_name=df_pd['project_name'], commit_hash=df_pd['commit_hash'],
    #                                class_name=df_pd['class_name'], own_duration=df_pd['median_val'], perf_changed=df_pd['perf_changed'])
    #     df = df.merge(df_pd[['project_name', 'commit_hash', 'class_name', 'median_val']].rename(
    #         columns={'median_val': 'own_duration'}), how='outer')
    #     df = df.loc[df['perf_changed'] == 1]


    if ttype == 'diff' or ttype == 'avg':
        df = pd.DataFrame().assign(project_name=df_pd['project_name'], commit_hash=df_pd['commit_hash'],
                                   class_name=df_pd['class_name'], own_duration=df_pd['mean_val'])
        df = df.merge(df_pd[['project_name', 'commit_hash', 'class_name', 'mean_val']].rename(
            columns={'mean_val': 'own_duration'}), how='outer')
    elif ttype == 'median':
        df = pd.DataFrame().assign(project_name=df_pd['project_name'], commit_hash=df_pd['commit_hash'],
                                   class_name=df_pd['class_name'], own_duration=df_pd['mean_val'], perf_changed=df_pd['changed_median'])
        df = df.merge(df_pd[['project_name', 'commit_hash', 'class_name', 'mean_val']].rename(
            columns={'mean_val': 'own_duration'}), how='outer')
        df = df.loc[df['perf_changed'] == 1]



    # df = pd.DataFrame().assign(project_name=df_pd['project_name'], commit_hash=df_pd['commit'],
    #                            class_name=df_pd['class_name'], own_duration=df_pd['avg1'])
    # df = df.merge(df_pd[['project_name', 'prevcommit', 'class_name', 'avg2']].rename(
    #     columns={'prevcommit': 'commit_hash', 'avg2': 'own_duration'}), how='outer')

    # understand
    und_metrics = []
    if project_name == 'jgit':
        und_metrics += ["Name", "File"]
    else:
        und_metrics += ["index1", "index2", "index3", "index4", "index5", "index6", "index7", "Kind", "Name", "File"]
    und_metrics += ["AvgCyclomatic", "AvgCyclomaticModified", "AvgCyclomaticStrict",
                   "AvgEssential", "AvgLine", "AvgLineBlank", "AvgLineCode", "AvgLineComment", "CountClassBase",
                   "CountClassCoupled", "CountClassDerived", "CountDeclClass", "CountDeclClassMethod",
                   "CountDeclClassVariable", "CountDeclFile", "CountDeclFunction", "CountDeclInstanceMethod",
                   "CountDeclInstanceVariable", "CountDeclMethod", "CountDeclMethodAll",
                   "CountDeclMethodDefault", "CountDeclMethodPrivate", "CountDeclMethodProtected",
                   "CountDeclMethodPublic", "CountInput", "CountLine", "CountLineBlank", "CountLineCode",
                   "CountLineCodeDecl", "CountLineCodeExe", "CountLineComment", "CountOutput", "CountPath",
                   "CountSemicolon", "CountStmt", "CountStmtDecl", "CountStmtExe", "Cyclomatic",
                   "CyclomaticModified", "CyclomaticStrict", "Essential", "MaxCyclomatic",
                   "MaxCyclomaticModified", "MaxCyclomaticStrict", "MaxEssential", "MaxInheritanceTree",
                   "MaxNesting", "PercentLackOfCohesion", "RatioCommentToCode", "SumCyclomatic",
                   "SumCyclomaticModified", "SumCyclomaticStrict", "SumEssential", 'unknown', 'commit_hash',
                   'project_name']
    df_und = pd.read_csv('../static_metrics/results/und/' + project_name + '-und_2.csv', sep=',',
                         engine='python', names=und_metrics)

    df_und = df_und.loc[df_und['project_name'] == project_name]

    df['file'] = df['class_name'].str.replace('src/', '')

    # if project_name == 'jgit':
    #     path1 = '/mnt/sda4/software-metrics/static_metrics/' + project_name + '/'
    # else:
    #     path1 = '/groups/ilabt-imec-be/software-performance/ck/' + project_name + '/'

    if project_name != 'jgit':
        df_und = df_und[df_und.columns[8:]]
    df_und['class'] = df_und['Name']

    # 'core/src/main/java/org/easymock/Capture.java'
    # 'core/src/main/java/org/easymock/Capture.java'


    df = pd.merge(left=df, right=df_und, left_on=['project_name', 'commit_hash', 'file'],
                  right_on=['project_name', 'commit_hash', 'File'], how='left')

    #plot correlations
    if project_name == 'jgit':
        metrics = ['own_duration'] + und_metrics[7:56]
    else:
        metrics = ['own_duration'] + und_metrics[10:64]


    q25, q75 = percentile(df['own_duration'], 25), percentile(df['own_duration'], 75)
    iqr = q75 - q25
    cut_off = iqr * 1.5
    lower, upper = q25 - cut_off, q75 + cut_off

    # identify outliers
    # outliers = [x for x in df['own_duration'] if x < lower or x > upper]
    # print('outliers:')
    # for o in outliers:
    #     print(o)

    # df.loc[(df['Discount'] >= 1000) & (df['Discount'] <= 2000)]
    df_outliers = df.loc[(df['own_duration'] >= lower) & (df['own_duration'] <= upper)]
    # print(df_outliers.dtypes)
    # for m in metrics:
    #     # print(m)
    #     # print(df_outliers[m])
    #     df_outliers[m] = df_outliers[m].fillna(0)
    #     df_outliers[m] = pd.to_numeric(df_outliers[m])
    #     sns.lmplot(x="own_duration", y=m, data=df_outliers)
    #     plt.savefig('results/correlation/und/' + project_name + '/' + project_name + '_' + m + '-outliers.pdf')
    # # plt.show()

    df_outliers['own_duration'].fillna(0).to_csv('results/own_dur.csv', index=False)
    df_outliers['AvgCyclomatic'].fillna(0).to_csv('results/AvgCyclomatic.csv', index=False)
    df_outliers[['own_duration', 'AvgCyclomatic']].fillna(0).corr().to_csv('results/corr.csv')


    df[metrics].fillna(0).corr().to_csv(output, index=False)
    df_outliers[metrics].fillna(0).corr().to_csv(output.replace('.csv', '_outliers.csv'), index=False)


def evo_ownduration_correlation(project_name, file, ttype, output):
    print(project_name + ' evo')
    df_pd = pd.read_csv(file, sep=',')  # ok
    df_pd['project_name'] = project_name
    #
    # df = pd.DataFrame().assign(project_name=df_pd['project_name'], commit_hash=df_pd['commit'],
    #                            class_name=df_pd['class_name'], own_duration=df_pd['avg1'])
    # df = df.merge(df_pd[['project_name', 'prevcommit', 'class_name', 'avg2']].rename(
    #     columns={'prevcommit': 'commit_hash', 'avg2': 'own_duration'}), how='outer')

    # if ttype == 'diff' or ttype == 'avg':
    #     df = pd.DataFrame().assign(project_name=df_pd['project_name'], commit_hash=df_pd['commit_hash'],
    #                                class_name=df_pd['class_name'], own_duration=df_pd['mean_val'])
    #     df = df.merge(df_pd[['project_name', 'commit_hash', 'class_name', 'mean_val']], how='outer')
    # elif ttype == 'median':
    #     df = pd.DataFrame().assign(project_name=df_pd['project_name'], commit_hash=df_pd['commit_hash'],
    #                                class_name=df_pd['class_name'], own_duration=df_pd['median_val'], perf_changed=df_pd['perf_changed'])
    #     df = df.merge(df_pd[['project_name', 'commit_hash', 'class_name', 'median_val']].rename(
    #         columns={'median_val': 'own_duration'}), how='outer')
    #     df = df.loc[df['perf_changed'] == 1]

    if ttype == 'diff' or ttype == 'avg':
        df = pd.DataFrame().assign(project_name=df_pd['project_name'], commit_hash=df_pd['commit_hash'],
                                   class_name=df_pd['class_name'], own_duration=df_pd['mean_val'])
        df = df.merge(df_pd[['project_name', 'commit_hash', 'class_name', 'mean_val']].rename(
            columns={'mean_val': 'own_duration'}), how='outer')
    elif ttype == 'median':
        df = pd.DataFrame().assign(project_name=df_pd['project_name'], commit_hash=df_pd['commit_hash'],
                                   class_name=df_pd['class_name'], own_duration=df_pd['mean_val'], perf_changed=df_pd['changed_median'])
        df = df.merge(df_pd[['project_name', 'commit_hash', 'class_name', 'mean_val']].rename(
            columns={'mean_val': 'own_duration'}), how='outer')
        df = df.loc[df['perf_changed'] == 1]

    # evolutionary metrics
    evo_metrics = ["project", "commit", "commitprevious", "class", "BOM", "TACH", "FCH", "LCH", "CHO", "FRCH",
                   "CHD", "WCD", "WFR", "ATAF", "LCA", "LCD", "CSB", "CSBS", "ACDF"]

    evo_file = '../static_metrics/results/evometrics/evometrics_all.csv'
    path1 = '/home/usuario/OneDrive/ufpr/datasets/software-metrics/projectA/' + project_name + '/'
    if project_name == 'jgit':
        evo_file = '../static_metrics/results/evometrics/jgit-results-processMetrics.csv'
        path1 = '/mnt/sda4/software-metrics/static_metrics/projectA/jgit/'
    df_evo = pd.read_csv(evo_file, usecols=evo_metrics, sep=',', index_col=False)
    df_evo = df_evo.loc[df_evo['project'] == project_name]

    df_evo['file'] = df_evo['class'].str.replace(path1, '')
    df = pd.merge(left=df, right=df_evo, left_on=['project_name', 'commit_hash', 'class_name'],
                  right_on=['project', 'commit', 'file'], how='left')

    #plot correlations
    metrics = ['own_duration'] + evo_metrics[4:19]

    q25, q75 = percentile(df['own_duration'], 25), percentile(df['own_duration'], 75)
    iqr = q75 - q25
    cut_off = iqr * 1.5
    lower, upper = q25 - cut_off, q75 + cut_off
    # identify outliers
    outliers = [x for x in df['own_duration'] if x < lower or x > upper]
    # print('outliers:')
    # for o in outliers:
    #     print(o)

    # df.loc[(df['Discount'] >= 1000) & (df['Discount'] <= 2000)]
    df_outliers = df.loc[(df['own_duration'] >= lower) & (df['own_duration'] <= upper)]
    for m in metrics:
        sns.lmplot(x="own_duration", y=m, data=df_outliers)
        plt.savefig('results/correlation/evo/' + project_name + '/' + project_name + '_' + m + '-outliers.pdf')
    # plt.show()

    df[metrics].corr().to_csv(output, index=False)
    df_outliers[metrics].corr().to_csv(output.replace('.csv', '_outliers.csv'), index=False)

def cd_ownduration_correlation(project_name, file, ttype, output):
    print(project_name + ' cd')
    df_pd = pd.read_csv(file, sep=',')  # ok
    df_pd['project_name'] = project_name
    # df = pd.DataFrame().assign(project_name=df_pd['project_name'], commit_hash=df_pd['commit'],
    #                            class_name=df_pd['class_name'], own_duration=df_pd['avg1'])
    # df = df.merge(df_pd[['project_name', 'prevcommit', 'class_name', 'avg2']].rename(
    #     columns={'prevcommit': 'commit_hash', 'avg2': 'own_duration'}), how='outer')

    # if ttype == 'diff' or ttype == 'avg':
    #     df = pd.DataFrame().assign(project_name=df_pd['project_name'], commit_hash=df_pd['commit_hash'],
    #                                class_name=df_pd['class_name'], own_duration=df_pd['mean_val'])
    #     df = df.merge(df_pd[['project_name', 'commit_hash', 'class_name', 'mean_val']], how='outer')
    # elif ttype == 'median':
    #     df = pd.DataFrame().assign(project_name=df_pd['project_name'], commit_hash=df_pd['commit_hash'],
    #                                class_name=df_pd['class_name'], own_duration=df_pd['median_val'], perf_changed=df_pd['perf_changed'])
    #     df = df.merge(df_pd[['project_name', 'commit_hash', 'class_name', 'median_val']].rename(
    #         columns={'median_val': 'own_duration'}), how='outer')
    #     df = df.loc[df['perf_changed'] == 1]

    if ttype == 'diff' or ttype == 'avg':
        df = pd.DataFrame().assign(project_name=df_pd['project_name'], commit_hash=df_pd['commit_hash'],
                                   class_name=df_pd['class_name'], own_duration=df_pd['mean_val'])
        df = df.merge(df_pd[['project_name', 'commit_hash', 'class_name', 'mean_val']].rename(
            columns={'mean_val': 'own_duration'}), how='outer')
    elif ttype == 'median':
        df = pd.DataFrame().assign(project_name=df_pd['project_name'], commit_hash=df_pd['commit_hash'],
                                   class_name=df_pd['class_name'], own_duration=df_pd['mean_val'], perf_changed=df_pd['changed_median'])
        df = df.merge(df_pd[['project_name', 'commit_hash', 'class_name', 'mean_val']].rename(
            columns={'mean_val': 'own_duration'}), how='outer')
        df = df.loc[df['perf_changed'] == 1]

    changedistiller_metrics = ["PROJECT_NAME", "CURRENT_COMMIT", "PREVIOUS_COMMIT", "CLASS_CURRENTCOMMIT",
                               "CLASS_PREVIOUSCOMMIT",
                               "STATEMENT_DELETE", "STATEMENT_INSERT", "STATEMENT_ORDERING_CHANGE",
                               "STATEMENT_PARENT_CHANGE", "STATEMENT_UPDATE", "TOTAL_STATEMENTLEVELCHANGES",
                               "PARENT_CLASS_CHANGE", "PARENT_CLASS_DELETE", "PARENT_CLASS_INSERT", "CLASS_RENAMING",
                               "TOTAL_CLASSDECLARATIONCHANGES",
                               "RETURN_TYPE_CHANGE", "RETURN_TYPE_DELETE", "RETURN_TYPE_INSERT", "METHOD_RENAMING",
                               "PARAMETER_DELETE", "PARAMETER_INSERT", "PARAMETER_ORDERING_CHANGE",
                               "PARAMETER_RENAMING",
                               "PARAMETER_TYPE_CHANGE", "TOTAL_METHODDECLARATIONSCHANGES",
                               "ATTRIBUTE_RENAMING", "ATTRIBUTE_TYPE_CHANGE", "TOTAL_ATTRIBUTEDECLARATIONCHANGES",
                               "ADDING_ATTRIBUTE_MODIFIABILITY", "REMOVING_ATTRIBUTE_MODIFIABILITY",
                               "REMOVING_CLASS_DERIVABILITY", "REMOVING_METHOD_OVERRIDABILITY",
                               "ADDING_CLASS_DERIVABILITY", "ADDING_CLASS_DERIVABILITY", "ADDING_METHOD_OVERRIDABILITY",
                               "TOTAL_DECLARATIONPARTCHANGES", "TOTAL_CHANGES"]

    cd_file = '../static_metrics/results/changedistiller/changedistiller_all.csv'
    path1 = '/groups/ilabt-imec-be/software-performance/changedistiller/projectB/' + project_name + '/'
    if project_name == 'jgit':
        cd_file = '../static_metrics/results/changedistiller/jgit-changedistiller.csv'
        path1 = '/home/usuario/PycharmProjects/software-metrics/static_metrics/jgit1/'
    df_cd = pd.read_csv(cd_file, sep=',', index_col=False)
    df_cd.columns = changedistiller_metrics
    df_cd = df_cd.loc[df_cd['PROJECT_NAME'] == project_name]

    df_cd['file'] = df_cd['CLASS_PREVIOUSCOMMIT'].str.replace(path1, '')
    df = pd.merge(left=df, right=df_cd, left_on=['project_name', 'commit_hash', 'class_name'],
                  right_on=['PROJECT_NAME', 'PREVIOUS_COMMIT', 'file'], how='left')

    #plot correlations
    metrics = ['own_duration'] + changedistiller_metrics[9:41]

    q25, q75 = percentile(df['own_duration'], 25), percentile(df['own_duration'], 75)
    iqr = q75 - q25
    cut_off = iqr * 1.5
    lower, upper = q25 - cut_off, q75 + cut_off
    # identify outliers
    outliers = [x for x in df['own_duration'] if x < lower or x > upper]
    print('outliers:')
    for o in outliers:
        print(o)

    # df.loc[(df['Discount'] >= 1000) & (df['Discount'] <= 2000)]
    df_outliers = df.loc[(df['own_duration'] >= lower) & (df['own_duration'] <= upper)]
    for m in metrics:
        print(m)
        if m != 'ADDING_CLASS_DERIVABILITY':
            sns.lmplot(x="own_duration", y=m, data=df_outliers)
            plt.savefig('results/correlation/evo/' + project_name + '/' + project_name + '_' + m + '-outliers.pdf')
    # plt.show()

    df[metrics].corr().to_csv(output, index=False)
    df_outliers[metrics].corr().to_csv(output.replace('.csv', '_outliers.csv'), index=False)


# def join_jgit_dataset(project_name, commits_list):
#     # performance difference
#     df_pd = pd.read_csv('../dynamic_metrics/results/' + project_name + '-performance-diff.csv', sep=',') #ok
#     df_pd['project_name'] = project_name
#     df = pd.DataFrame().assign(project_name=df_pd['project_name'], commit_hash=df_pd['commit'], class_name=df_pd['class_name'],
#                                own_duration=df_pd['mean_val'])
#     df = df.merge(df_pd[['project_name', 'prevcommit', 'class_name', 'mean_val']].rename(columns={'prevcommit': 'commit_hash', 'mean_val': 'own_duration'}), how='outer')
#
#     ck_metrics = ['index', 'file', 'class', 'type', 'cbo_x', 'cboModified_x', 'fanin_x', 'fanout_x', 'wmc_x', 'dit',
#                   'noc', 'rfc_x', 'lcom', 'lcom*', 'tcc', 'lcc', 'totalMethodsQty', 'staticMethodsQty',
#                   'publicMethodsQty', 'privateMethodsQty', 'protectedMethodsQty', 'defaultMethodsQty',
#                   'visibleMethodsQty', 'abstractMethodsQty', 'finalMethodsQty', 'synchronizedMethodsQty',
#                   'totalFieldsQty', 'staticFieldsQty', 'publicFieldsQty', 'privateFieldsQty', 'protectedFieldsQty',
#                   'defaultFieldsQty', 'finalFieldsQty', 'synchronizedFieldsQty', 'nosi', 'loc_x', 'returnQty',
#                   'loopQty_x', 'comparisonsQty_x', 'tryCatchQty_x', 'parenthesizedExpsQty_x', 'stringLiteralsQty_x',
#                   'numbersQty_x', 'assignmentsQty_x', 'mathOperationsQty_x', 'variablesQty_x', 'maxNestedBlocksQty_x',
#                   'anonymousClassesQty_x', 'innerClassesQty_x', 'lambdasQty_x', 'uniqueWordsQty_x', 'modifiers_x',
#                   'logStatementsQty_x', 'method', 'constructor', 'line', 'cbo_y', 'cboModified_y', 'fanin_y',
#                   'fanout_y', 'wmc_y', 'rfc_y', 'loc_y', 'returnsQty', 'variablesQty_y', 'parametersQty',
#                   'methodsInvokedQty', 'methodsInvokedLocalQty', 'methodsInvokedIndirectLocalQty', 'loopQty_y',
#                   'comparisonsQty_y', 'tryCatchQty_y', 'parenthesizedExpsQty_y', 'stringLiteralsQty_y', 'numbersQty_y',
#                   'assignmentsQty_y', 'mathOperationsQty_y', 'maxNestedBlocksQty_y', 'anonymousClassesQty_y',
#                   'innerClassesQty_y', 'lambdasQty_y', 'uniqueWordsQty_y', 'modifiers_y', 'logStatementsQty_y',
#                   'hasJavaDoc', 'commit_hash', 'project_name']
#     df_ck = pd.read_csv('../static_metrics/results/ck/' + project_name + '-ck_all2.csv', usecols=ck_metrics, sep=',', index_col=False)
#     path1 = '/mnt/sda4/software-metrics/static_metrics/jgit/'
#     df_ck['file'] = df_ck['file'].str.replace(path1, '')
#     try:
#         spl_word = "commons-"
#         file_str = df_ck[df_ck['file'].str.contains(spl_word)].iloc[0]
#         res = file_str['file'].split(spl_word, 1)
#         splitString = res[0]
#         df_ck['file'] = df_ck.file.str.replace(splitString, '')
#     except:
#         pass
#     df = pd.merge(left=df, right=df_ck, left_on=['project_name', 'commit_hash', 'class_name'],
#                       right_on=['project_name', 'commit_hash', 'file'], how='left')
#
#
#     # understand
#     # und_metrics = ["index1", "index2", "index3", "index4", "index5", "index6", "index7", "Kind", "Name", "File",
#     und_metrics = ["Name", "File",
#     "AvgCyclomatic", "AvgCyclomaticModified", "AvgCyclomaticStrict",
#                    "AvgEssential", "AvgLine", "AvgLineBlank", "AvgLineCode", "AvgLineComment", "CountClassBase",
#                    "CountClassCoupled", "CountClassDerived", "CountDeclClass", "CountDeclClassMethod",
#                    "CountDeclClassVariable", "CountDeclFile", "CountDeclFunction", "CountDeclInstanceMethod",
#                    "CountDeclInstanceVariable", "CountDeclMethod", "CountDeclMethodAll",
#                    "CountDeclMethodDefault", "CountDeclMethodPrivate", "CountDeclMethodProtected",
#                    "CountDeclMethodPublic", "CountInput", "CountLine", "CountLineBlank", "CountLineCode",
#                    "CountLineCodeDecl", "CountLineCodeExe", "CountLineComment", "CountOutput", "CountPath",
#                    "CountSemicolon", "CountStmt", "CountStmtDecl", "CountStmtExe", "Cyclomatic",
#                    "CyclomaticModified", "CyclomaticStrict", "Essential", "MaxCyclomatic",
#                    "MaxCyclomaticModified", "MaxCyclomaticStrict", "MaxEssential", "MaxInheritanceTree",
#                    "MaxNesting", "PercentLackOfCohesion", "RatioCommentToCode", "SumCyclomatic",
#                    "SumCyclomaticModified", "SumCyclomaticStrict", "SumEssential", 'unknown', 'commit_hash',
#                    'project_name']
#     df_und = pd.read_csv('../static_metrics/results/und/und_all.csv', sep=',',
#                              engine='python', names=und_metrics)  # , nrows=5)
#     # df_und = df_und[df_und.columns[8:]]
#     # df_und['class'] = df_und['Name']
#
#     df = pd.merge(left=df, right=df_und, left_on=['project_name', 'commit_hash', 'file'],
#                       right_on=['project_name', 'commit_hash', 'File'], how='left')
#     # df.to_csv('results/static_features_ck_und.csv', sep=',', index=False)
#
#     # evolutionary metrics
#     evo_metrics = ["project", "commit", "commitprevious", "class", "BOM", "TACH", "FCH", "LCH", "CHO", "FRCH",
#                    "CHD", "WCD", "WFR", "ATAF", "LCA", "LCD", "CSB", "CSBS", "ACDF"]
#     df_evo = pd.read_csv('../static_metrics/results/evometrics/' + project_name + '-results-processMetrics.csv',
#                          usecols=evo_metrics, sep=',', index_col=False)
#     path1 = '/mnt/sda4/software-metrics/static_metrics/projectA/jgit/'
#     df_evo['file'] = df_evo['class'].str.replace(path1, '')
#     df = pd.merge(left=df, right=df_evo, left_on=['project_name', 'commit_hash', 'file'],
#                       right_on=['project', 'commit', 'file'], how='left')
#     # df.to_csv('results/static_features_evo.csv', sep=',', index=False)
#
#     # change distiller
#     changedistiller_metrics = ["PROJECT_NAME", "CURRENT_COMMIT", "PREVIOUS_COMMIT", "CLASS_CURRENTCOMMIT",
#                                "CLASS_PREVIOUSCOMMIT",
#                                "STATEMENT_DELETE", "STATEMENT_INSERT", "STATEMENT_ORDERING_CHANGE",
#                                "STATEMENT_PARENT_CHANGE", "STATEMENT_UPDATE", "TOTAL_STATEMENTLEVELCHANGES",
#                                "PARENT_CLASS_CHANGE", "PARENT_CLASS_DELETE", "PARENT_CLASS_INSERT", "CLASS_RENAMING",
#                                "TOTAL_CLASSDECLARATIONCHANGES",
#                                "RETURN_TYPE_CHANGE", "RETURN_TYPE_DELETE", "RETURN_TYPE_INSERT", "METHOD_RENAMING",
#                                "PARAMETER_DELETE", "PARAMETER_INSERT", "PARAMETER_ORDERING_CHANGE",
#                                "PARAMETER_RENAMING",
#                                "PARAMETER_TYPE_CHANGE", "TOTAL_METHODDECLARATIONSCHANGES",
#                                "ATTRIBUTE_RENAMING", "ATTRIBUTE_TYPE_CHANGE", "TOTAL_ATTRIBUTEDECLARATIONCHANGES",
#                                "ADDING_ATTRIBUTE_MODIFIABILITY", "REMOVING_ATTRIBUTE_MODIFIABILITY",
#                                "REMOVING_CLASS_DERIVABILITY", "REMOVING_METHOD_OVERRIDABILITY",
#                                "ADDING_CLASS_DERIVABILITY", "ADDING_CLASS_DERIVABILITY", "ADDING_METHOD_OVERRIDABILITY",
#                                "TOTAL_DECLARATIONPARTCHANGES", "TOTAL_CHANGES"]
#     df_cd = pd.read_csv('../static_metrics/results/changedistiller/' + project_name + '-changedistiller.csv',
#                             sep=',', index_col=False)
#     df_cd.columns = changedistiller_metrics
#     path1 = '/home/usuario/PycharmProjects/software-metrics/static_metrics/jgit1/'
#     df_cd['file'] = df_cd['CLASS_PREVIOUSCOMMIT'].str.replace(path1, '')
#     df = pd.merge(left=df, right=df_cd, left_on=['project_name', 'commit_hash', 'class_name'],
#                       right_on=['PROJECT_NAME', 'PREVIOUS_COMMIT', 'file'], how='left')
#
#     # # refactoring miner
#     # rm_metrics = ['class_name', 'commit_hash', 'destinationAddAttributeAnnotation', 'destinationAddAttributeModifier',
#     #               'destinationAddClassAnnotation', 'destinationAddClassModifier', 'destinationAddMethodAnnotation',
#     #               'destinationAddMethodModifier', 'destinationAddParameter', 'destinationAddParameterAnnotation',
#     #               'destinationAddParameterModifier', 'destinationAddThrownExceptionType',
#     #               'destinationAddVariableAnnotation',
#     #               'destinationAddVariableModifier', 'destinationChangeAttributeAccessModifier',
#     #               'destinationChangeAttributeType',
#     #               'destinationChangeClassAccessModifier', 'destinationChangeMethodAccessModifier',
#     #               'destinationChangeParameterType', 'destinationChangeReturnType',
#     #               'destinationChangeThrownExceptionType',
#     #               'destinationChangeTypeDeclarationKind', 'destinationChangeVariableType',
#     #               'destinationCollapseHierarchy', 'destinationEncapsulateAttribute',
#     #               'destinationExtractAndMoveMethod', 'destinationExtractAttribute', 'destinationExtractClass',
#     #               'destinationExtractInterface', 'destinationExtractMethod', 'destinationExtractSubclass',
#     #               'destinationExtractSuperclass', 'destinationExtractVariable', 'destinationInlineAttribute',
#     #               'destinationInlineMethod', 'destinationInlineVariable', 'destinationLocalizeParameter',
#     #               'destinationMergeAttribute', 'destinationMergeClass', 'destinationMergePackage',
#     #               'destinationMergeParameter', 'destinationMergeVariable', 'destinationModifyAttributeAnnotation',
#     #               'destinationModifyClassAnnotation', 'destinationModifyMethodAnnotation',
#     #               'destinationModifyVariableAnnotation', 'destinationMoveAndInlineMethod',
#     #               'destinationMoveAndRenameAttribute', 'destinationMoveAndRenameClass',
#     #               'destinationMoveAndRenameMethod', 'destinationMoveAttribute', 'destinationMoveClass',
#     #               'destinationMoveMethod', 'destinationMovePackage', 'destinationMoveSourceFolder',
#     #               'destinationParameterizeAttribute', 'destinationParameterizeVariable', 'destinationPullUpAttribute',
#     #               'destinationPullUpMethod', 'destinationPushDownAttribute', 'destinationPushDownMethod',
#     #               'destinationRemoveAttributeAnnotation', 'destinationRemoveAttributeModifier',
#     #               'destinationRemoveClassAnnotation', 'destinationRemoveClassModifier',
#     #               'destinationRemoveMethodAnnotation', 'destinationRemoveMethodModifier', 'destinationRemoveParameter',
#     #               'destinationRemoveParameterAnnotation', 'destinationRemoveParameterModifier',
#     #               'destinationRemoveThrownExceptionType', 'destinationRemoveVariableAnnotation',
#     #               'destinationRemoveVariableModifier', 'destinationRenameAttribute', 'destinationRenameClass',
#     #               'destinationRenameMethod', 'destinationRenamePackage', 'destinationRenameParameter',
#     #               'destinationRenameVariable', 'destinationReorderParameter', 'destinationReplaceAnonymousWithLambda',
#     #               'destinationReplaceAttribute', 'destinationReplaceAttributeWithVariable',
#     #               'destinationReplaceLoopWithPipeline', 'destinationReplacePipelineWithLoop',
#     #               'destinationReplaceVariableWithAttribute', 'destinationSplitAttribute',
#     #               'destinationSplitClass', 'destinationSplitConditional', 'destinationSplitPackage',
#     #               'destinationSplitParameter', 'destinationSplitVariable', 'projectName',
#     #               'sourceAddAttributeAnnotation',
#     #               'sourceAddAttributeModifier', 'sourceAddClassAnnotation', 'sourceAddClassModifier',
#     #               'sourceAddMethodAnnotation', 'sourceAddMethodModifier', 'sourceAddParameter',
#     #               'sourceAddParameterAnnotation', 'sourceAddParameterModifier', 'sourceAddThrownExceptionType',
#     #               'sourceAddVariableAnnotation', 'sourceAddVariableModifier', 'sourceChangeAttributeAccessModifier',
#     #               'sourceChangeAttributeType', 'sourceChangeClassAccessModifier', 'sourceChangeMethodAccessModifier',
#     #               'sourceChangeParameterType', 'sourceChangeReturnType', 'sourceChangeThrownExceptionType',
#     #               'sourceChangeTypeDeclarationKind', 'sourceChangeVariableType', 'sourceCollapseHierarchy',
#     #               'sourceEncapsulateAttribute', 'sourceExtractAndMoveMethod', 'sourceExtractAttribute',
#     #               'sourceExtractClass', 'sourceExtractInterface', 'sourceExtractMethod', 'sourceExtractSubclass',
#     #               'sourceExtractSuperclass', 'sourceExtractVariable', 'sourceInlineAttribute', 'sourceInlineMethod',
#     #               'sourceInlineVariable', 'sourceLocalizeParameter', 'sourceMergeAttribute', 'sourceMergeClass',
#     #               'sourceMergePackage', 'sourceMergeParameter', 'sourceMergeVariable',
#     #               'sourceModifyAttributeAnnotation',
#     #               'sourceModifyClassAnnotation', 'sourceModifyMethodAnnotation', 'sourceModifyVariableAnnotation',
#     #               'sourceMoveAndInlineMethod', 'sourceMoveAndRenameAttribute', 'sourceMoveAndRenameClass',
#     #               'sourceMoveAndRenameMethod', 'sourceMoveAttribute', 'sourceMoveClass', 'sourceMoveMethod',
#     #               'sourceMovePackage', 'sourceMoveSourceFolder', 'sourceParameterizeAttribute',
#     #               'sourceParameterizeVariable',
#     #               'sourcePullUpAttribute', 'sourcePullUpMethod', 'sourcePushDownAttribute', 'sourcePushDownMethod',
#     #               'sourceRemoveAttributeAnnotation', 'sourceRemoveAttributeModifier', 'sourceRemoveClassAnnotation',
#     #               'sourceRemoveClassModifier', 'sourceRemoveMethodAnnotation', 'sourceRemoveMethodModifier',
#     #               'sourceRemoveParameter', 'sourceRemoveParameterAnnotation', 'sourceRemoveParameterModifier',
#     #               'sourceRemoveThrownExceptionType', 'sourceRemoveVariableAnnotation', 'sourceRemoveVariableModifier',
#     #               'sourceRenameAttribute', 'sourceRenameClass', 'sourceRenameMethod', 'sourceRenamePackage',
#     #               'sourceRenameParameter', 'sourceRenameVariable', 'sourceReorderParameter',
#     #               'sourceReplaceAnonymousWithLambda',
#     #               'sourceReplaceAttribute', 'sourceReplaceAttributeWithVariable', 'sourceReplaceLoopWithPipeline',
#     #               'sourceReplacePipelineWithLoop', 'sourceReplaceVariableWithAttribute', 'sourceSplitAttribute',
#     #               'sourceSplitClass', 'sourceSplitConditional', 'sourceSplitPackage', 'sourceSplitParameter',
#     #               'sourceSplitVariable']
#     #
#     # rm_values = pd.read_csv('../static_metrics/results/refactoring/' + project_name + '-refactoring.csv', names=rm_metrics, sep=',', index_col=False)
#     #
#     # rm_values['file'] = rm_values['projectName'] + '/' + rm_values['class_name']
#     #
#     # df = pd.merge(left=df, right=rm_values, left_on=['project_name', 'commit_hash', 'class'],
#     #                   right_on=['projectName', 'commit_hash', 'file'], how='outer')
#
#     df.to_csv('../static_metrics/results/static_features_correlation.csv', sep=',', index=False)
#
#     #plot correlations
#     # metrics = ['own_duration'] + ck_metrics[4:52] + ck_metrics[55:83]
#     #
#     # for m in metrics:
#     #     sns.lmplot(x="own_duration", y=m, data=df)
#     #     plt.savefig('results/correlation/ck/' + m + '.pdf')
#     # # plt.show()
#     #
#     # df[metrics].corr().to_csv('results/correlation/ck_correlation.csv')
#
#
#     # understand
#     # metrics = ['own_duration'] + und_metrics[2:55]
#     # df[metrics] = df[metrics].astype(float)
#     # for m in metrics:
#     #     print(m)
#     #     sns.lmplot(x="own_duration", y=m, data=df)
#     #     plt.savefig('results/correlation/und/' + m + '.pdf')
#     # # plt.show()
#     #
#     # df[metrics].corr().to_csv('results/correlation/und_correlation.csv')
#
#     #evolutionary
#     # metrics = ['own_duration'] + evo_metrics[4:]
#     # df[metrics] = df[metrics].astype(float)
#     # for m in metrics:
#     #     print(m)
#     #     sns.lmplot(x="own_duration", y=m, data=df)
#     #     plt.savefig('results/correlation/evo/' + m + '.pdf')
#     # plt.show()
#
#     # df[metrics].corr().to_csv('results/correlation/evo_correlation.csv')
#
#     # change distiller
#     metrics = ['own_duration'] + changedistiller_metrics[5:]
#
#     for m in metrics:
#         print(m)
#         print(df[m].shape)
#         print('---')
#         print(df['own_duration'].shape)
#         if m != 'own_duration' and m != 'ADDING_CLASS_DERIVABILITY':
#             sns.lmplot(x="own_duration", y=m, data=df)
#             plt.savefig('results/correlation/cd/' + m + '.pdf')
#     # plt.show()
#
#     df[metrics].corr().to_csv('results/correlation/cd_correlation.csv')
#     return df

if __name__ == "__main__":

    projects = ['commons-bcel', 'commons-text', 'easymock', 'jgit', 'Openfire']
    # projects = ['commons-bcel']
    for project_name in projects:
        # all instances using avg
        trace_file = '../6.join_metrics/results/' + project_name + '-all-releases.csv'

        # 1) ck avg
        output = 'results/correlation/ck/' + project_name + '/' + project_name + '_ck_correlation_avg.csv'
        ck_file = '../static_metrics/results/ck/' + project_name + 'ck_2.csv'
        ck_cor = ck_ownduration_correlation(project_name, trace_file, ck_file, 'avg', output)

        # 2) und avg
        output = 'results/correlation/und/' + project_name + '/' + project_name + '_und_correlation_avg.csv'
        und_cor = und_ownduration_correlation(project_name, trace_file, 'avg', output)

        # 3) evo avg
        output = 'results/correlation/evo/' + project_name + '/' + project_name + 'evo_correlation_avg.csv'
        evo_cor = evo_ownduration_correlation(project_name, trace_file, 'avg', output)

        # 4) change distiller avg
        output = 'results/correlation/cd/' + project_name + '/' + project_name + '_cd_correlation_avg.csv'
        cd_cor = cd_ownduration_correlation(project_name, trace_file, 'avg', output)
        #
        #
        # # mean value greater than the median of the commit to be considered a performance change
        trace_file = '../dynamic_metrics/results/' + project_name + '/' + project_name + '-class-performance-median_filtered.csv'
        ck_file = '../static_metrics/results/ck/' + project_name + 'ck_2.csv'
        output = 'results/correlation/ck/' + project_name + '/' + project_name + '_ck_correlation_median.csv'
        ck_cor = ck_ownduration_correlation(project_name, trace_file, ck_file, 'median', output)
        output = 'results/correlation/und/' + project_name + '/' + project_name + '_und_correlation_median.csv'
        und_cor = und_ownduration_correlation(project_name, trace_file, 'median', output)
        output = 'results/correlation/evo/' + project_name + '/' + project_name + 'evo_correlation_median.csv'
        evo_cor = evo_ownduration_correlation(project_name, trace_file, 'median', output)
        output = 'results/correlation/cd/' + project_name + '/' + project_name + '_cd_correlation_median.csv'
        cd_cor = cd_ownduration_correlation(project_name, trace_file, 'median', output)
        #
        # # t-student statistical significance to be considered a performance change
        trace_file = '../dynamic_metrics/results/' + project_name + '/' + project_name + '-class-performance-diff_filtered.csv'
        ck_file = '../static_metrics/results/ck/' + project_name + 'ck_2.csv'
        output = 'results/correlation/ck/' + project_name + '/' + project_name + '_ck_correlation_diff.csv'
        ck_cor = ck_ownduration_correlation(project_name, trace_file, ck_file, 'diff', output)
        output = 'results/correlation/und/' + project_name + '/' + project_name + '_und_correlation_diff.csv'
        und_cor = und_ownduration_correlation(project_name, trace_file, 'diff', output)
        output = 'results/correlation/evo/' + project_name + '/' + project_name + 'evo_correlation_diff.csv'
        evo_cor = evo_ownduration_correlation(project_name, trace_file, 'diff', output)
        output = 'results/correlation/cd/' + project_name + '/' + project_name + '_cd_correlation_diff.csv'
        cd_cor = cd_ownduration_correlation(project_name, trace_file, 'diff', output)

    print('end')