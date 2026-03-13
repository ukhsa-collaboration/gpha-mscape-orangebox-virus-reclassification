#!/usr/bin/env nextflow

include { KRAKEN } from './modules/viral_kraken.nf'
include { ANALYSIS } from './modules/kraken_analysis.nf'
include { ONYX_JSON } from './modules/kraken_analysis.nf'
include { DETECT_VIRUS } from './modules/kraken_analysis.nf'

workflow {
     fastq = channel.fromPath(params.fastq)
     KRAKEN(fastq, params.kraken_database, params.runid)
     ANALYSIS(KRAKEN.out.climbid, params.runid, KRAKEN.out.kreport, KRAKEN.out.kresults, params.db_path)
     DETECT_VIRUS(KRAKEN.out.climbid, params.runid, KRAKEN.out.kreport, KRAKEN.out.kresults, params.tp_db_path)
     ONYX_JSON(KRAKEN.out.climbid, params.runid, KRAKEN.out.kreport, KRAKEN.out.kresults, ANALYSIS.out.json, DETECT_VIRUS.out.detection_json, params.fastq, params.kraken_database)
}