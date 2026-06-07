import re

import pandas as pd


packs = {'commons-bcel': ['examples\/', 'src\/examples\/', 'src\/java\/', 'src\/main\/java\/',
                                              'src\/test\/', 'src\/test\/java\/'],
         'commons-io': ['src\/test\/java\/', 'src\/java\/', 'src\/main\/java\/', 'src\/test\/'],
         'junit4': ['src\/test\/java\/', 'src\/java\/', 'src\/main\/java\/', 'src\/test\/', ''],
         'pdfbox': ['src\/test\/java\/', 'src\/java\/', 'src\/main\/java\/', 'src\/test\/',
                    'ant\/src\/main\/java\/', 'examples\/src\/main\/java\/',
                    'lucene\/src\/main\/java\/', 'preflight\/src\/main\/java\/',
                    'pdfbox\/src\/main\/java\/', 'jempbox\/src\/main\/java\/',
                    'xmpbox\/src\/main\/java\/', 'fontbox\/src\/main\/java\/',
                    'fontbox\/src\/test\/java\/', 'debugger\/src\/main\/java\/',
                    'tools\/src\/main\/java\/', 'pdfbox\/src\/test\/java\/',
                    'xmpbox\/src\/test\/java\/', 'examples\/src\/test\/java',
                    'preflight\/src\/test\/java\/',
                    ''],
         'wro4j': ['src\/test\/java\/', 'src\/java\/', 'src\/main\/java\/', 'src\/test\/',
                'wro4j-examples\/src\/main\/java\/', 'wro4j-maven-plugin\/src\/main\/java\/',
                   'wro4j-extensions\/src\/main\/java\/', 'wro4j-test-utils\/src\/main\/java\/',
                   'wro4j-core\/src\/main\/java\/',
                   'wro4j-examples\/src\/test\/java\/', 'wro4j-maven-plugin\/src\/test\/java\/',
                   'wro4j-extensions\/src\/test\/java\/', 'wro4j-test-utils\/src\/test\/java\/',
                   'wro4j-core\/src\/test\/java\/', ''],
         'commons-csv': ['src\/test\/java\/', 'src\/java\/', 'src\/main\/java\/', 'src\/test\/', ''],
         'easymock': ['src\/samples\/java\/',
                      'bench\/src\/main\/java\/', 'core\/src\/main\/java\/', 'core\/src\/samples\/java\/',
                      'core\/src\/test\/java\/', 'test-android\/src\/main\/java\/', 'test-deploy\/src\/main\/java\/',
                      'test-integration\/src\/main\/java\/', 'test-integration\/src\/test\/java\/',
                      'test-java8\/src\/test\/java\/', 'test-junit5\/src\/test\/java\/', 'test-nodeps\/src\/test\/java\/',
                      'test-osgi\/src\/test\/java\/', 'test-testng\/src\/test\/java\/',
                      'src\/test\/java\/', 'src\/java\/', 'src\/main\/java\/', 'src\/test\/',
                      'easymock\/src\/samples\/java\/',
                      'easymock\/bench\/src\/main\/java\/', 'easymock\/core\/src\/main\/java\/', 'easymock\/core\/src\/samples\/java\/',
                      'easymock\/core\/src\/test\/java\/', 'easymock\/test-android\/src\/main\/java\/', 'easymock\/test-deploy\/src\/main\/java\/',
                      'easymock\/test-integration\/src\/main\/java\/', 'easymock\/test-integration\/src\/test\/java\/',
                      'easymock\/test-java8\/src\/test\/java\/', 'easymock\/test-junit5\/src\/test\/java\/', 'easymock\/test-nodeps\/src\/test\/java\/',
                      'easymock\/test-osgi\/src\/test\/java\/', 'easymock\/test-testng\/src\/test\/java\/',
                      'easymock\/src\/test\/java\/', 'easymock\/src\/java\/', 'easymock\/src\/main\/java\/', 'easymock\/src\/test\/',
                      ''],
         'jgit': ['org.eclipse.jgit.ant.test\/', 'org.eclipse.jgit.ant\/', 'org.eclipse.jgit.archive\/', 'org.eclipse.jgit.http.apache\/',
                    'org.eclipse.jgit.http.server\/', 'org.eclipse.jgit.http.test\/', 'org.eclipse.jgit.junit.http\/', 'org.eclipse.jgit.junit\/',
                    'org.eclipse.jgit.lfs.server.test\/', 'org.eclipse.jgit.lfs.server\/', 'org.eclipse.jgit.lfs.test\/',
                    'org.eclipse.jgit.lfs\/', 'org.eclipse.jgit.packaging\/', 'org.eclipse.jgit.pgm.test\/',
                    'org.eclipse.jgit.pgm\/', 'org.eclipse.jgit.test\/tst\/', 'org.eclipse.jgit.test\/', 'org.eclipse.jgit.ui\/',
                  'org.eclipse.jgit\/', 'org.eclipse.jgit.src\/', ''],
         'Openfire': ['src\/java\/', 'src\/test\/java']
    }


