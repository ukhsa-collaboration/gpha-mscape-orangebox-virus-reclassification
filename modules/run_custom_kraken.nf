#!/usr/bin/env nextflow

process KRAKEN {
    container 'quay.io/biocontainers/kraken2:2.17--pl5321h077b44d_0'
    // tag "${climb_id}"
    label 'process_medium'
    publishDir "results", mode: 'copy'
    
    input:
        val fastq
        val customdb
        // val climbid  // need to include -> climbid_kraken_results.txt and climb_kraken_report.txt
        val runid  // need to include -> climbid_runid_kraken_results.txt

    output:
        path "${fastq.baseName}_${runid}_kraken_results.txt", emit: kresults
        path "${fastq.baseName}_${runid}_kraken_report.txt", emit: kreport
        val "${fastq.baseName}", emit: climbid

    script:
    """
    kraken2 --db ${customdb} ${fastq} --output ${fastq.baseName}_${runid}_kraken_results.txt --report ${fastq.baseName}_${runid}_kraken_report.txt
    """
}