
# <img src="https://upload.wikimedia.org/wikipedia/fi/6/69/UKHSA_Logo.svg.png" width="75" height="75"> GPHA mSCAPE OrangeBox Virus Reclassification
---

## Table of Contents

- [Info](#info)
- [Features](#features)
- [Requirements](#requirements)
- [Install](#install)
- [Usage](#usage)
- [Commands](#commands)
- [Troubleshooting](#troubleshooting)
- [Change-log](#change-log)
- [To-do](#to-do)
---

## Info

| Name         | GPHA mSCAPE OrangeBox Virus Reclassification                                        |
|--------------|-------------------------------------------------------------------------------------|
| Version      | 1.0.1                                                                               |
| Last Updated | 28.02.2026                                                                          |
| Author(s)    | Mike Brown                                                                          |
| Contact      | michael.d.brown@ukhsa.gov.uk                                                        |
| Summary      | NextFlow data pipleine for rerunning Kraken with comprehensive custom viral database|

---

## Features

<img width="1051" height="700" alt="image" src="https://github.com/user-attachments/assets/db9a08d0-a8e4-4ccf-8476-8d0d6c160289" />

---

## Requirements
> [!Warning]
> To run it is neccessary to have obtained:
> Access to BRYN <br>
---

## Install
- Login to BRYN
- Start notebook server
- Start a terminal session
- Navigate to desired parent directory
- Run:
```bash
git clone https://github.com/ukhsa-collaboration/gpha-mscape-orangebox-virus-reclassification.git

```
> [!Tip]
> It is reccomended to run in screen or TMUX session in case of crash
---

## Usage
##### To run the pipeline
  - Navigate to gpha-mscape-orangebox-virus-reclassification folder
  - Run the NextFlow data pipeline
  - Run:
```bash
cd gpha-mscape-orangebox-virus-reclassification
nextflow run main.nf 
```
---

## Commands
> [!Note]
> Arguments can be filled out in the config/params.config file

  - --fastq - path to fastq files
  - --kraken_database - path to custom Kraken database folder
  - --output - output diirectory path
  - --runid - Run ID
  - --db_path - path to folder containing taxa DB files
---

## Troubleshooting

> [!Important]
> Make sure all paths are entered correctly <br>
> Make sure necessary DB files are within directed folders
---

## Change-log

---

## To-do

- [ ] \(Optional) run ruff linter on .py files
- [ ] \(Optional) task

---
