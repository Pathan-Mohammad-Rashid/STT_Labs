import sys
import csv
from pydriller import Repository
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller.metrics.process.commits_count import CommitsCount
from pydriller.metrics.process.hunks_count import HunksCount

columns = ['SHA','Message','Diff']

rows = []
count=0
last_n=100

commits = []
for x in Repository(sys.argv[1],only_no_merge=True,order='reverse').traverse_commits():
  if (x.in_main_branch==True):
    count=count+1
    commits.append(x)
    if count == last_n:
      break

in_order = []
for value in range(len(commits)):
  in_order.append(commits.pop())

commits=in_order
i=-1
for commit in commits:
  i+=1
  print('[{}/{}] Mining commit {}.{}'.format(i+1,len(commits),sys.argv[1],commit.hash))
  diff = []
  for m in commit.modified_files:
    diff.append(m.diff_parsed)
      
  if (i>=1):   
    rows.append([commit.hash,commit.msg,diff])
  elif (i==0):
    rows.append([commit.hash,commit.msg,''])
       
with open(sys.argv[1]+'_results/commits_info.csv', 'a') as csvFile:
  writer = csv.writer(csvFile)
  writer.writerow(columns)
  writer.writerows(rows)
