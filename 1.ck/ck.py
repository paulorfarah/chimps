import pandas as pd
import pydriller
import git
import csv
if __name__ == "__main__":
    # ap = argparse.ArgumentParser(description='Join Metrics')
    # args = ap.parse_args()

    res = []

    projects = ['wro4j']
    for project_name in projects:
        repo_path = project_name
        gr = pydriller.Git(repo_path)
        repo = git.Repo(repo_path)
        tags = repo.tags
        release = 1

        csv_results = 'results/' + project_name + '-all-releases.csv'

        # f = open(csvPath, "w")
        # writer = csv.writer(f)
        missing = []

        commits = []
        for tag in tags:
            hash = gr.get_commit_from_tag(tag.name).hash
            # print(tag.name, hash, tag.commit.committed_date)
            commit = [tag.name, hash, tag.commit.committed_date]
            if commit not in commits:
                commits.append(commit)
        df = pd.DataFrame(commits, columns=['Tag', 'Hash', 'Commiter_date'])
        df = df.sort_values(by=['Commiter_date', 'Tag'])
        releases = df['Hash'].drop_duplicates()

        # for tag in tags:
        #     current_hash = gr.get_commit_from_tag(tag.name).hash
        for current_release in releases:
            # print(current_release)
            res.append([current_release])

        # opening the csv file in 'w+' mode
        file = open(project_name + '.csv', 'w+', newline='')

        # writing the data into the file
        with file:
            write = csv.writer(file)
            write.writerows(res)
