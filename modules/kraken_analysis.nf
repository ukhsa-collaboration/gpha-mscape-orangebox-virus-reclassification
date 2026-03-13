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
        path "${climbid}_taxacounts.txt", emit: taxacounts
        path "${climbid}_taxa.txt"
        path "${climbid}_lineages.txt", emit: lineages
        path "${climbid}_viral_reclassifier.kraken.json", emit: json

    script:
    """
    cat "${kraken_report}" | cut -f5,3 | tail -n+3 > "${climbid}_taxacounts.txt"
    cat "${kraken_report}" | cut -f5 | tail -n+3 > "${climbid}_taxa.txt"
    taxonkit lineage --data-dir "${db_path}" -R "${climbid}_taxa.txt"  > "${climbid}_lineages.txt"
    aggregate_lineages_bracken.py -i "${climbid}_lineages.txt" -b "${climbid}_taxacounts.txt" -u "${kraken_report}" -p "temp_kraken"
    file1=`cat *.json`
    echo "{"'"${climbid}"'": "\$file1"}" >> "${climbid}_viral_reclassifier.kraken.json"
    """

}


process DETECT_VIRUS {
    container 'ghcr.io/ukhsa-collaboration/gpha-mscape-taxaplease:2.1.1'
    publishDir "results", mode: "copy"
    
    input:
        val climbid
        val runid
        path kraken_report
        path kraken_results
        val tp_db_path
        
    output:
        //file "${climbid}_taxacounts.txt"
        //file "${climbid}_taxa.txt"
        //file "${climbid}_lineages.txt"
        //file "${climbid}.VIRUS_RECLASSIFICATION.analysis_fields.json"
        path "${climbid}_data.json", emit: detection_json
    
    script:
    """  
    virus_presence.py --report ${kraken_report} --results ${kraken_results} --climbid ${climbid} --runid ${runid} --database ${tp_db_path}
    """
}


process ONYX_JSON {
    container 'ghcr.io/ukhsa-collaboration/gpha-mscape-onyx-analysis-helper:pr-2'
    publishDir "results", mode: "copy"
    
    input:
        val climbid
        val runid
        path kraken_report
        path kraken_results
        path results_json
        path results_summary_json
        path file
        path kraken_database
        
    output:
        //file "${climbid}_taxacounts.txt"
        //file "${climbid}_taxa.txt"
        //file "${climbid}_lineages.txt"
        file "${climbid}.VIRUS_RECLASSIFICATION.analysis_fields.json"
    
    script:
    """  
    create_onyx_json.py --report ${kraken_report} --results ${kraken_results} --climbid ${climbid} --runid ${runid} --results_json ${results_json} --results_json_summary ${results_summary_json} --file_path ${file} --method ${kraken_database} --pipeline_info \"name:${workflow.manifest.name},version:${workflow.manifest.version},homePage:${workflow.manifest.homePage}\"
    """
    
}