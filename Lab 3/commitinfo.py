from pydriller import Repository
import csv

repo_url = "https://github.com/tesseract-ocr/tesseract"

output_file = "analysisLab3.csv"

def compare_lists_line_by_line(list1, list2):
    for line1, line2 in zip(list1, list2):
        if line1 == line2:
            continue
        else:
            return False
    return True

def compare_diff_myers_and_histogram(diff_myers, diff_histogram):
    myers_added = [line[1:] for line in diff_myers.splitlines() if line.startswith('+')]
    myers_deleted = [line[1:] for line in diff_myers.splitlines() if line.startswith('-')]

    histogram_added = [line[1] for line in diff_histogram['added']]
    histogram_deleted = [line[1] for line in diff_histogram['deleted']]

    myers_added = [line for line in myers_added]
    histogram_added = [line for line in histogram_added]

    myers_deleted = [line for line in myers_deleted]
    histogram_deleted = [line for line in histogram_deleted]
    
    # added_equal = myers_added == histogram_added
    
    added_equal = compare_lists_line_by_line(myers_added, histogram_added)
    added_equal_deleted = compare_lists_line_by_line(myers_added, histogram_added)

    # print(myers_added, histogram_added, '\n')
    return "yes" if added_equal_deleted and added_equal else "no"

yes_count = 0
no_count = 0

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "old_file_path", "new_file_path", "commit_sha",
        "parent_commit_sha", "commit_message", "diff_myers", "diff_histogram", "diff_equal"
    ])

    commit_count = 0

    for commit in Repository(repo_url, order="reverse").traverse_commits():
        if len(commit.parents) > 1:
            continue

        if commit_count >= 500:
            break

        for modified_file in commit.modified_files:
            diff_myers = modified_file.diff
            diff_histogram = modified_file.diff_parsed

            diff_equal = compare_diff_myers_and_histogram(diff_myers, diff_histogram)

            # print (diff_equal)

            if diff_equal == "yes":
                yes_count += 1
            else:
                no_count += 1

            writer.writerow([
                modified_file.old_path, modified_file.new_path,
                commit.hash, commit.parents[0] if commit.parents else 'N/A',
                commit.msg, diff_myers, diff_histogram, diff_equal
            ])

        commit_count += 1

print(f"saved in {output_file}")
print(f"Total 'yes' count: {yes_count}")
print(f"Total 'no' count: {no_count}")