ck = ['file', 'class', 'method', 'constructor', 'line', 'cbo', 'cboModified', 'fanin', 'fanout', 'wmc',
                      'rfc', 'loc', 'returnsQty', 'variablesQty', 'parametersQty', 'methodsInvokedQty',
                      'methodsInvokedLocalQty', 'methodsInvokedIndirectLocalQty', 'loopQty', 'comparisonsQty',
                      'tryCatchQty', 'parenthesizedExpsQty', 'stringLiteralsQty', 'numbersQty', 'assignmentsQty',
                      'mathOperationsQty', 'maxNestedBlocksQty', 'anonymousClassesQty', 'innerClassesQty', 'lambdasQty',
                      'uniqueWordsQty', 'modifiers', 'logStatementsQty', 'hasJavaDoc']
added = ['method_name', 'commit_hash']
und = ["Kind", "Name", "File", "AvgCyclomatic", "AvgCyclomaticModified", "AvgCyclomaticStrict",
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
                         "SumCyclomatic", "SumCyclomaticModified", "SumCyclomaticStrict", "SumEssential"]
evo = ['project', 'commit', 'commitprevious', 'release', 'file', 'method', 'BOM', 'TACH', 'FCH', 'LCH', 'CHO',
               'FRCH', 'CHD', 'WCH', 'WCD', 'WFR', 'ATAF', 'LCA', 'LCD', 'CSB', 'CSBS', 'ACDF']

cd = ["PROJECT_NAME", "PREVIOUS_COMMIT", "CURRENT_COMMIT", "CLASS_CURRENTCOMMIT", "CLASS_PREVIOUSCOMMIT",
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
               "TOTAL_DECLARATIONPARTCHANGES", "TOTAL_CHANGES", 'will_change']

cols = ck + added + und + evo + cd
def format_method(row):
    # public java.lang.String org.jivesoftware.openfire.IQHandlerInfo.getNamespace()

    method_name = row['method_name']
    patternMethod = r'[a-zA-Z0-9._]+\([a-zA-Z0-9 .,_\[\]<>]*\)'
    method = re.search(patternMethod, method_name)
    if method:
        method_name = method[0]

    proj = row['project']
    for p in packs[proj]:
        pattern = r'^\/' + p
        name = re.split(pattern, method_name)
        if len(name) > 1:
            method_name = name[1]
            break

    method_name = method_name.replace('/', '.')
    method_name = method_name.replace(' ', '')
    return method_name



project_name = 'commons-bcel'
df = pd.read_csv('results/' + project_name + '-all-releases.csv')
df.columns = cols

df_perf = pd.read_csv('../3.performance/results/' + project_name + '/' + project_name + '-method-performance-diff_all.csv')

# commit_hash,prevcommit,class_name,method_name,metric,stat,pvalue,mean_val,avg2,change,perf_change,change_abs
df_perf.columns = ['commit_hash', 'prevcommit', 'class_name', 'method_name', 'metric', 'stat', 'pvalue', 'mean_val',
                   'avg2', 'change', 'perf_change', 'change_abs']
df_perf['project'] = project_name
df_perf['original_method_name'] = df_perf['method_name']

if len(df.index) and len(df_perf.index):
    df_perf['method_name'] = df_perf.apply(format_method, axis=1)
    df_perf2 = df_perf[['project', 'commit_hash', 'method_name', 'perf_change']]
    df_joined_outer = pd.merge(left=df, right=df_perf2, on=['commit_hash', 'method_name'], how='outer',
                               indicator=True)
    df_disjoint = df_joined_outer.query('_merge != "both"')[['method_name', '_merge']]
    df_disjoint_both = df_joined_outer.query('_merge != "both"')[['method_name', '_merge']]
    df_disjoint_right = df_joined_outer.query('_merge == "right_only"')[['method_name', '_merge']]
    df_disjoint_left = df_joined_outer.query('_merge == "left_only"')[['method_name', '_merge']]
    df_joined = pd.merge(left=df, right=df_perf2,
                         on=['project', 'commit_hash', 'method_name'], how='inner')

    print('all left right left+right inner')
    print(len(df_joined_outer.index), len(df_disjoint_left.index), len(df_disjoint_right),
          len(df_disjoint_both.index), len(df_joined))
    df_joined.to_csv('results/' + project_name + '-perf-diff-all.csv')
    df_joined_cd_perf = df_joined
    df_joined_cd_perf.loc[df['will_change'] == 0, 'perf_change'] = 0
    df_joined_cd_perf.to_csv('results/' + project_name + '-cd-perf-diff-all.csv')
print('end.')
