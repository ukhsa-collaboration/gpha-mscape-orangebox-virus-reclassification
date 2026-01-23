#!/usr/bin/env nextflow


process ANALYSIS {
    container 'community.wave.seqera.io/library/biopython_taxonkit:f509bdb54ad22eed'
    publishDir "results", mode: 'copy'
    
    input:
        val climbid
        val runid
        path kraken_report
        path kraken_results
        val db_path

    output:
        // file "data.json"
        file "taxacounts.txt"
        file "taxa.txt"
        file "lineages.txt"
        file "${climbid}_viral_reclassifier.kraken.json"

    
    script:
    """
    cat "${kraken_report}" | cut -f5,3 | tail -n+3 > taxacounts.txt
    cat "${kraken_report}" | cut -f5 | tail -n+3 > taxa.txt
    taxonkit lineage --data-dir "${db_path}" -R taxa.txt  > lineages.txt
    aggregate_lineages_bracken.py -i "lineages.txt" -b "taxacounts.txt" -u "${kraken_report}" -p "temp_kraken"
    file1=`cat *.json`
    echo "{"'"${climbid}"'": "\$file1"}" >> "${climbid}_viral_reclassifier.kraken.json"
    """

    

}