
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

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
# main_columns: file, class ,method, constructor, line, cbo, cboModified, fanin, fanout, wmc, rfc, loc, returnsQty, variablesQty, parametersQty, methodsInvokedQty, methodsInvokedLocalQty, methodsInvokedIndirectLocalQty, loopQty, comparisonsQty, tryCatchQty, parenthesizedExpsQty, stringLiteralsQty, numbersQty, assignmentsQty, mathOperationsQty, maxNestedBlocksQty, anonymousClassesQty, innerClassesQty, lambdasQty, uniqueWordsQty, modifiers, logStatementsQty, hasJavaDoc, method_name, current_hash, Kind, Name, File, AvgCyclomatic, AvgCyclomaticModified, AvgCyclomaticStrict, AvgEssential, AvgLine, AvgLineBlank, AvgLineCode, AvgLineComment, CountClassBase, CountClassCoupled, CountClassDerived, CountDeclClass, CountDeclClassMethod, CountDeclClassVariable, CountDeclFile, CountDeclFunction, CountDeclInstanceMethod, CountDeclInstanceVariable, CountDeclMethod, CountDeclMethodAll, CountDeclMethodDefault, CountDeclMethodPrivate, CountDeclMethodProtected, CountDeclMethodPublic, CountInput, CountLine, CountLineBlank, CountLineCode, CountLineCodeDecl, CountLineCodeExe, CountLineComment, CountOutput, CountPath, CountSemicolon, CountStmt, CountStmtDecl, CountStmtExe, Cyclomatic, CyclomaticModified, CyclomaticStrict, Essential, MaxCyclomatic, MaxCyclomaticModified, MaxCyclomaticStrict, MaxEssential, MaxInheritanceTree, MaxNesting, PercentLackOfCohesion, RatioCommentToCode, SumCyclomatic, SumCyclomaticModified, SumCyclomaticStrict, SumEssential, project, commit, commitprevious, release, file, method, BOC, TACH, FCH, LCH, CHO, FRCH, CHD, WCH, WCD, WFR, ATAF, LCA, LCD, CSB, CSBS, ACDF, PROJECT_NAME, PREVIOUS_COMMIT, CURRENT_COMMIT, CLASS_CURRENTCOMMIT, CLASS_PREVIOUSCOMMIT, CLASS_CURRENTNAME, CLASS_PREVIOUSNAME, STATEMENT_DELETE, STATEMENT_INSERT, STATEMENT_ORDERING_CHANGE, STATEMENT_PARENT_CHANGE, STATEMENT_UPDATE, TOTAL_STATEMENTLEVELCHANGES, PARENT_CLASS_CHANGE, PARENT_CLASS_DELETE, PARENT_CLASS_INSERT, CLASS_RENAMING, TOTAL_CLASSDECLARATIONCHANGES, RETURN_TYPE_CHANGE, RETURN_TYPE_DELETE, RETURN_TYPE_INSERT, METHOD_RENAMING, PARAMETER_DELETE, PARAMETER_INSERT, PARAMETER_ORDERING_CHANGE, PARAMETER_RENAMING, PARAMETER_TYPE_CHANGE, TOTAL_METHODDECLARATIONSCHANGES, ATTRIBUTE_RENAMING, ATTRIBUTE_TYPE_CHANGE, TOTAL_ATTRIBUTEDECLARATIONCHANGES, ADDING_ATTRIBUTE_MODIFIABILITY, REMOVING_ATTRIBUTE_MODIFIABILITY, REMOVING_CLASS_DERIVABILITY, REMOVING_METHOD_OVERRIDABILITY, ADDING_CLASS_DERIVABILITY, ADDING_CLASS_DERIVABILITY, ADDING_METHOD_OVERRIDABILITY, TOTAL_DECLARATIONPARTCHANGES, TOTAL_CHANGES, will_change

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

