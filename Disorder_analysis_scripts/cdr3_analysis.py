import pandas as pd

# File paths
raw_data_file = "/Users/tusharsingh/Documents/PY/idp_vdj/vdj_sample_17409309014266422_half.tsv"
disorder_file = "/Users/tusharsingh/Documents/PY/idp_vdj/disorder_results_17409309014266422_half.tsv"
output_file = "cdr3_disorder_analysis.tsv"

# Load datasets
raw_df = pd.read_csv(raw_data_file, sep="\t")
disorder_df = pd.read_csv(disorder_file, sep="\t")

# Strip spaces from column names
raw_df.columns = raw_df.columns.str.strip()
disorder_df.columns = disorder_df.columns.str.strip()

# Merge datasets on 'Filename'
merged_df = pd.merge(raw_df, disorder_df, on="Filename", how="inner")

# Rename 'V_CDR3_J_x' if it exists
if 'V_CDR3_J_x' in merged_df.columns:
    merged_df['V_CDR3_J'] = merged_df['V_CDR3_J_x']
    merged_df = merged_df.drop(columns=['V_CDR3_J_x', 'V_CDR3_J_y'], errors='ignore')

# Function to extract disorder scores corresponding to CDR3
def extract_cdr3_disorder(v_cdr3_j, cdr3, disorder_scores):
    disorder_scores = [float(score) for score in disorder_scores.split(',')]  # Convert to list of floats
    start_pos = v_cdr3_j.find(cdr3)
    if start_pos != -1:
        end_pos = start_pos + len(cdr3)
        return disorder_scores[start_pos:end_pos]  # Return only the relevant disorder scores
    return []

# Apply the function to get CDR3-specific disorder scores
merged_df['CDR3_Disorder_Scores'] = merged_df.apply(
    lambda row: extract_cdr3_disorder(row['V_CDR3_J'], row['CDR3'], row['Disorder_Scores']),
    axis=1
)

# Function to compute disorder statistics
def calculate_disorder_stats(disorder_scores):
    if disorder_scores:  # Ensure it's not empty
        mean_score = sum(disorder_scores) / len(disorder_scores)
        num_disordered = sum(1 for score in disorder_scores if score > 0.5)
        total_residues = len(disorder_scores)
        fraction_disorder = num_disordered / total_residues if total_residues else 0
        return pd.Series([mean_score, num_disordered, total_residues, fraction_disorder])
    return pd.Series([None, 0, 0, 0])

# Compute disorder statistics
merged_df[['Mean_Score', 'Num_Disordered_Residues', 'Total_Residues', 'Fraction_Disorder']] = \
    merged_df['CDR3_Disorder_Scores'].apply(calculate_disorder_stats)

# Convert disorder scores back to string format for final output
merged_df['CDR3_Disorder_Scores'] = merged_df['CDR3_Disorder_Scores'].apply(lambda x: ','.join(map(str, x)) if x else '')

# Select and order final columns
output_df = merged_df[['Filename', 'CDR3', 'V_CDR3_J', 'CDR3_Disorder_Scores', 'Mean_Score', 'Num_Disordered_Residues', 'Total_Residues', 'Fraction_Disorder']]

# Save to file
output_df.to_csv(output_file, sep="\t", index=False)

print(f"Analysis complete. Results saved to: {output_file}")
