import os
import sys

import pandas as pd
import pydriller
import argparse
from csv import reader
import shutil
import subprocess

import git
from os import listdir
from os.path import isfile, join


def transform_method_to_class(method_file):
    code = []
    file_name = method_file.replace('(', '_').replace(')', '_').replace(' ', '').replace(',', '_').replace('[',
                                                                                                           '_').replace(
        ']', '')

    class_sig = 'public class Fake_function_qwerty {'
    with open(method_file, 'r') as f:
        code = f.readlines()
        if not code[0].startswith(class_sig):
            code.insert(0, class_sig)
            code.append('}')
    with open(file_name, 'w') as fw:
        fw.writelines(code)
    return file_name


def compare_classes(java, pathA, pathB, currentCommit, previousCommit):
    filesA = pathA.files()
    filesB = pathB.files()
    filesA = [x for x in filesA if x.endswith('.java')]
    filesB = [x for x in filesB if x.endswith('.java')]
    csvPath = absolute_path + 'results/' + args.project_name + "-cd-methods-results.csv"
    try:
        f = open(csvPath, "x")
    except FileExistsError:
        print('File already exists: ' + csvPath)
        # print("file exists")
        print(sys.exc_info())
    for file in filesA:
        file_temp = file.replace(absolute_path + "projectA", '')
        if any(file_temp in s for s in filesB):
            file2 = absolute_path + "projectB" + file_temp
            # classPreviousCommit classCurrentCommit csvPath projectName currentCommit previousCommit

            subprocess.call([java, '-jar',
                             'JMethodsExtractor-0.0.1-SNAPSHOT-jar-with-dependencies.jar', 'file', file, currentCommit])
            subprocess.call([java, '-jar',
                             'JMethodsExtractor-0.0.1-SNAPSHOT-jar-with-dependencies.jar', 'file', file2,
                             previousCommit])

            methods_path_A = 'results/' + currentCommit + file
            methods_path_B = 'results/' + previousCommit + file2
            method_files_A = None
            method_files_B = None
            try:
                method_files_A = [f for f in listdir(methods_path_A) if isfile(join(methods_path_A, f))]
            except FileNotFoundError:
                if method_files_A:
                    print('[>>>FileNotFound]: ' + methods_path_A + '! \n Check if class has methods...')
                else:
                    print('Error ind method_filesA: ' + str(sys.exc_info()))
            except:
                print('error reading files A: ' + str(sys.exc_info()))
            try:
                method_files_B = [f for f in listdir(methods_path_B) if isfile(join(methods_path_B, f))]
            except FileNotFoundError:
                if method_files_B:
                    print('[>>>FileNotFound]: ' + methods_path_B + '! \n Check if class has methods...')
                else:
                    print('Error ind method_filesB: ' + str(sys.exc_info()))
            except:
                print('error reading files B: ' + str(sys.exc_info()))

            if method_files_A and method_files_B:
                for method_file in method_files_A:
                    if any(method_file == f for f in method_files_B):
                        method_file_A = methods_path_A + '/' + method_file
                        method_file_B = methods_path_B + '/' + method_file

                        method_file_A_renamed = absolute_path + transform_method_to_class(method_file_A)
                        method_file_B_renamed = absolute_path + transform_method_to_class(method_file_B)
                        cd_cmd = '/usr/lib/jvm/java-8-openjdk-amd64/bin/java -jar ChangeDistillerReader-methods-0.0.1-SNAPSHOT-jar-with-dependencies.jar ' + method_file_A_renamed + ' ' + method_file_B_renamed + ' ' + csvPath + ' ' + args.project_name + ' ' + currentCommit + ' ' + previousCommit + ' ' + method_file_A + ' ' +method_file_B
                        # print(cd_cmd)
                        # subprocess.call(['java', '-jar', 'ChangeDistillerReader-0.0.1-SNAPSHOT-jar-with-dependencies.jar',
                        #                  '"' + method_file_B + '"', '"' + method_file_A + '"', csvPath, args.project_name, currentCommit, previousCommit])
                        res = subprocess.check_output((['/usr/lib/jvm/java-8-openjdk-amd64/bin/java', '-jar',
                                                        'ChangeDistillerReader-methods-0.0.1-SNAPSHOT-jar-with-dependencies.jar',
                                                        method_file_A_renamed, method_file_B_renamed, csvPath,
                                                        args.project_name, currentCommit, previousCommit, method_file_A, method_file_B]))

            elif method_files_A:
                print('files not found in previous path')
            else:
                print('files not found in current path')

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description='Extractor for changeDistiller')
    ap.add_argument('--pathA', required=True)
    ap.add_argument('--pathB', required=True)
    ap.add_argument('--project_name', required=True)
    # ap.add_argument('--absolute_path', required=True)
    ap.add_argument('--java', required=True)
    args = ap.parse_args()

    absolute_path = os.getcwd() + '/'
    pathA = pydriller.Git(args.pathA)
    pathB = pydriller.Git(args.pathB)
    repo = git.Repo(args.pathA)
    tags = repo.tags

    commits = []
    for tag in tags:
        try:
            hash = pathA.get_commit_from_tag(tag.name).hash
            commit = [tag.name, hash, tag.commit.committed_date]
            commits.append(commit)
        except:
            print(tag)
    df = pd.DataFrame(commits, columns=['Tag', 'Hash', 'Commiter_date'])
    df = df.sort_values(by=['Commiter_date',  'Tag'])

    releases = df['Hash']
    prev_release = None
    for current_release in releases:
        print(current_release)
        if not prev_release:
            prev_release = current_release
        else:
            pathA.checkout(prev_release)
            pathB.checkout(current_release)
            compare_classes(args.java, pathA, pathB, str(prev_release), str(current_release))
            prev_release = current_release
