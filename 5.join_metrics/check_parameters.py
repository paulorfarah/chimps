import re
import pydriller
import git
import pandas as pd

params_list = {}

def extract_params(row):
    params = []
    method_name = row['Name']
    m = re.search('\([a-zA-Z0-9\._,\[\]]+\)$', method_name)
    if m:
        p = re.findall('[a-zA-Z0-9\._\[\]]+,|[a-zA-Z0-9\._\[\]]+\)', m.group(0))
        for param in p:
            param = param.replace(',', '').replace(')', '')
            last = param.rsplit('.', 1)[-1]
            if last not in params_list:
                params_list[last] = [param]
            else:
                if last not in params_list[param]:
                    params_list[last].append(param)


if __name__ == "__main__":
    projects = ['commons-bcel']
    for project_name in projects:
        repo_path = "repos/" + project_name
        gr = pydriller.Git(repo_path)
        repo = git.Repo(repo_path)
        tags = repo.tags
        release = 1

        csv_results = 'results/' + project_name + '-all-releases.csv'

        # f = open(csvPath, "w")
        # writer = csv.writer(f)
        missing = []
        parameters = {}

        for tag in tags:
            current_hash = gr.get_commit_from_tag(tag.name).hash
            csv_path = '../2.understand/results/' + project_name + '/' + current_hash + '.csv'
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
            df = None
            try:
                df = pd.read_csv(csv_path, usecols=metrics, sep=',', engine='python', index_col=False)
                df_methods = df[df['Kind'].str.contains("Method")]
                df_constructors = df[df['Kind'].str.contains("Constructor")]

                df_filtered = pd.concat([df_methods, df_constructors])

                for index, row in df.iterrows():
                    extract_params(row)
            except:
                print(csv_path)

        for k, v in params_list.items():
            print(k + ": " + str(v))
