#!/usr/bin/env nextflow

include { KRAKEN } from './modules/run_custom_kraken.nf'
include { ANALYSIS } from './modules/run_kraken_analysis.nf'


workflow {
     KRAKEN(params.fastq, params.kraken_database, params.climbid, params.runid)
     ANALYSIS(params.climbid, params.runid, KRAKEN.out.kreport, KRAKEN.out.kresults, params.db_path)
}