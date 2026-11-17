#!/usr/bin/env nextflow


process ANALYSIS {
    container 'community.wave.seqera.io/library/biopython_taxonkit:f509bdb54ad22eed'
    publishDir "results", mode: 'copy'
    
    input:
        val sample_id
        path fastq
        path kraken_report
        path kraken_results
        val microbe
        val tp_database
        val ncbi_database
        val out_dir

    output:
        // file "data.json"
        path "${climbid}_taxacounts.txt", emit: taxacounts
        path "${climbid}_taxa.txt"
        path "${climbid}_lineages.txt", emit: lineages
        path "${climbid}_viral_reclassifier.kraken.json", emit: json

    script:
    """
    classify run-reclassification \
    --sample-id ${sample_id} \
    --fastq ${fastq} \
    --kraken_report ${kraken_report} \
    --kraken_results ${kraken_results} \
    --microbbe ${microbe} \
    --tp_database ${tp_database} \
    --ncbi_database ${ncbi_database} \
    --out_dir ${out_dir}
    """
}