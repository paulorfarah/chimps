import re
import pandas as pd

def format_method(row):
    method_name = row['Name']
    m = re.search('\([a-zA-Z0-9\._,\[\]<>]+\)$', method_name)
    if m:
        params = []
        p = re.findall('[a-zA-Z0-9\._\[\]<>]+,|[a-zA-Z0-9\._\[\]<>]+\)', m.group(0))
        for param in p:
            last = param.rsplit('.', 1)[-1]
            tag = re.findall('<[a-zA-Z0-9\._\[\]]+>', last)
            for t in tag:
                last = last.replace(t, '')

            params.append(last.replace(',', '').replace(')', ''))
        method_name = re.sub('\([a-zA-Z0-9\._,\[\]<>]+\)$', '(' + ','.join(params) + ')', method_name)
    method_name = method_name.replace('$', '.')
    return method_name

def join_understand(project_name, current_hash):
    # print("Understand ")
    csv_path = '../2.understand/' + project_name + '/' + current_hash + '.csv'

    # understandRepo = pydriller.Git(csvPathUndestand)
    metrics = ["Kind", "Name", "File", "AvgCyclomatic", "AvgCyclomaticModified", "AvgCyclomaticStrict",
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

    df = pd.read_csv(csv_path, usecols=metrics, sep=',', engine='python', index_col=False)
    # df = df.dropna()
    df_methods = df[df['Kind'].str.contains("Method")]
    df_constructors = df[df['Kind'].str.contains("Constructor")]

    df_filtered = pd.concat([df_methods, df_constructors])
    if len(df.index):
        df_filtered['method_name'] = df.apply(format_method, axis=1)
    # print(df_filtered.shape[0])
    return df_filtered
