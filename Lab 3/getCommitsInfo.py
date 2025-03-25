# import sys
# import csv
# from pydriller import Repository
# from pydriller.metrics.process.code_churn import CodeChurn
# from pydriller.metrics.process.commits_count import CommitsCount
# from pydriller.metrics.process.hunks_count import HunksCount

# columns = ['SHA','Message','Diff']

# rows = []
# count=0
# last_n=100

# commits = []
# for x in Repository(sys.argv[1],only_no_merge=True,order='reverse').traverse_commits():
#   if (x.in_main_branch==True):
#     count=count+1
#     commits.append(x)
#     if count == last_n:
#       break

# in_order = []
# for value in range(len(commits)):
#   in_order.append(commits.pop())

# commits=in_order
# i=-1
# for commit in commits:
#   i+=1
#   print('[{}/{}] Mining commit {}.{}'.format(i+1,len(commits),sys.argv[1],commit.hash))
#   diff = []
#   for m in commit.modified_files:
#     diff.append(m.diff_parsed)
      
#   if (i>=1):   
#     rows.append([commit.hash,commit.msg,diff])
#   elif (i==0):
#     rows.append([commit.hash,commit.msg,''])
       
# with open(sys.argv[1]+'_results/commits_info.csv', 'a') as csvFile:
#   writer = csv.writer(csvFile)
#   writer.writerow(columns)
#   writer.writerows(rows)



import sys
import csv
import os
from pydriller import Repository

def process_commits(repo_path, last_n=500, diff_algo='histogram'):
    """
    Traverses the repository commits (non-merge, main branch only) using a specified diff algorithm.
    For each modified file in a commit, collects:
      - commit SHA
      - parent commit SHA (first parent if available)
      - commit message
      - old file path
      - new file path
      - diff output (as parsed by pydriller)
      - file index (to help align multiple modifications per commit)
    """
    results = []
    count = 0
    # order='reverse' gives commits in chronological order.
    for commit in Repository(repo_path, only_no_merge=True, order='reverse', diff_algo=diff_algo).traverse_commits():
        if commit.in_main_branch:
            count += 1
            parent_sha = commit.parents[0] if commit.parents else ''
            for idx, mod in enumerate(commit.modified_files):
                results.append({
                    'commit': commit.hash,
                    'parent': parent_sha,
                    'message': commit.msg,
                    'old_path': mod.old_path,
                    'new_path': mod.new_path,
                    'file_index': idx,
                    'diff': mod.diff_parsed  # diff parsed output
                })
            if count == last_n:
                break
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python getCommitsInfo_updated.py <repo_path>")
        sys.exit(1)
    repo_path = sys.argv[1]
    
    # Create results directory if not present
    output_dir = repo_path + '_results'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("Processing histogram diff for 500 commits...")
    results_hist = process_commits(repo_path, last_n=500, diff_algo='histogram')

    print("Processing Myers diff for 500 commits...")
    results_myers = process_commits(repo_path, last_n=500, diff_algo='myers')

    # Build a lookup dictionary for Myers results keyed by (commit, file_index)
    myers_dict = {(item['commit'], item['file_index']): item for item in results_myers}

    combined_rows = []
    # CSV columns:
    # old_file_path, new_file_path, commit_SHA, parent_commit_SHA, commit_message,
    # diff_myers, diff_hist, Matches
    for item in results_hist:
        key = (item['commit'], item['file_index'])
        myers_item = myers_dict.get(key)
        diff_myers = myers_item['diff'] if myers_item else ''
        diff_hist = item['diff']
        # Compare diffs ignoring all whitespace differences
        if "".join(diff_myers.split()) == "".join(diff_hist.split()):
            match = "Yes"
        else:
            match = "No"
        combined_rows.append([
            item['old_path'],
            item['new_path'],
            item['commit'],
            item['parent'],
            item['message'],
            diff_myers,
            diff_hist,
            match
        ])

    # Write output CSV
    columns = ['old_file_path', 'new_file_path', 'commit_SHA', 'parent_commit_SHA', 'commit_message', 'diff_myers', 'diff_hist', 'Matches']
    csv_file_path = os.path.join(output_dir, 'diff_comparison.csv')
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(columns)
        writer.writerows(combined_rows)

    print("Dataset generated at: " + csv_file_path)

if __name__ == "__main__":
    main()
