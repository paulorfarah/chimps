from mdi import mdi
from information_gain import information_gain_cpmp
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

def plot_ranking(df):
    sns.set(font_scale=1.5)
    df['rank'] = df['rank'].astype(int)
    df1 = df[df['rank'] == 1]
    df1 = df1.metric.value_counts()
    print(df1.index)
    plot = df1.plot.pie(y='0', autopct='%1.1f%%', startangle=90, figsize=(5, 5), ylabel='', xlabel='')
#     plot = df1.plot.pie(y='metric', figsize=(5, 5))
#     plt.axes().set_ylabel('')
    plt.savefig('results/cpmp/top1.pdf')
    # plt.close()

    # top5

    df1 = df[df['rank'] <= 5]
    df1 = df1.metric.value_counts()
    print(df1.index)
    # plot = df1.plot.pie(y='0', autopct='%1.1f%%', startangle=90, figsize=(7, 7), textprops={'fontsize': 14})
    plot = df1.plot.barh(figsize=(11, 5))

    plt.xticks(range(1, df1.max() + 1))
    plt.savefig('results/cpmp/top5.pdf')
    plt.close()


def plot_barh(df, filename):
    # matplotlib.rcParams.update({'font.size': 16})
    # sns.set(font_scale=1.2)
    plt.figure(figsize=(8, 8))

    graph = plt.barh(
        df.index.to_list(),
        df['count'],
        color="lightsteelblue",
    )
    plt.xticks(range(0, df['count'].max() + 1))
    # plt.xlim([0, 100])
    i = 0
    for p in graph:
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy()
        plt.text(x + width,
                 y + height * 0.3,
                 str(df.percent[i]) + '%',
                 ha='center')
        i += 1
    plt.tight_layout()
    plt.savefig('results/cpmp/' + filename)

    # courses = list(data.keys())
    # values = list(data.values())
    #
    # fig = plt.figure(figsize=(10, 5))
    #
    # # creating the bar plot
    # plt.barh(courses, values, color='maroon')
    #
    # plt.xlabel("Courses offered")
    # plt.ylabel("No. of students enrolled")
    # plt.title("Students enrolled in different courses")
    # plt.show()


def plot_pie(df, filename):
    matplotlib.rcParams.update({'font.size': 16})
    # sns.set(font_scale=1.2)
    plt.figure(figsize=(8, 8))

    plt.pie(
        x=df['count'],
        labels=df.index.to_list(),
        # autopct='%1.2f%%',
        # colors=sns.color_palette('magma'),
        startangle=90,
        # Add space around only one slice
        # explode=[0, 0, 0, 0, 0.12, 0]
    )
    plt.savefig('results/cpmp/' + filename)


