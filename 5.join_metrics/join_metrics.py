import argparse

import git
import numpy as np
import pandas as pd
import pydriller

from change_distiller import join_change_distiller
from ck import join_ck
from evo import join_evo
from understand import join_understand

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description='Join Metrics')
    # args = ap.parse_args()

    projects = ['Openfire']
    for project_name in projects:
        repo_path = "repos/" + project_name
        gr = pydriller.Git(repo_path)
        repo = git.Repo(repo_path)
        tags = repo.tags
        release = 1
        merge_type = 'inner'

        csv_results = 'results/' + project_name + '-all-releases-' + merge_type + '.csv'

        # f = open(csvPath, "w")
        # writer = csv.writer(f)
        missing = []
        # for tag in tags:
        #     current_hash = gr.get_commit_from_tag(tag.name).hash
        commits = []
        for tag in tags:
            try:
                hash = gr.get_commit_from_tag(tag.name).hash

                # if hash == '0bde7625668738bdee0e48f5fcb821ed91a71ec2': #retirar essa linha
                commit = [tag.name, hash, tag.commit.committed_date]
                commits.append(commit)

            except:
                print(tag)
        df = pd.DataFrame(commits, columns=['Tag', 'Hash', 'Commiter_date'])
        df = df.sort_values(by=['Commiter_date', 'Tag'])

        releases = df['Hash']
        for current_hash in releases:
            print(current_hash)
            # if current_hash.startswith('c0f26'):
            #     print('here')

            try:
                df_ck = join_ck(project_name, current_hash)
                if len(df_ck.index):
                    df_joined = df_ck
                    df_joined['commit'] = current_hash

                    # df_joined = join_understand(project_name, current_hash)
                    und = join_understand(project_name, current_hash)
                    df_joined_outer = pd.merge(left=df_joined, right=und, on='method_name', how='outer', indicator=True)
                    df_disjoint_left = df_joined_outer.query('_merge == "left_only"')[['method_name', 'Name', '_merge']]
                    df_disjoint_right = df_joined_outer.query('_merge == "right_only"')[['method_name', 'Name', '_merge']]
                    df_disjoint_both = df_joined_outer.query('_merge != "both"')[['method_name', 'Name', '_merge']]
                    if len(und.index) and len(df_joined.index):
                        # df_joined = pd.merge(left=df_joined, right=und, on='method_name', how='inner')
                        df_joined = pd.merge(left=df_joined, right=und, on='method_name', how=merge_type)

                        # print(len(df_joined_outer.index), len(df_disjoint_left.index), len(df_disjoint_right), len(df_disjoint_both.index), len(df_joined_inner))
                        evo = join_evo(project_name, current_hash)
                        df_joined_outer = pd.merge(left=df_joined, right=evo, on='method_name', how='outer', indicator=True)
                        df_disjoint = df_joined_outer.query('_merge != "both"')[['method_name',  '_merge']]
                        df_disjoint_both = df_joined_outer.query('_merge != "both"')[['method_name', '_merge']]
                        df_disjoint_left = df_joined_outer.query('_merge == "left_only"')[['method_name', '_merge']]
                        df_disjoint_right = df_joined_outer.query('_merge == "right_only"')[['method_name','_merge']]
                        if len(evo.index) and len(df_joined.index):
                            # df_joined = pd.merge(left=df_joined, right=evo, on='method_name', how='inner')
                            df_joined = pd.merge(left=df_joined, right=evo, on='method_name', how=merge_type)
                            print('evo: all left right left+right inner')
                            print(len(df_joined_outer.index), len(df_disjoint_left.index), len(df_disjoint_right),
                                  len(df_disjoint_both.index), len(df_joined))

                            # print(len(df_joined_outer.index), len(df_disjoint_left.index), len(df_disjoint_right),
                            #       len(df_disjoint_both.index), len(df_joined))

                            # smells = join_smells(project_name, current_hash)
                            # df_joined = pd.merge(left=df_joined, right=smells, left_on='class', right_on='fullyQualifiedName')

                            # merged_full = pd.merge(left=ck_understand_process_organic, right=releaseChangeDistillerMetrics,
                            #                        left_on='class', right_on='CLASS_PREVIOUSCOMMIT')

                            change_distiller = join_change_distiller(project_name, current_hash)
                            if len(change_distiller.index) and len(df_joined.index):
                                df_joined_outer = pd.merge(left=df_joined, right=change_distiller, on='method_name', how='outer',
                                                       indicator=True)
                                df_disjoint = df_joined_outer.query('_merge != "both"')[['method_name', '_merge']]
                                df_disjoint_both = df_joined_outer.query('_merge != "both"')[['method_name', '_merge']]
                                df_disjoint_right = df_joined_outer.query('_merge == "right_only"')[['method_name', '_merge']]
                                df_disjoint_left = df_joined_outer.query('_merge == "left_only"')[['method_name', '_merge']]
                                # df_joined = pd.merge(left=df_joined, right=change_distiller, on='method_name', how='inner')
                                df_joined = pd.merge(left=df_joined, right=change_distiller, on='method_name',
                                                     how=merge_type)

                                print('cd: all left right left+right inner')
                                print(len(df_joined_outer.index), len(df_disjoint_left.index), len(df_disjoint_right),
                                      len(df_disjoint_both.index), len(df_joined))
                                # listclass.list(String)

                                if len(df_joined.index):
                                    # df_joined.loc[:,'class_frequency'] = 1
                                    df_joined.loc[:, 'will_change'] = 0
                                    # df_joined.loc[:,'number_of_changes'] = 0
                                    df_joined.loc[:, 'release'] = release
                                    medianChanges = df_joined['TOTAL_CHANGES'].median()
                                    df_joined['will_change'] = np.where(df_joined['TOTAL_CHANGES'] > medianChanges, 1, 0)
                                    if release == 1:
                                        df_joined.to_csv(csv_results, index=False)
                                    else:
                                        df_joined.to_csv(csv_results, mode="a", header=False, index=False)

                release += 1
            except Exception as e:
                print(e)
                # print(hashCurrent)
                missing.append(current_hash)

        print(missing)
