# IOSCO Publications Database for European Central Counterparties (CCPs)

## Project Description

This project entails developing a code that downloads, compiles, and converts the IOSCO publications of most of the active Central Counterparties (CCPs) in Europe into a comprehensive database. Of the 14 CCPs authorized to offer services and activities in the European Union, 11 are included.

They are:

- BOE Clear
- KDPW
- Eurex AG
- LCH
- European Commodity Clearing
- SKDD
- ICE Clear
- OMIClear
- BME Clearing
- CCP Austria

The CCPs yet to be implemented are Keler CCP, Athex Clearing House and Nasdaq OMX Clearing.

## Project Structure

- **Code**: Contains all the scripts used in the project.
- **Database**: Stores the compiled datasets for each CCP and the final IOSCO database.
- **Raw Data**: Folder containing all the downloaded files.
- **Additional Info**: Contains supplementary information such as the variables reported by each CCP and the quarters for which the data is available.

## Instructions

1. **Adjust the Path**: Ensure you change the path to match your system configuration.
2. **Run the Web Scraper**: Execute the web scraping script.
3. **Run the Compilation Scripts**: Either run all compilation scripts individually or use the script that executes all CCP-specific scripts simultaneously.
4. **Run the Database Compiler Preconversion**: Execute the preconversion database compiler script.
5. **Run the Conversion Script**: Execute the conversion script to convert currencies to Euros. Note that the conversion rates are hardcoded as of July 5, 2024.

## Explanation of Variables

- **ReportDate**: Extracted from the source, indicating the publication date.
- **CCP**: Hardcoded identifier for each CCP.
- **Clearing Service**: The variable “ReportLevelIdentifier” identifies different clearing services within the CCP.
- **DefaultFund**: Derived from the “Clearing Service” variable. CCPs either have a single default fund that covers their entire portfolio or several ones. If unsure, the DefaultFund is set as CCP_"ClearingService". Example: BMEC_Equity 
- **Currency**: The currency code indicating the denomination of the value.
