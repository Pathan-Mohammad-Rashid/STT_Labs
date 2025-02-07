
from pydriller import Repository
import csv

# Define repository URL (change this to your selected repository)
repo_url = "https://github.com/encode/django-rest-framework"  # Replace with your repo URL

# Output CSV file
output_file = "analysis.csv"

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "old_file_path", "new_file_path", "commit_sha",
        "parent_commit_sha", "commit_message", "diff_histogram"
    ])

    # Counter to limit to the last 500 non-merge commits
    commit_count = 0

    # Iterate through the commits in reverse order (most recent first)
    for commit in Repository(repo_url, order="reverse").traverse_commits():
        if len(commit.parents) > 1:  # Ignore merge commits
            continue

        if commit_count >= 500:
            break

        for modified_file in commit.modified_files:
            # Get the diff using Myers algorithm (default)
            # diff_myers = modified_file.diff

            # Get the diff using Histogram algorithm
            diff_histogram = modified_file.diff_parsed

            # Write the data to CSV
            writer.writerow([
                modified_file.old_path, modified_file.new_path,
                commit.hash, commit.parents[0] if commit.parents else 'N/A',
                commit.msg, diff_histogram
            ])

        commit_count += 1

print(f"Analysis complete! Results saved in {output_file}")