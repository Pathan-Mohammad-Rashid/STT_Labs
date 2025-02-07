import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Load dataset generated in previous steps
df = pd.read_csv("mcc_analysis.csv")

# Identify the top 3 frequently changed files
file_counts = Counter(df["new_path"].dropna())
top_3_files = file_counts.most_common(3)
print("Top 3 frequently changed files:", top_3_files)

# Select the most frequently changed file
most_changed_file = top_3_files[0][0]
print(f"Most frequently changed file: {most_changed_file}")

# Filter data for this file
df_file = df[df["new_path"] == most_changed_file]

# # Save to CSV for future reference
# df_file.to_csv("most_changed_file_data.csv", index=False)

# Load MCC dataset for the most frequently changed file
df = pd.read_csv("C:\\Users\\Rashid\\OneDrive\\Desktop\\STT\\Labs\\Lab_4\\cs202_miner\\most_changed_file_data.csv")

# Convert commit timestamp to datetime format
df["commit_SHA"] = df["commit_SHA"].astype(str)
df["old_MCC"] = df["old_MCC"].fillna(0).astype(int)
df["new_MCC"] = df["new_MCC"].fillna(0).astype(int)

# Sort by commit history (assumes chronological order)
df = df.sort_values(by="commit_SHA")

# Plot MCC changes over time
plt.figure(figsize=(12, 6))
plt.plot(df["commit_SHA"], df["old_MCC"], label="Old MCC", marker="o", linestyle="dashed")
plt.plot(df["commit_SHA"], df["new_MCC"], label="New MCC", marker="o", linestyle="-")
plt.xlabel("Commit SHA (truncated)")
plt.ylabel("Cyclomatic Complexity (MCC)")
plt.xticks(rotation=45, ha="right")
plt.title(f"MCC Evolution for {most_changed_file}")
plt.legend()
plt.grid()
plt.tight_layout()

# Save the figure
plt.savefig("mcc_timeline.png", dpi=300)
plt.show()
