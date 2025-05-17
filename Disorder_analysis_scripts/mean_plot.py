import pandas as pd
import matplotlib.pyplot as plt

# Load the TSV file that contains your data
df = pd.read_csv("/Users/tusharsingh/Documents/PY/idp_vdj/disorder_results_17409309014266422.tsv", sep="\t")  # Replace TIMESTAMP with your timestamp or filename part

def parse_scores(score_str):
    """Convert a comma-separated string of scores to a list of floats."""
    # If there is a possibility of invalid entries, you can add try/except here
    return [float(x) for x in score_str.split(',')]

# Calculate mean disorder for each CDR3 sequence
df['Mean_Disorder'] = df['Disorder_Scores'].apply(lambda s: sum(parse_scores(s)) / len(parse_scores(s)) 
                                                   if s != "No valid residues" else None)

# Count number of residues with disorder > 0.5 for each sequence
threshold = 0.5
df['Disordered_Residue_Count'] = df['Disorder_Scores'].apply(lambda s: sum(1 for score in parse_scores(s) if score > threshold)
                                                              if s != "No valid residues" else 0)

# Calculate the fraction of residues above the threshold
df['Fraction_Disordered'] = df.apply(lambda row: row['Disordered_Residue_Count'] / len(parse_scores(row['Disorder_Scores']))
                                     if row['Disorder_Scores'] != "No valid residues" else None, axis=1)

# Show some summary statistics
print("Summary of Mean Disorder Scores:")
print(df['Mean_Disorder'].describe())

print("\nSummary of Fraction Disordered:")
print(df['Fraction_Disordered'].describe())

# Visualize the distribution of Mean Disorder Scores
plt.figure(figsize=(8, 5))
plt.hist(df['Mean_Disorder'].dropna(), bins=20, edgecolor='black')
plt.xlabel('Mean Disorder Score')
plt.ylabel('Number of CDR3 Sequences')
plt.title('Distribution of Mean Disorder Scores')
plt.show()

# Visualize the distribution of Fraction Disordered
plt.figure(figsize=(8, 5))
plt.hist(df['Fraction_Disordered'].dropna(), bins=20, edgecolor='black')
plt.xlabel('Fraction of Residues with Disorder > 0.5')
plt.ylabel('Number of CDR3 Sequences')
plt.title('Distribution of Fraction Disordered Residues')
plt.show()