if __name__ == "__main__":
    projects = ['commons-bcel', 'commons-csv', 'commons-io', 'easymock', 'Openfire', 'pdfbox', 'wro4j']
    # projects = ['commons-bcel', 'commons-csv']
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
        'commitprevious', 'release', 'file', 'method', 'BOM', 'TACH', 'FCH', 'LCH', 'CHO',
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
    #main_columns: file, class ,method, constructor, line, cbo, cboModified, fanin, fanout, wmc, rfc, loc, returnsQty, variablesQty, parametersQty, methodsInvokedQty, methodsInvokedLocalQty, methodsInvokedIndirectLocalQty, loopQty, comparisonsQty, tryCatchQty, parenthesizedExpsQty, stringLiteralsQty, numbersQty, assignmentsQty, mathOperationsQty, maxNestedBlocksQty, anonymousClassesQty, innerClassesQty, lambdasQty, uniqueWordsQty, modifiers, logStatementsQty, hasJavaDoc, method_name, current_hash, Kind, Name, File, AvgCyclomatic, AvgCyclomaticModified, AvgCyclomaticStrict, AvgEssential, AvgLine, AvgLineBlank, AvgLineCode, AvgLineComment, CountClassBase, CountClassCoupled, CountClassDerived, CountDeclClass, CountDeclClassMethod, CountDeclClassVariable, CountDeclFile, CountDeclFunction, CountDeclInstanceMethod, CountDeclInstanceVariable, CountDeclMethod, CountDeclMethodAll, CountDeclMethodDefault, CountDeclMethodPrivate, CountDeclMethodProtected, CountDeclMethodPublic, CountInput, CountLine, CountLineBlank, CountLineCode, CountLineCodeDecl, CountLineCodeExe, CountLineComment, CountOutput, CountPath, CountSemicolon, CountStmt, CountStmtDecl, CountStmtExe, Cyclomatic, CyclomaticModified, CyclomaticStrict, Essential, MaxCyclomatic, MaxCyclomaticModified, MaxCyclomaticStrict, MaxEssential, MaxInheritanceTree, MaxNesting, PercentLackOfCohesion, RatioCommentToCode, SumCyclomatic, SumCyclomaticModified, SumCyclomaticStrict, SumEssential, project, commit, commitprevious, release, file, method, BOC, TACH, FCH, LCH, CHO, FRCH, CHD, WCH, WCD, WFR, ATAF, LCA, LCD, CSB, CSBS, ACDF, PROJECT_NAME, PREVIOUS_COMMIT, CURRENT_COMMIT, CLASS_CURRENTCOMMIT, CLASS_PREVIOUSCOMMIT, CLASS_CURRENTNAME, CLASS_PREVIOUSNAME, STATEMENT_DELETE, STATEMENT_INSERT, STATEMENT_ORDERING_CHANGE, STATEMENT_PARENT_CHANGE, STATEMENT_UPDATE, TOTAL_STATEMENTLEVELCHANGES, PARENT_CLASS_CHANGE, PARENT_CLASS_DELETE, PARENT_CLASS_INSERT, CLASS_RENAMING, TOTAL_CLASSDECLARATIONCHANGES, RETURN_TYPE_CHANGE, RETURN_TYPE_DELETE, RETURN_TYPE_INSERT, METHOD_RENAMING, PARAMETER_DELETE, PARAMETER_INSERT, PARAMETER_ORDERING_CHANGE, PARAMETER_RENAMING, PARAMETER_TYPE_CHANGE, TOTAL_METHODDECLARATIONSCHANGES, ATTRIBUTE_RENAMING, ATTRIBUTE_TYPE_CHANGE, TOTAL_ATTRIBUTEDECLARATIONCHANGES, ADDING_ATTRIBUTE_MODIFIABILITY, REMOVING_ATTRIBUTE_MODIFIABILITY, REMOVING_CLASS_DERIVABILITY, REMOVING_METHOD_OVERRIDABILITY, ADDING_CLASS_DERIVABILITY, ADDING_CLASS_DERIVABILITY, ADDING_METHOD_OVERRIDABILITY, TOTAL_DECLARATIONPARTCHANGES, TOTAL_CHANGES, will_change

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
        'BOM', 'TACH', 'FCH', 'LCH', 'CHO', 'FRCH', 'CHD', 'WCH', 'WCD', 'WFR', 'ATAF', 'LCA', 'LCD', 'CSB', 'CSBS',
        'ACDF',
    ]
    change_distiller_metrics = [
        "TOTAL_CHANGES"
        "will_change"
    ]

    model1 = structural_metrics
    model2 = structural_metrics + evolutionary_metrics
    model3 = evolutionary_metrics

    ### mdi
    res = mdi(projects, main_columns, model2)
    res['rank'] = res['rank'].astype(int)
    # df1 = res[res['rank'] == 1]
    # df1 = pd.DataFrame(df1.metric.value_counts())
    # df1.columns = ['count']
    # print(df1.index)
    #
    # df1['percent'] = (df1['count'] /
    #                   df1['count'].sum()) * 100
    # plot_pie(df1, 'mdi-top1.pdf')
    # df1.to_csv('results/cpmp/mdi-df1.csv')
    #
    # df5 = res[res['rank'] <= 5]
    # df5 = pd.DataFrame(df5.metric.value_counts())
    # df5.columns = ['count']
    # # print(df1.index)
    #
    # df5['percent'] = (df5['count'] /
    #                   df5['count'].sum()) * 100
    # df5['percent'] = df5['percent'].round(1)
    # df5.sort_values(by=['percent'], ascending=False)
    # df5 = df5.rename_axis('metrics').sort_values(by=['percent', 'metrics'], ascending=[True, False])
    # plot_barh(df5, 'mdi-top5.pdf')
    # df5.to_csv('results/cpmp/mdi-top5.csv')

    df5 = res[res['rank'] <= 10]
    df5 = pd.DataFrame(df5.metric.value_counts())
    df5.columns = ['count']
    # print(df1.index)

    df5['percent'] = (df5['count'] /
                      df5['count'].sum()) * 100
    df5['percent'] = df5['percent'].round(1)
    df5.sort_values(by=['percent'], ascending=False)
    df5 = df5.rename_axis('metrics').sort_values(by=['percent', 'metrics'], ascending=[True, False])
    plot_barh(df5, 'mdi-top10.pdf')
    df5.to_csv('results/cpmp/mdi-top10.csv')


    ### information gain
    res = information_gain_cpmp(projects, main_columns, model2)

    res['rank'] = res['rank'].astype(int)
    # df1 = res[res['rank'] == 1]
    # df1 = pd.DataFrame(df1.metric.value_counts())
    # df1.columns = ['count']
    # # print(df1.index)
    #
    #
    # df1['percent'] = (df1['count'] /
    #                   df1['count'].sum()) * 100
    # plot_pie(df1, 'infgain-top1.pdf')
    # df1.to_csv('results/cpmp/infgian-top1.csv')
    #
    # df5 = res[res['rank'] <= 5]
    # df5 = pd.DataFrame(df5.metric.value_counts())
    # df5.columns = ['count']
    # # print(df1.index)
    #
    # df5['percent'] = (df5['count'] /
    #                   df5['count'].sum()) * 100
    # df5['percent'] = df5['percent'].round(1)
    # df5.sort_values(by=['percent'], ascending=False)
    # df5 = df5.rename_axis('metrics').sort_values(by=['percent', 'metrics'], ascending=[True, False])
    # plot_barh(df5, 'infgain-top5.pdf')
    # df5.to_csv('results/cpmp/infgain-top5.csv')

    df5 = res[res['rank'] <= 10]
    df5 = pd.DataFrame(df5.metric.value_counts())
    df5.columns = ['count']
    # print(df1.index)

    df5['percent'] = (df5['count'] /
                      df5['count'].sum()) * 100
    df5['percent'] = df5['percent'].round(1)
    df5.sort_values(by=['percent'], ascending=False)
    df5 = df5.rename_axis('metrics').sort_values(by=['percent', 'metrics'], ascending=[True, False])
    plot_barh(df5, 'infgain-top10.pdf')
    df5.to_csv('results/cpmp/infgain-top10.csv')
