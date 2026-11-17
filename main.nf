#!/usr/bin/env nextflow

include { KRAKEN } from './modules/kraken.nf'
include { ANALYSIS } from './modules/analysis.nf'

workflow {
     fastq = channel.fromPath(params.fastq)
     KRAKEN(fastq, params.kraken_database, params.runid)
     ANALYSIS(params.sample_id, fastq, params.run_id, KRAKEN.out.kreport, KRAKEN.out.kresults, params.microbe, 
     params.tp_db_path, params.ncbi_db_path, params.out_dir)
}