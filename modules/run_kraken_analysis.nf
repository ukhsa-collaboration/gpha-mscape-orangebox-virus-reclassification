#!/usr/bin/env nextflow


process ANALYSIS {
    container 'community.wave.seqera.io/library/pip_pandas:40d2e76c16c136f0'
    container 'ghcr.io/ukhsa-collaboration/gpha-mscape-taxaplease:2.0.0'
    publishDir "results", mode: 'copy'
    
    input:
        val climbid
        val runid
        path kraken_report
        path kraken_results
        val directory
        val db_path

    output:
        file "midpoint.csv"

    
    script:
    """
    do_stuff.py --report ${kraken_report} --results ${kraken_results} --outdir ${directory} --climb-id ${climbid} --run-id ${runid} --s3-bucket "" --database ${db_path}

    """

}