#!/usr/bin/env nextflow

process KRAKEN {
    container 'quay.io/biocontainers/kraken2:2.17--pl5321h077b44d_0'
    label 'process_medium'
    publishDir "results", mode: 'copy'
    
    input:
        val climb_id
        val run_id 
        val fastq
        val scan_name
        val kraken_db

    output:
        path "${fastq.getBaseName(1)}_${climb_id}_${scan_name}_kraken_results.txt", emit: kresults
        path "${fastq.getBaseName(1)}_${climb_id}_${scan_name}_kraken_report.txt", emit: kreport

    script:
    """
    kraken2 --db ${kraken_db} ${fastq} --output ${fastq.baseName}_${climb_id}_${scan_name}_kraken_results.txt --report ${fastq.baseName}_${climb_id}_${scan_name}_kraken_report.txt
    """
}