struc1 = ['cbo', 'cboModified', 'fanin', 'fanout', 'wmc',
                      'rfc', 'loc', 'returnsQty', 'variablesQty', 'parametersQty', 'methodsInvokedQty',
                      'methodsInvokedLocalQty', 'methodsInvokedIndirectLocalQty', 'loopQty', 'comparisonsQty',
                      'tryCatchQty', 'parenthesizedExpsQty', 'stringLiteralsQty', 'numbersQty', 'assignmentsQty',
                      'mathOperationsQty', 'maxNestedBlocksQty', 'anonymousClassesQty', 'innerClassesQty',
                      'lambdasQty']

struc2 = ['uniqueWordsQty', 'modifiers', 'logStatementsQty', 'hasJavaDoc',
                      "AvgCyclomatic", "AvgCyclomaticModified", "AvgCyclomaticStrict",
                      "AvgEssential", "AvgLine", "AvgLineBlank", "AvgLineCode", "AvgLineComment", "CountClassBase",
                      "CountClassCoupled", "CountClassDerived", "CountDeclClass", "CountDeclClassMethod",
                      "CountDeclClassVariable", "CountDeclFile", "CountDeclFunction", "CountDeclInstanceMethod",
                      "CountDeclInstanceVariable", "CountDeclMethod", "CountDeclMethodAll",
                      "CountDeclMethodDefault"]
struc3 = ["CountDeclMethodPrivate", "CountDeclMethodProtected", "CountDeclMethodPublic", "CountInput",
                      "CountLine", "CountLineBlank", "CountLineCode", "CountLineCodeDecl", "CountLineCodeExe",
                      "CountLineComment", "CountOutput", "CountPath", "CountSemicolon", "CountStmt",
                      "CountStmtDecl"]
struc4 = ["CountStmtExe", "Cyclomatic", "CyclomaticModified", "CyclomaticStrict", "Essential",
                      "MaxCyclomatic", "MaxCyclomaticModified", "MaxCyclomaticStrict", "MaxEssential",
                      "MaxInheritanceTree", "MaxNesting", "PercentLackOfCohesion", "RatioCommentToCode",
                      "SumCyclomatic", "SumCyclomaticModified", "SumCyclomaticStrict", "SumEssential"]


for project in projects:
    df = pd.read_csv(
        '../6.join_metrics/results/' + project + '-all-releases.csv')
    df.columns = main_columns
    df = df.fillna(0)

    fig, ax = plt.subplots()
    # sns.boxplot(x='variable', y='value', data=df)
    # box = sns.boxplot(x=col1, y=col2, data=df, ax=ax).set(xlabel=col1, ylabel=col2)
    box = df.boxplot(column=struc1)
    # fig = box.get_figure()
    plt.xticks(rotation=15)
    plt.savefig('results/charts/' + project + 'struc1-features-boxplot.pdf')
    plt.close()

    fig, ax = plt.subplots()
    # sns.boxplot(x='variable', y='value', data=df)
    # box = sns.boxplot(x=col1, y=col2, data=df, ax=ax).set(xlabel=col1, ylabel=col2)
    box = df.boxplot(column=struc2)
    # fig = box.get_figure()
    plt.xticks(rotation=15)
    plt.savefig('results/charts/' + project + 'struc2-features-boxplot.pdf')
    plt.close()

    fig, ax = plt.subplots()
    # sns.boxplot(x='variable', y='value', data=df)
    # box = sns.boxplot(x=col1, y=col2, data=df, ax=ax).set(xlabel=col1, ylabel=col2)
    box = df.boxplot(column=struc3)
    # fig = box.get_figure()
    plt.xticks(rotation=15)
    plt.savefig('results/charts/' + project + 'struc3-features-boxplot.pdf')
    plt.close()

    fig, ax = plt.subplots()
    # sns.boxplot(x='variable', y='value', data=df)
    # box = sns.boxplot(x=col1, y=col2, data=df, ax=ax).set(xlabel=col1, ylabel=col2)
    box = df.boxplot(column=struc4)
    # fig = box.get_figure()
    plt.xticks(rotation=15)
    plt.savefig('results/charts/' + project + 'struc4-features-boxplot.pdf')
    plt.close()