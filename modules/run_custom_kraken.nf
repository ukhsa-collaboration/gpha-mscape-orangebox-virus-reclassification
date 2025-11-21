#!/usr/bin/env nextflow

process KRAKEN {
    // container 'docker.io/staphb/kraken2:2.1.6'
    container 'quay.io/biocontainers/kraken2:2.17--pl5321h077b44d_0'
    cpus = 8
    memory = '16GB'
    publishDir "results", mode: 'copy'
    
    input:
        val fastq
        val customdb
        val climbid  // need to include -> climbid_kraken_results.txt and climb_kraken_report.txt
        val runid  // need to include -> climbid_runid_kraken_results.txt 

    output:
        file "kraken_results.txt", emit: results
        file "kraken_report.txt", emit: report

    script:
    """
    kraken2 --db ${customdb} ${fastq} --output ${climbid}_${run_id}_kraken_results.txt --report ${climbid}_${run_id}_kraken_report.txt
    """
}

