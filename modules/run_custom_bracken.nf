#!/usr/bin/env nextflow

process BRACKEN {
    container 'quay.io/biocontainers/bracken:3.1--h9948957_0'
    // tag "${climb_id}"
    label 'process_medium'
    publishDir "results", mode: 'copy'
    
    input:
        path kreport
        val customdb
        val climbid  // need to include -> climbid_kraken_results.txt and climb_kraken_report.txt
        val runid  // need to include -> climbid_runid_kraken_results.txt

    output:
        path "${climbid}_${runid}_bracken_summary.txt", emit: bsummary
        path "${climbid}_${runid}_bracken_report.txt", emit: breport

    script:
    """
    bracken \
        -d "${customdb}" \
        -i "${kreport}" \
        -r null \
        -l 'S' \
        -o "${climbid}_${runid}.bracken_summary.txt" \
        -w "${climbid}_${runid}.bracken_report.txt"
    """
}

    //do_stuff.py --report ${kraken_report} --results ${kraken_results} --outdir ${directory} --climbid ${climbid} --runid ${runid} --s3-bucket "" //--database ${db_path}