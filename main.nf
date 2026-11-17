#!/usr/bin/env nextflow

include { KRAKEN } from './modules/kraken.nf'
include { ANALYSIS } from './modules/analysis.nf'

workflow {
     KRAKEN(params.climb_id, params.run_id, params.fastq, params.scan_name, params.kraken_database)
     ANALYSIS(params.sample_id, fastq, params.run_id, KRAKEN.out.kreport, KRAKEN.out.kresults, params.microbe, 
     params.tp_db_path, params.ncbi_db_path, params.out_dir)
}
