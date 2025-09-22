import metapredict as meta     
import pandas as pd        

def import_tsv(filename):
    """Load TSV file into a pandas DataFrame."""
    return pd.read_csv(filename, sep='\t')

def get_disorder(sequence, d_threshold=0.3, min_idr_size=9):
    """Compute disorder scores per residue for a given sequence, handling invalid characters."""
    # Remove '*' (stop codon) and replace 'X' (unknown) with 'A'
    sequence = sequence.replace("*", "").replace("X", "A")  
    
    # Ensure sequence is not empty after filtering
    if not sequence:
        return "No valid residues"

    disorder_obj = meta.predict_disorder(sequence, return_domains=True,
                                         disorder_threshold=d_threshold,
                                         minimum_IDR_size=min_idr_size)
    return ",".join(map(str, disorder_obj.disorder))  # Convert to comma-separated string

def main():
    timestamp = "17409309014266422"
    input_filename = "vdj_sample_" + timestamp + ".tsv"
    
    # Load VDJ data
    vdj = import_tsv(input_filename)
    
    # Define the column names (update if different in your file)
    cdr3_column = "V_CDR3_J"  # Column with CDR3 sequences
    id_column = "Filename"  # Unique identifier column
    

    # Compute disorder scores for each CDR3 sequence
    vdj["Disorder_Scores"] = vdj[cdr3_column].apply(get_disorder)
    
    # Save the results with unique identifiers
    output_filename = "disorder_results_" + timestamp + ".tsv"
    vdj[[id_column, cdr3_column, "Disorder_Scores"]].to_csv(output_filename, sep='\t', index=False)
    print(f"Results saved to {output_filename}")

if __name__ == "__main__":
    main()
