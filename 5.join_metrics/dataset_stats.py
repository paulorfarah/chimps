import pandas as pd
from matplotlib import pyplot as plt


def performance_stats(df):
    print(len(df['release'].unique()))
    print(len(df['commit_hash'].unique()))
    print(len(df['class'].unique()))
    print(len(df['method'].unique()))
    print(len(df['method']))
    print(len(df['perf_change']))
    df_cpmp = df.groupby(['will_change']).size()
    print(df_cpmp)
    df_perf = df.groupby(['perf_change']).size()
    print(df_perf)

    df2 = len(df[(df["perf_change"] == 1) &
                 (df["will_change"] == 1)])
    print(df2)


def cpmp_stats(df):
    main_columns = [
        # ck
        'file', 'class', 'method_ck', 'constructor', 'line', 'cbo', 'cboModified', 'fanin', 'fanout', 'wmc',
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
        'commitprevious', 'release', 'file', 'method_evo', 'BOC', 'TACH', 'FCH', 'LCH', 'CHO',
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
    df.columns = main_columns
    print('releases:' + str(len(df['release'].unique())))
    print('commits: ' + str(len(df['current_hash'].unique())))
    print('classes: ' + str(len(df['class'].unique())))
    print('methods: ' + str(len(df['method_name'].unique())))
    print('#methods: ' +  str(len(df['method_name'])))
    print('changes: ' + str(len(df['will_change'])))
    df_change = df.groupby(['will_change']).size()
    print(df_change)


if __name__ == "__main__":
    # projects = ['commons-bcel', 'commons-csv', 'commons-io',  'easymock', 'Openfire', 'pdfbox', 'wro4j']
    projects = ['commons-bcel', 'commons-csv', 'jgit', 'easymock','Openfire']
    for project_name in projects:
        print('-- ' + project_name + ' --')
        df = pd.read_csv('../6.join_metrics/results/' + project_name + '-perf-diff-all.csv')
        performance_stats(df)
        # df = pd.read_csv('../6.join_metrics/results/' + project_name + '-all-releases.csv')
        # cpmp_stats(df)
    #     releases = df['release'].unique()
    #     res = df.groupby(['release', 'commit_hash', 'class']).count()
    #     print(res)
        # for release in releases:
        #
