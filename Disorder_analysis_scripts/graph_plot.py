#!/usr/bin/python

import metapredict as meta
import pandas as pd
import re

def import_tsv(filename):
    df = pd.read_csv(filename, sep='\t')
    return df

def get_disorder(sequence,d_threshold=0.3,min_idr_size=9):
    return meta.predict_disorder(sequence, return_domains=True,
                                 disorder_threshold=d_threshold,
                                 minimum_IDR_size=min_idr_size)

def graph_disordered_regions_cdr3(sequence, name, number):
    graph_title = str(number) + ": " + name + " Disorder"
    output_filename = str(number) + "_" + name
    meta.graph_disorder(sequence, pLDDT_scores=True, title=graph_title, disorder_threshold=0.3,
                        output_file=output_filename)

def graph_disordered_regions_shaded_idr(sequence, name, number):
    graph_title = str(number) + ": " + name + " Disordered Regions"
    output_filename = str(number) + "_" + name
    disorder = get_disorder(sequence)
    boundaries = disorder.disordered_domain_boundaries
    one_index_boundaries = [[element + 1 for element in sublist] for sublist in boundaries]
    meta.graph_disorder(sequence, pLDDT_scores=True, title=graph_title, disorder_threshold=0.3,
                        shaded_regions=one_index_boundaries, shaded_region_color="red",
                        output_file=output_filename)
    
def graph_disordered_regions_shaded_v_cdr3_j(sequence, cdr, name, number):
    graph_title = str(number) + ": " + name + " Disorder"
    output_filename = str(number) + "_" + name
    meta.graph_disorder(sequence, pLDDT_scores=True, title=graph_title, disorder_threshold=0.3,
                        shaded_regions=cdr, shaded_region_color="lime",
                        output_file=output_filename)

def graph_cdr3(df):
    column_indices = df.columns.get_indexer(["Case ID", "CDR3"])
    name_index = column_indices[0]
    sequence_index = column_indices[1]
    num_rows = df.shape[0]
    row_indices = list(range(num_rows))
    print("Generating graphs of disordered regions:")
    for index in row_indices:
        current_sequence = df.iat[index,sequence_index]
        # sanitize inputs for metapredict
        sanitized_sequence = re.sub(r'[^ARNDCQEGHILKMFPSTWYV]',"",current_sequence)
        current_name = "CDR3_" + df.iat[index,name_index]
        graph_disordered_regions_cdr3(sanitized_sequence, current_name, index)
        print(str(index) + "_" + current_name)
    print("Task complete!")

def graph_v_cdr3_j(df):
    column_indices = df.columns.get_indexer(["Case ID", "V_CDR3_J", "CDR3"])
    name_index = column_indices[0]
    sequence_index = column_indices[1]
    cdr_index = column_indices[2]
    num_rows = df.shape[0]
    row_indices = list(range(num_rows))
    print("Generating graphs of disordered regions:")
    for index in row_indices:
        current_sequence = df.iat[index,sequence_index]
        # sanitize inputs for metapredict
        sanitized_sequence = re.sub(r'[^ARNDCQEGHILKMFPSTWYV]',"",current_sequence)
        current_cdr = df.iat[index,cdr_index]
        # sanitize inputs for metapredict
        sanitized_cdr = re.sub(r'[^ARNDCQEGHILKMFPSTWYV]',"",current_cdr)
        for loc in re.finditer(sanitized_cdr, sanitized_sequence):
            cdr_loc_list = [[loc.start()+1,loc.end()+1]]
        current_name = "V_CDR3_J_" + df.iat[index,name_index]
        graph_disordered_regions_shaded_v_cdr3_j(sanitized_sequence, cdr_loc_list, 
                                             current_name, index)
        print(str(index) + "_" + current_name)
    print("Task complete!")

    
def main():
    timestamp = "17409309014266422"
    input_filename = "vdj_sample_" + timestamp + ".tsv"
    vdj = import_tsv(input_filename)
    graph_cdr3(vdj)
    graph_v_cdr3_j(vdj)
    
    
if __name__ == "__main__":
    main()