import filecmp
import os
import subprocess
import sys
from asyncore import write
from os import listdir
from os.path import isfile, join

import myers as myers
import pandas as pd
import pydriller
import argparse
from csv import reader
import csv
from pydriller import Repository
import git


def read_method_files(hash, file, methods_path):
    subprocess.call([args.java, '-jar',
                     'JMethodsExtractor-0.0.1-SNAPSHOT-jar-with-dependencies.jar', 'file', file,
                     hash])
    method_files = None
    try:
        method_files = [mf for mf in listdir(methods_path) if isfile(join(methods_path, mf))]
    except FileNotFoundError:
        pass
        # print('[>>>FileNotFound]: Check if class has methods:')
        # if methods_path:
        #     print(methods_path)
    except:
        print('[>>>Error]: extracting methods: ' + str(sys.exc_info()))
    return method_files


def read_nloc(commit_methods_path_A, commit_method_file_A):
    nloc = 0
    try:
        with open(commit_methods_path_A + '/' + commit_method_file_A, 'r') as cmp:
            nloc = len(cmp.readlines())
    except:
        print('Error reading nloc: ' + commit_method_file_A)
        print(sys.exc_info())
    return nloc


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description='Extract process metrics')
    ap.add_argument('--pathA', required=True)
    ap.add_argument('--pathB', required=True)
    ap.add_argument('--project_name', required=True)
    ap.add_argument('--java', required=True)
    args = ap.parse_args()

    project = args.project_name
    # folder with repo: projectA and projectB

    path_A = pydriller.Git(args.pathA)
    path_B = pydriller.Git(args.pathB)

    # tags
    repo = git.Repo(args.pathA)
    tags = repo.tags

    release = 1
    bom_list = {}
    fch_list = {}
    lch_list = {}
    tach_list = {}
    chd_list = {}

    frchArray = {}
    wcdArray = {}
    wfrArray = {}
    lcaArray = {}
    lcdArray = {}
    csbArray = {}
    csbsArray = {}
    acdfArray = {}

    absolute_path = os.getcwd() + '/'
    csv_path = absolute_path + "results/" + args.project_name + "-methods-results-processMetrics.csv"
    f = open(csv_path, "w")
    writer = csv.writer(f)

    commits = []
    for tag in tags:
        try:
            hash = path_A.get_commit_from_tag(tag.name).hash
            # print(tag.name, hash, tag.commit.committed_date)
            commit = [tag.name, hash, tag.commit.committed_date]
            if commit not in commits:
                commits.append(commit)
        except:
            print(tag)
    df = pd.DataFrame(commits, columns=['Tag', 'Hash', 'Commiter_date'])
    df = df.sort_values(by=['Commiter_date', 'Tag'])
    releases = df['Hash'].drop_duplicates()

    previous_release = None
    # for tag in tags:
    #     current_release = path_A.get_commit_from_tag(tag.name).hash
    for current_release in releases:
        print(current_release, tag.name)
        path_A.checkout(current_release)
        files = path_A.files()
        files = [x for x in files if x.endswith('.java')]

        if release == 1:
            header = ['project', 'commit', 'commitprevious', 'release', 'file', 'method', 'BOM', 'TACH', 'FCH', 'LCH',
                      'CHO', 'FRCH', 'CHD', 'WCH', 'WCD', 'WFR', 'ATAF', 'LCA', 'LCD', 'CSB', 'CSBS', 'ACDF']
            writer.writerow(header)

            # Birth of the first methods (BOM)
            for file in files:
                # '/usr/lib/jvm/java-19-openjdk-amd64/bin/java'
                methods_path_A = 'results/' + current_release + file
                method_files_A = read_method_files(current_release, file, methods_path_A)
                if method_files_A:
                    for method_file in method_files_A:
                        method_file_A = methods_path_A + '/' + method_file
                        method_short_name = method_file_A.split(args.pathA, 1)[1].replace('.java', '')
                        if method_short_name not in bom_list:
                            bom_list[method_short_name] = release
                            nloc = read_nloc(methods_path_A, method_file)
                            csbsArray[method_short_name] = nloc

                            row = [args.project_name, current_release, '', release, file, method_short_name, release, 0,
                                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                            writer.writerow(row)
        else:
            # release > 1
            # print('prev: ' + previous_release)
            bom = release
            tach = 0
            fch = 0
            lch = 0
            cho = 0
            frch = 0
            chd = 0
            wch = 0
            wcd = 0
            wfr = 0
            ataf = 0
            lca = 0
            lcd = 0
            csb = 0
            csbs = 0
            acdf = 0

            commits_between_releases = Repository(args.pathA, from_commit=previous_release,
                                                  to_commit=current_release).traverse_commits()

            # calculate the birth of methods
            for file in files:
                file_short_name = file.split(args.pathA + '/', 1)[1]
                methods_path_A = 'results/' + current_release + file
                method_files_A = read_method_files(current_release, file, methods_path_A)

                # search for methods that appear for the first time (Birth of Method)
                if method_files_A:
                    cho_list = {}
                    for method_file in method_files_A:
                        method_file_A = methods_path_A + '/' + method_file
                        method_short_name = method_file_A.split(args.pathA, 1)[1].replace('.java', '')

                        # if method_short_name == '/src/test/resources/Java8Example/hello()':
                            # print(release)
                            # print(current_release)

                        if method_short_name not in bom_list:
                            bom = release
                            bom_list[method_short_name] = bom
                        else:
                            bom = bom_list.get(method_short_name)
                        if method_short_name not in fch_list:
                            fch_list[method_short_name] = 0
                        if method_short_name not in frchArray:
                            frchArray[method_short_name] = 0
                        if method_short_name not in wcdArray:
                            wcdArray[method_short_name] = 0
                        if method_short_name not in wfrArray:
                            wfrArray[method_short_name] = 0
                        if method_short_name not in lcaArray:
                            lcaArray[method_short_name] = 0
                        if method_short_name not in lcdArray:
                            lcdArray[method_short_name] = 0
                        if method_short_name not in csbArray:
                            csbArray[method_short_name] = 0
                        if method_short_name not in csbsArray:
                            nloc = read_nloc(methods_path_A, method_file)
                            csbsArray[method_short_name] = nloc
                        if method_short_name not in acdfArray:
                            acdfArray[method_short_name] = 0
                        if method_short_name not in cho_list:
                            cho_list[method_short_name] = 0
                        if method_short_name not in tach_list:
                            tach_list[method_short_name] = [0]
                        else:
                            tach_list[method_short_name].append(0)
                        if method_short_name not in chd_list:
                            chd_list[method_short_name] = []
                        if method_short_name not in lch_list:
                            lch_list[method_short_name] = 0

                        # work with modified methods

                        added_lines = 0
                        deleted_lines = 0
                        loc = 0
                        previous_commit = None
                        for current_commit in commits_between_releases:
                            # print('comm: ' + current_commit.hash)

                            if not previous_commit:
                                # first commit
                                previous_commit = current_commit

                            else:
                                path_A.checkout(current_commit.hash)
                                path_B.checkout(previous_commit.hash)

                                # modified_files = [x for x in current_commit.modified_files if x.filename.endswith('.java')]
                                try:
                                    modified_files = [x for x in current_commit.modified_files if x.filename.endswith('.java') and
                                                  (x.new_path == file_short_name or x.old_path == file_short_name)]
                                except ValueError:
                                    modified_files = []
                                # previous_files = pathB.files()

                                for modified_file in modified_files:
                                    # print(modified_file.filename)

                                    current_commit_hash = current_commit.hash
                                    current_commit_path = str(path_A.path) + '/' + str(modified_file.new_path)
                                    commit_methods_path_A = 'results/' + current_commit.hash + current_commit_path

                                    commit_method_files_A = read_method_files(current_commit_hash, current_commit_path,
                                                                              commit_methods_path_A)

                                    if modified_file.new_path and modified_file.old_path:
                                        # print('modify: ' + modified_file.new_path + ' ' + modified_file.old_path)

                                        previous_commit_hash = previous_commit.hash
                                        previous_commit_path = str(path_B.path) + '/' + str(modified_file.old_path)
                                        commit_methods_path_B = 'results/' + previous_commit_hash + previous_commit_path

                                        commit_method_files_B = read_method_files(previous_commit_hash,
                                                                                  previous_commit_path,
                                                                                  commit_methods_path_B)

                                        result = filecmp.dircmp(commit_methods_path_A, commit_methods_path_B)
                                        # print(result.report())

                                        # new methods
                                        for new_method in result.left_only:
                                            nloc = read_nloc(commit_methods_path_A, new_method)
                                            commit_method_file_A_renamed = commit_methods_path_A + '/' + new_method
                                            commit_method_short_name = \
                                                commit_method_file_A_renamed.split(args.pathA, 1)[1].replace('.java',
                                                                                                             '')
                                            csbsArray[commit_method_short_name] = nloc

                                        # modified methods
                                        for modified_method in result.diff_files:
                                            # 'printFlags(int, int).java'
                                            # print(modified_method)
                                            # loc = modified_file.nloc
                                            loc = read_nloc(result.left, modified_method)

                                            with open(result.left + '/' + modified_method) as lf:
                                                cur_method_file = lf.readlines()
                                                with open(result.right + '/' + modified_method) as lr:
                                                    prev_method_file = lr.readlines()
                                                    diff = myers.diff(prev_method_file, cur_method_file)
                                                    for d in diff:
                                                        if d[0] == 'i':
                                                            added_lines += 1
                                                        elif d[0] == 'r':
                                                            deleted_lines += 1

                                            # first time change
                                            if fch_list[method_short_name] == 0:
                                                fch_list[method_short_name] = release
                                                fch = release

                                            # last time change, the lastest released analayzed
                                            # lch = release

                                            lch_list[method_short_name] = release
                                            # if changes have occurred
                                            cho_list[method_short_name] = 1
                                            # frequency of change
                                            frchArray[method_short_name] += 1
                                            frch = frchArray[method_short_name]

                                    elif modified_file.new_path:
                                        # print('new: ' + modified_file.new_path)
                                        # commit_method_files_A = read_method_files(current_commit.hash, modified_file.new_path,
                                        #                                    commit_methods_path_A)
                                        if commit_method_files_A:
                                            for commit_method_file_A in commit_method_files_A:
                                                nloc = read_nloc(commit_methods_path_A, commit_method_file_A)
                                                commit_method_file_A_renamed = commit_methods_path_A + '/' + commit_method_file_A
                                                commit_method_short_name = \
                                                    commit_method_file_A_renamed.split(args.pathA, 1)[1].replace(
                                                        '.java', '')
                                                csbsArray[commit_method_short_name] = nloc

                                    # elif modified_file.old_path:
                                    #     print('old: ' + modified_file.old_path)
                            previous_commit = current_commit

                        # total amount change, added lines + deleted lines (changed lines are already counted twice )
                        tach = added_lines + deleted_lines
                        tach_list[method_short_name][-1] = tach
                        if tach > 0:
                            chd = tach / loc
                            # cumulative weight of change
                            wcdArray[method_short_name] += tach * pow(2, bom - release)
                            # sum of change density, to normalize later
                            # acdfArray[method_short_name] += chd
                            # agregate change size, normalized by frequency change
                            if frch > 0:
                                ataf = tach / frch
                                # agregate change density normalized by frch
                                # acdf = acdfArray[method_short_name] / frch
                            # else:
                            #     acdf = 0

                            # last amount of change
                            lcaArray[method_short_name] = tach
                            # last change density
                            lcdArray[method_short_name] = chd
                            csbArray[method_short_name] += tach
                        else:
                            chd = 0
                            wcdArray[method_short_name] += 0

                        # sum of change density, to normalize later
                        acdfArray[method_short_name] += chd
                        # agregate change size, normalized by frequency change
                        if frch > 0:
                            # agregate change density normalized by frch
                            acdf = acdfArray[method_short_name] / frch
                        else:
                            acdf = 0

                        wch = 0
                        i = 0
                        n = release
                        for j in range(bom, n):
                            r = j + 1
                            try:
                                tach_r = tach_list[method_short_name][i]
                            except:
                                print(bom)
                            wch += tach_r * pow(2, r - n)
                            i += 1

                        chd_list[method_short_name].append(chd)

                        wcd = 0
                        i = 0
                        for j in range(bom, n):
                            r = j + 1
                            try:
                                chd_r = chd_list[method_short_name][i]
                            except:
                                print(bom)
                            wcd += chd_r * pow(2, r - n)
                            i += 1

                        # cumulative weight frequency
                        wfrArray[method_short_name] += (release - 1) * cho_list[method_short_name]
                        wfr = wfrArray[method_short_name]
                        lca = lcaArray[method_short_name]
                        lcd = lcdArray[method_short_name]
                        csb = csbArray[method_short_name]
                        cho = cho_list[method_short_name]
                        fch = fch_list[method_short_name]
                        lch = lch_list[method_short_name]
                        if csb > 0 and csbsArray[method_short_name] > 0:
                            csbs = csb / csbsArray[method_short_name]
                        else:
                            csbs = 0
                        row = [args.project_name, current_release, previous_release, release, file, method_short_name,
                               bom,
                               tach, fch, lch, cho, frch, chd, wch, wcd, wfr, ataf, lca, lcd, csb, csbs, acdf]
                        writer.writerow(row)

            # put 0 in methods that not changed
            for k, v in tach_list.items():
                if len(tach_list[k]) < release - bom_list[k]:
                    tach_list[k].append(0)

            for k, v in chd_list.items():
                if len(chd_list[k]) < release - bom_list[k]:
                    chd_list[k].append(0)

        # print('curr: ' + current_release)
        # print('--------')
        previous_release = current_release
        release += 1
    f.close()
