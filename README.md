# CCP-IOSCO Database for European Central Counterparties

## Overview

This repository contains the code, data construction pipeline, and database outputs for a harmonised panel of European central counterparties (CCPs) based on CPMI-IOSCO public quantitative disclosures.

The project builds a quarterly database covering major European CCPs from **2015Q3 to 2025Q2**. The raw disclosures are mapped consistently at the **CCP × service × currency × quarter** level and aggregated into complementary **CCP-level** and **EU-level** analysis datasets.

The database was developed to support empirical research on CCP risk buffers, including default waterfalls, leverage, and procyclicality.

## Coverage

The database covers the following CCPs:

- Athex
- BME Clearing
- CBOE Clear Europe
- CCP Austria
- Eurex AG
- Euronext
- European Commodity Clearing
- ICE Clear
- KDPW
- KELER
- LCH
- NASDAQ
- OMI Clearing
- SKDD

## Repository Structure

- **Code/**  
  Scripts for data collection, harmonisation, compilation, currency conversion, aggregation, and analysis.

- **Database/**  
  Compiled CCP-level datasets, harmonised EUR-denominated files, and consolidated database outputs.

- **Raw Data/**  
  Archived source disclosure files downloaded from public CCP reporting pages.

- **Additional Info/**  
  Supplementary material such as variable mappings, coverage information, audit notes, and supporting documentation.

## What the Database Contains

The construction pipeline is designed to:

1. download and archive source disclosure files,
2. parse the relevant CPMI-IOSCO quantitative disclosure tables,
3. harmonise variable names and identifiers across CCPs and reporting vintages,
4. construct comparable activity totals from the 23.x.x block,
5. merge and de-duplicate overlapping disclosures,
6. convert non-EUR observations into EUR,
7. build CCP-level and EU-level quarterly analysis datasets.

## Main Unit of Observation

The raw long-format database is organised at the following level:

- **CCP**
- **Service**
- **Currency**
- **Quarter**
- **Variable**

This structure preserves the original reporting granularity and supports flexible aggregation for analysis.

## Key Variables

- **ReportDate**  
  Reporting date extracted from the source disclosure.

- **CCP**  
  CCP identifier.

- **ClearingService**  
  The report-level clearing service or market segment reported in the disclosure templates.

- **DefaultFund**  
  Identifier for the relevant default fund grouping used in the harmonised database.

- **Currency**  
  Currency denomination of the reported value before EUR conversion.

- **Variable**  
  CPMI-IOSCO quantitative disclosure code, harmonised to a consistent format across sources.

## Currency Conversion

All series used in the final analysis are expressed in EUR. Where CCPs report in non-EUR currencies, values are converted into EUR using a consistent quarterly exchange-rate series based on European Central Bank exchange rates. The corresponding conversion factors are applied systematically across observations in the data construction pipeline.

## Reproducibility

The workflow is fully script-based. The pipeline is designed to preserve file-to-sheet-to-row lineage, support auditability, and make the final database reproducible.

A small number of targeted adjustments are documented explicitly in the workflow and supporting materials where necessary.

## Usage Notes

To reproduce the database:

1. archive or update the raw disclosure files,
2. run the parsing and harmonisation scripts,
3. compile CCP-specific datasets,
4. run the database consolidation scripts,
5. run the currency conversion step,
6. generate the CCP-level and EU-level analysis files.

Please check local paths and environment settings before running the scripts.

## Research Use

This repository supports the paper:

**Risk Buffers in European Central Counterparties: Default Waterfalls, Leverage, and Procyclicality**

The database is intended for research and replication purposes.

## Contact

For questions regarding the repository or database construction, please contact:

**Yannick Broich**  
info@yannick-broich.de
