# Computational Analysis of Intrinsic Disorder in CDR3 Immune Receptor Regions   

This project explores the structural flexibility of CDR3 regions in immune receptor sequences through computational disorder prediction.

Project Summary

- **Objective:** Determine intrinsic disorder profiles of CDR3 sequences from cancer patient datasets.
- **Workflow:**
  - Extracted CDR3-containing reads from aligned BAM files using a custom VDJ mining pipeline.
  - Filtered immune receptor loci (e.g., IGH, TRB) and validated sequences using the VDJdb database.
  - Processed and wrangled data in R for clean export.
  - Applied `metapredict` (Python) to quantify and visualize disorder scores across CDR3 regions and their V/J context.

 Key Findings

- CDR3 regions showed moderate disorder across all samples.
- When analyzed with their surrounding V and J segments, CDR3s were **more disordered** on average but **not highly disordered** overall — suggesting functional flexibility without full disorder.

Tools & Technologies

- Python, R, metapredict, SAMtools, VDJdb
- GDC Data Transfer Tool, UNIX Shell

 Data

- Input: BAM files from GDC (TCGA/CPTAC datasets)
- Output: CSVs with CDR3 sequences and per-residue disorder scores

---

