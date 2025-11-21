#!/usr/bin/env nextflow


process ANALYSIS{
    container ''
    cpus = 2
    memory = '4GB'
    
    input:
        file kraken_report.txt
        file kraken_results.txt
        val directory

    
    script:
    """
    do_stuff.py --reports ${kraken_report.txt} --results ${kraken_results.txt} --outdir ${directory}

    """

}