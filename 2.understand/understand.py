import argparse

import pydriller
import shutil
import subprocess
import os
import time
import sys


def check(chash):
    if os.path.exists(chash + '.csv'):
        print("Commit", chash, "already collected, skipping...")
        return True
    else:
        print("Commit", chash, "not found, collecting...")
        return False

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description='Extractor for changeDistiller')
    ap.add_argument('--project', required=True)
    args = ap.parse_args()
    with open('commits-' + args.project + '.csv') as f:
        commits = f.read().splitlines()
    gr = pydriller.Git(args.project)
    # commits = ['73a432514936fcee1386b37a0d60dcd913706bd1', 'e7142a3937825074ec68e4bacba30f9c962bd1e4',
    #            'df479df17676148bf6391401a704a7d7265c45fa', '399d2929ee0912bfeda8a4ef125f1b96bb7fd144',
    #            'f3b8653021830d8a503c5e7a9d33cb82b16db739', 'f2c58503d76be1dfb8072f6a7d592f88133708e1',
    #            '41b194c718d50763a79951029787cca70a5804a5', '1447159b926076c9222a96b3abbe17571953a74f',
    #            '4f0daa3bb2a5fa28286f1973deb9d13996cc73cc', 'bf32c9102fb1b5fdfa7a26a120b5d9a6b428dd2f']

    # for commit in gr.get_list_commits():
    #     commits.append(commit.hash)

    for commit in commits:
        if check(commit):
            continue

        gr.clear()
        print("git checkout on commit", commit + "...")
        gr.checkout(commit)
        if os.path.exists(commit + '.und'):
            print("deleting possibly corrupt project files...")
            shutil.rmtree(commit + '.und')
        print("creating the project", commit + ".udb ...")
        subprocess.run(['und', 'create', '-db', commit + '.und', '-languages', 'java'])
        os.makedirs(commit + '.und/local')
        print("adding java files to project...")
        subprocess.run(['und', '-db', commit + '.und', 'add', '.'])
        print("analyzing source code for commit", commit + "...")
        subprocess.run(['und', 'analyze', '-db', commit + '.und'])
        print("adding the metrics to the project and setting up the environment...")
        subprocess.run(
            ['und', 'settings', '-metricmetricsAdd', 'AvgCyclomatic', 'AvgCyclomaticModified', 'AvgCyclomaticStrict',
             'AvgEssential', 'AvgLine', 'AvgLineBlank', 'AvgLineCode', 'AvgLineComment', 'CountClassBase',
             'CountClassCoupled', 'CountClassDerived', 'CountDeclClass', 'CountDeclClassMethod',
             'CountDeclClassVariable', 'CountDeclFile', 'CountDeclFunction', 'CountDeclInstanceMethod',
             'CountDeclInstanceVariable', 'CountDeclMethod', 'CountDeclMethodAll', 'CountDeclMethodDefault',
             'CountDeclMethodPrivate', 'CountDeclMethodProtected', 'CountDeclMethodPublic', 'CountInput',
             'CountLine', 'CountLineBlank', 'CountLineCode', 'CountLineCodeDecl', 'CountLineCodeExe',
             'CountLineComment', 'CountOutput', 'CountPath', 'CountSemicolon', 'CountStmt', 'CountStmtDecl',
             'CountStmtExe', 'Cyclomatic', 'CyclomaticModified', 'CyclomaticStrict', 'Essential',
             'MaxCyclomatic', 'MaxCyclomaticModified', 'MaxCyclomaticStrict', 'MaxEssential',
             'MaxInheritanceTree', 'MaxNesting', 'PercentLackOfCohesion', 'RatioCommentToCode', 'SumCyclomatic',
             'SumCyclomaticModified', 'SumCyclomaticStrict', 'SumEssential', commit + '.und'])
        subprocess.run(['und', 'settings', '-MetricFileNameDisplayMode', 'RelativePath', commit + '.und'])
        subprocess.run(['und', 'settings', '-MetricDeclaredInFileDisplayMode', 'RelativePath', commit + '.und'])
        subprocess.run(['und', 'settings', '-MetricShowDeclaredInFile', 'on', commit + '.und'])
        subprocess.run(['und', 'settings', '-MetricShowFunctionParameterTypes', 'on', commit + '.und'])
        print("calculating metrics for", commit + "...")
        subprocess.run(['und', 'metrics', commit + '.und'])
        print("deleting", commit + '.und')
        if os.path.exists(commit + '.und'):
            shutil.rmtree(commit + '.und')
        if os.path.exists("/home/usuario/.local/share/Scitools/Db/"+commit):
            shutil.rmtree("/home/usuario/.local/share/Scitools/Db/"+commit)
        print("resetting repository", commit + "...")
        try:
            gr.reset()
        except:
            print(sys.exc_info())
        print("waiting for 3 seconds, it is safe to ctrl+c here...", flush=True)
        for i in range(300):
            time.sleep(0.01)