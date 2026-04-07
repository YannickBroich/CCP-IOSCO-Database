
import os
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DIRECTORY = r"YOUR_PATH_TO_REPLICATION_PACKAGE\Replication Package\Database\01. Compiled CCP Datasets"
OUTPUT = r"YOUR_PATH_TO_REPLICATION_PACKAGE\Replication Package\Database\02. Intermediate Panel\CCP_IOSCO_Database - I Raw Values.xlsx"


column_map = {
    'ReportDate': ['ReportDate'],
    'CCP': ['CCP'],
    'ClearingService': ['ClearingService'],
    'DefaultFund': ['DefaultFund'],
    'Currency': ['Currency'],

    '4.1.1': ['4.1.1', '4_1_1'],
    '4.1.2': ['4.1.2', '4_1_2'],
    '4.1.3': ['4.1.3', '4_1_3'],
    '4.1.4': ['4.1.4', '4_1_4'],
    '4.1.5': ['4.1.5', '4_1_5'],
    '4.1.6': ['4.1.6', '4_1_6'],
    '4.1.7': ['4.1.7', '4_1_7'],
    '4.1.8': ['4.1.8', '4_1_8'],
    '4.1.9': ['4.1.9', '4_1_9'],
    '4.1.10': ['4.1.10', '4_1_10'],
    '4.2.1': ['4.2.1', '4_2_1'],
    '4.4.1': ['4.4.1', '4_4_1'],
    '4.4.2': ['4.4.2', '4_4_2'],
    '4.4.4': ['4.4.4', '4_4_4'],
    '4.4.8': ['4.4.8', '4_4_8'],

    '5.1.1': ['5.1.1', '5_1_1'],
    '5.2.1': ['5.2.1', '5_2_1'],
    '5.3.1': ['5.3.1', '5_3_1'],
    '5.3.2': ['5.3.2', '5_3_2'],
    '5.3.3': ['5.3.3', '5_3_3'],
    '5.3.4': ['5.3.4', '5_3_4'],

    '6.3.1': ['6.3.1', '6_3_1'],
    '6.4.1': ['6.4.1', '6_4_1'],
    '6.4.2': ['6.4.2', '6_4_2'],
    '6.4.3': ['6.4.3', '6_4_3'],
    '6.4.4': ['6.4.4', '6_4_4'],
    '6.4.5': ['6.4.5', '6_4_5'],
    '6.4.6': ['6.4.6', '6_4_6'],
    '6.4.7': ['6.4.7', '6_4_7'],
    '6.4.8': ['6.4.8', '6_4_8'],
    '6.4.9': ['6.4.9', '6_4_9'],
    '6.4.10': ['6.4.10', '6_4_10'],
    '6.4.11': ['6.4.11', '6_4_11'],
    '6.4.12': ['6.4.12', '6_4_12'],
    '6.4.13': ['6.4.13', '6_4_13'],
    '6.4.14': ['6.4.14', '6_4_14'],
    '6.4.15': ['6.4.15', '6_4_15'],

    '6.5.1.1': ['6.5.1.1', '6_5_1_1'],
    '6.5.1.2': ['6.5.1.2', '6_5_1_2'],
    '6.5.1.3': ['6.5.1.3', '6_5_1_3'],
    '6.5.2': ['6.5.2', '6_5_2'],
    '6.5.3': ['6.5.3', '6_5_3'],
    '6.5.4': ['6.5.4', '6_5_4'],
    '6.5.5': ['6.5.5', '6_5_5'],

    '6.6.1': ['6.6.1', '6_6_1'],
    '6.7.1': ['6.7.1', '6_7_1'],
    '6.8.1': ['6.8.1', '6_8_1'],

    '7.1.1': ['7.1.1', '7_1_1'],
    '7.1.10': ['7.1.10', '7_1_10'],
    '7.1.11': ['7.1.11', '7_1_11'],
    '7.2.1': ['7.2.1', '7_2_1'],
    '7.3.2': ['7.3.2', '7_3_2'],

    '12.1.1': ['12.1.1', '12_1_1'],
    '12.1.2': ['12.1.2', '12_1_2'],
    '12.1.3': ['12.1.3', '12_1_3'],
    '12.2.1': ['12.2.1', '12_2_1'],
    '12.2.2': ['12.2.2', '12_2_2'],
    '12.2.3': ['12.2.3', '12_2_3'],

    '13.1.1': ['13.1.1', '13_1_1'],
    '13.1.2': ['13.1.2', '13_1_2'],
    '13.1.3.1': ['13.1.3.1', '13_1_3_1'],
    '13.1.3.2': ['13.1.3.2', '13_1_3_2'],
    '13.1.4': ['13.1.4', '13_1_4'],

    '14.1.1': ['14.1.1', '14_1_1'],
    '14.1.2': ['14.1.2', '14_1_2'],
    '14.1.3': ['14.1.3', '14_1_3'],
    '14.1.4': ['14.1.4', '14_1_4'],

    '15.1.1': ['15.1.1', '15_1_1'],
    '15.1.2': ['15.1.2', '15_1_2'],
    '15.2.1': ['15.2.1', '15_2_1'],
    '15.2.2': ['15.2.2', '15_2_2'],
    '15.2.3': ['15.2.3', '15_2_3'],
    '15.2.4': ['15.2.4', '15_2_4'],
    '15.2.5': ['15.2.5', '15_2_5'],
    '15.2.6': ['15.2.6', '15_2_6'],
    '15.2.7': ['15.2.7', '15_2_7'],
    '15.3.1': ['15.3.1', '15_3_1'],
    '15.3.2': ['15.3.2', '15_3_2'],

    '16.1.1': ['16.1.1', '16_1_1'],
    '16.1.2': ['16.1.2', '16_1_2'],

    '16.2.1': ['16.2.1', '16_2_1'],
    '16.2.2': ['16.2.2', '16_2_2'],
    '16.2.3': ['16.2.3', '16_2_3'],
    '16.2.4': ['16.2.4', '16_2_4'],
    '16.2.5': ['16.2.5', '16_2_5'],
    '16.2.6': ['16.2.6', '16_2_6'],
    '16.2.7': ['16.2.7', '16_2_7'],
    '16.2.8_Percentage_EUR': ['16.2.8_Percentage_EUR', '16.2.8_Perenteage_EUR', '16.2.8_EUR'],
    '16.2.8_Percentage_PLN': ['16.2.8_Percentage_PLN'],
    '16.2.8_Percentage_DKK': ['16.2.8_Percentage_DKK'],
    '16.2.8_Percentage_NOK': ['16.2.8_Percentage_NOK'],
    '16.2.8_Percentage_CHF': ['16.2.8_Percentage_CHF'],
    '16.2.8_Percentage_GBP': ['16.2.8_Percentage_GBP'],
    '16.2.8_Percentage_USD': ['16.2.8_Percentage_USD'],
    '16.2.8_Percentage_CNH': ['16.2.8_Percentage_CNH'],
    '16.2.8_Percentage_HRK': ['16.2.8_Percentage_HRK'],
    '16.2.8_Percentage_CAD': ['16.2.8_Percentage_CAD'],
    '16.2.8_Percentage_SGD': ['16.2.8_Percentage_SGD'],
    '16.2.8_Percentage_JPY': ['16.2.8_Percentage_JPY'],
    '16.2.8_Percentage_Other': ['16.2.8_Percentage_Other'],

    '16.2.9': ['16.2.9', '16_2_9'],
    '16.2.10': ['16.2.10', '16_2_10'],
    '16.2.11': ['16.2.11', '16_2_11'],
    '16.2.12': ['16.2.12', '16_2_12'],
    '16.2.13': ['16.2.13', '16_2_13'],
    '16.2.14': ['16.2.14', '16_2_14'],
    '16.2.15_Percentage_EUR': ['16.2.15_Percentage_EUR', '16.2.15_Perenteage_EUR', '16.2.15_EUR'],
    '16.2.15_Percentage_PLN': ['16.2.15_Percentage_PLN'],
    '16.2.15_Percentage_DKK': ['16.2.15_Percentage_DKK'],
    '16.2.15_Percentage_NOK': ['16.2.15_Percentage_NOK'],
    '16.2.15_Percentage_CHF': ['16.2.15_Percentage_CHF'],
    '16.2.15_Percentage_GBP': ['16.2.15_Percentage_GBP'],
    '16.2.15_Percentage_USD': ['16.2.15_Percentage_USD'],
    '16.2.15_Percentage_CNH': ['16.2.15_Percentage_CNH'],
    '16.2.15_Percentage_HRK': ['16.2.15_Percentage_HRK'],
    '16.2.15_Percentage_CAD': ['16.2.15_Percentage_CAD'],
    '16.2.15_Percentage_SGD': ['16.2.15_Percentage_SGD'],
    '16.2.15_Percentage_JPY': ['16.2.15_Percentage_JPY'],
    '16.2.15_Percentage_Other': ['16.2.15_Percentage_Other'],

    '16.2.16': ['16.2.16', '16_2_16'],
    '16.2.17': ['16.2.17', '16_2_17'],
    '16.2.18': ['16.2.18', '16_2_18'],
    '16.2.19': ['16.2.19', '16_2_19'],
    '16.2.20': ['16.2.20', '16_2_20'],

    '16.3.1': ['16.3.1', '16_3_1'],
    '16.3.2': ['16.3.2', '16_3_2'],
    '16.3.3_ON_1D': ['16.3.3_ON_1D', '16.3.3_nan'],
    '16.3.4_ON_1D': ['16.3.4_ON_1D', '16.3.4_nan'],
    '16.3.3_1D_1W': ['16.3.3_1D_1W'],
    '16.3.4_1D_1W': ['16.3.4_1D_1W'],
    '16.3.3_1W_1M': ['16.3.3_1W_1M'],
    '16.3.4_1W_1M': ['16.3.4_1W_1M'],
    '16.3.3_1M_1Y': ['16.3.3_1M_1Y'],
    '16.3.4_1M_1Y': ['16.3.4_1M_1Y'],
    '16.3.3_1Y_2Y': ['16.3.3_1Y_2Y'],
    '16.3.4_1Y_2Y': ['16.3.4_1Y_2Y'],
    '16.3.3_2Y+': ['16.3.3_2Y+'],
    '16.3.4_2Y+': ['16.3.4_2Y+'],

    '17.1.1': ['17.1.1', '17_1_1'],
    '17.2.1': ['17.2.1', '17_2_1'],
    '17.4.1': ['17.4.1', '17_4_1'],

    '17.3.1_DurationofFailures': [
        '17.3.1_DurationofFailures', '17.3.1_DurationofFailure4', '17.3.1_1 failure',
        '17.3.1_3 failures', '17.3.1_2 failures', '17.3.1_DurationofFailures_7',
        '17.3.1_DurationofFailures_6', '17.3.1_73 failures', '17.3.1_DurationofFailures_4',
        '17.3.1_DurationofFailures_5', '17.3.1_2 failurs', '17.3.1_3 failurs',
        '17_3_1,17.3.1_6 failures', '17.3.1_2 failure', '17.3.1_7 failures',
        '17.3.1_3 failurs', '17.3.1_2 failurs', '17.3.1_1 failurs', '17.3.1_0 failure',
        '17.3.1_DurationofFailure3', '17.3.1_DurationofFailure#(HH:MI:SS)',
        '17.3.1_DurationofFailure1', '17.3.1_DurationofFailure', '17.3.1_2 failures',
        '17.3.1_1 failure', '17.3.1_0 failures', '17.3.1_4 failures', '17.3.1_6 failures',
        '17.3.1_44 failures', '17.3.1_33 failures', '17.3.1_5 failures',
        '17.3.1_0 Failures', '17.3.1_1'
    ],
    '17.3.1_NumberofFailures': [
        '17.3.1_NumberofFailures', '17.3.1_no failure', '17.3.1_2 failures',
        'Total No of Failures', '17.3.1_No failures'
    ],

    '18.1.1.1': ['18.1.1.1', '18_1_1_1'],
    '18.1.1.2': ['18.1.1.2', '18_1_1_2'],
    '18.1.1.3': ['18.1.1.3', '18_1_1_3'],
    '18.1.2.1': ['18.1.2.1', '18_1_2_1'],
    '18.1.2.2': ['18.1.2.2', '18_1_2_2'],
    '18.1.2.3': ['18.1.2.3', '18_1_2_3'],
    '18.1.2.4': ['18.1.2.4', '18_1_2_4'],
    '18.1.3.1': ['18.1.3.1', '18_1_3_1'],
    '18.1.3.2': ['18.1.3.2', '18_1_3_2'],

    '18.2.1_AverageInQuarter': ['18.2.1_AverageInQuarter', '18.2.1_Average'],
    '18.2.1_PeakInQuarter': ['18.2.1_PeakInQuarter', '18.2.1_Peak'],
    '18.2.2_AverageInQuarter': ['18.2.2_AverageInQuarter', '18.2.2_Average'],
    '18.2.2_PeakInQuarter': ['18.2.2_PeakInQuarter', '18.2.2_Peak'],
    '18.2.3_AverageInQuarter': ['18.2.3_AverageInQuarter', '18.2.3_Average'],
    '18.2.3_PeakInQuarter': ['18.2.3_PeakInQuarter', '18.2.3_Peak'],

    '18.3.1_AverageInQuarter': ['18.3.1_AverageInQuarter', '18.3.1_Average'],
    '18.3.1_PeakInQuarter': ['18.3.1_PeakInQuarter', '18.3.1_Peak'],
    '18.3.2_AverageInQuarter': ['18.3.2_AverageInQuarter', '18.3.2_Average'],
    '18.3.2_PeakInQuarter': ['18.3.2_PeakInQuarter', '18.3.2_Peak'],
    '18.3.3_AverageInQuarter': ['18.3.3_AverageInQuarter', '18.3.3_Average'],
    '18.3.3_PeakInQuarter': ['18.3.3_PeakInQuarter', '18.3.3_Peak'],

    '18.4.1': ['18.4.1', '18_4_1'],
    '18.4.2': ['18.4.2', '18_4_2'],
    '18.4.3': ['18.4.3', '18_4_3'],

    '19.1.1': ['19.1.1', '19_1_1'],
    '19.1.2': ['19.1.2', '19_1_2'],
    '19.1.3.1': ['19.1.3.1', '19_1_3_1'],
    '19.1.3.2': ['19.1.3.2', '19_1_3_2'],
    '19.1.4.1': ['19.1.4.1', '19_1_4_1'],
    '19.1.4.2': ['19.1.4.2', '19_1_4_2'],

    # 4.3.x Pre/Post Haircut
    '4.3.1_PreHaircut': ['4.3.1_PreHaircut'],
    '4.3.1_PostHaircut': ['4.3.1_PostHaircut'],
    '4.3.2_PreHaircut': ['4.3.2_PreHaircut'],
    '4.3.2_PostHaircut': ['4.3.2_PostHaircut'],
    '4.3.3_PreHaircut': ['4.3.3_PreHaircut'],
    '4.3.3_PostHaircut': ['4.3.3_PostHaircut'],
    '4.3.4_PreHaircut': ['4.3.4_PreHaircut'],
    '4.3.4_PostHaircut': ['4.3.4_PostHaircut'],
    '4.3.5_PreHaircut': ['4.3.5_PreHaircut'],
    '4.3.5_PostHaircut': ['4.3.5_PostHaircut'],
    '4.3.6_PreHaircut': ['4.3.6_PreHaircut'],
    '4.3.6_PostHaircut': ['4.3.6_PostHaircut'],
    '4.3.7_PreHaircut': ['4.3.7_PreHaircut'],
    '4.3.7_PostHaircut': ['4.3.7_PostHaircut'],
    '4.3.8_PreHaircut': ['4.3.8_PreHaircut'],
    '4.3.8_PostHaircut': ['4.3.8_PostHaircut'],
    '4.3.9_PreHaircut': ['4.3.9_PreHaircut'],
    '4.3.9_PostHaircut': ['4.3.9_PostHaircut'],
    '4.3.10_PreHaircut': ['4.3.10_PreHaircut'],
    '4.3.10_PostHaircut': ['4.3.10_PostHaircut'],
    '4.3.11_PreHaircut': ['4.3.11_PreHaircut'],
    '4.3.11_PostHaircut': ['4.3.11_PostHaircut'],
    '4.3.12_PreHaircut': ['4.3.12_PreHaircut'],
    '4.3.12_PostHaircut': ['4.3.12_PostHaircut'],
    '4.3.13_PreHaircut': ['4.3.13_PreHaircut'],
    '4.3.13_PostHaircut': ['4.3.13_PostHaircut'],
    '4.3.14_PreHaircut': ['4.3.14_PreHaircut'],
    '4.3.14_PostHaircut': ['4.3.14_PostHaircut'],
    '4.3.15_PreHaircut': ['4.3.15_PreHaircut'],
    '4.3.15_PostHaircut': ['4.3.15_PostHaircut'],

    # 4.4.x Extras
    '4.4.3_PeakDayAmountInPast12Months': ['4.4.3_PeakDayAmountInPast12Months', '4.4.3_Peak Day Amount In Past 12 Months'],
    '4.4.3_MeanAverageOverPrevious12Months': ['4.4.3_MeanAverageOverPrevious12Months', '4.4.3_Mean Average Over Previous12 Months'],
    '4.4.6_PeakDayAmountInPast12Months': ['4.4.6_PeakDayAmountInPast12Months', '4.4.6_Peak Day Amount In Past 12 Months'],
    '4.4.6_MeanAverageOverPrevious12Months': ['4.4.6_MeanAverageOverPrevious12Months', '4.4.6_Mean Average Over Previous12 Months'],
    '4.4.7_PeakDayAmountInPast12Months': ['4.4.7_PeakDayAmountInPast12Months', '4.4.7_Peak Day Amount In Past 12 Months'],
    '4.4.7_MeanAverageOverPrevious12Months': ['4.4.7_MeanAverageOverPrevious12Months', '4.4.7_Mean Average Over Previous12 Months'],
    '4.4.10_PeakDayAmountInPast12Months': ['4.4.10_PeakDayAmountInPast12Months', '4.4.10_Peak Day Amount In Past 12 Months'],
    '4.4.10_MeanAverageOverPrevious12Months': ['4.4.10_MeanAverageOverPrevious12Months', '4.4.10_Mean Average Over Previous12 Months'],
    '4.4.5_AmountExceeded': [
        '4.4.5_AmountExceeded', '4.4.5_AmountExceeded0', '4.4.5_AmountExceeded3', '4.4.5_AmountExceeded1',
        '4.4.5_AmountExceeded day 1', '4.4.5_AmountExceeded day 2', '4.4.5_AmountExceeded day 3', '4.4.5_nan',
        '4.4.5_AmountExceeded2', '4.4.5_AmountExceeded4', '4.4.5_AmountExceeded_2'
    ],
    '4.4.9_AmountExceeded': [
        '4.4.9_AmountExceeded', '4.4.9_AmountExceeded3', '4.4.9_AmountExceeded0', '4.4.9_AmountExceeded1',
        '4.4.9_AmountExceeded day 1', '4.4.9_AmountExceeded day 2', '4.4.9_AmountExceeded day 3', '4.4.9_nan',
        '4.4.9_AmountExceeded2', '4.4.9_AmountExceeded4', '4.4.9_AmountExceeded_2'
    ],

    # 6.1 / 6.2 IM (House/Client/Total)
    '6.1.1_House_Net': ['6.1.1_House_Net', '6.1.1_House'],
    '6.1.1_Client_Net': ['6.1.1_Client_Net', '6.1.1_Client_net'],
    '6.1.1_Client_Gross': ['6.1.1_Client_Gross'],
    '6.1.1_Total': ['6.1.1_Total'],

    '6.2.1_HouseIM_PreHaircut': ['6.2.1_HouseIM_PreHaircut'],
    '6.2.1_HouseIM_PostHaircut': ['6.2.1_HouseIM_PostHaircut'],
    '6.2.2_HouseIM_PreHaircut': ['6.2.2_HouseIM_PreHaircut'],
    '6.2.2_HouseIM_PostHaircut': ['6.2.2_HouseIM_PostHaircut'],
    '6.2.3_HouseIM_PreHaircut': ['6.2.3_HouseIM_PreHaircut'],
    '6.2.3_HouseIM_PostHaircut': ['6.2.3_HouseIM_PostHaircut'],
    '6.2.4_HouseIM_PreHaircut': ['6.2.4_HouseIM_PreHaircut'],
    '6.2.4_HouseIM_PostHaircut': ['6.2.4_HouseIM_PostHaircut'],
    '6.2.5_HouseIM_PreHaircut': ['6.2.5_HouseIM_PreHaircut'],
    '6.2.5_HouseIM_PostHaircut': ['6.2.5_HouseIM_PostHaircut'],
    '6.2.6_HouseIM_PreHaircut': ['6.2.6_HouseIM_PreHaircut'],
    '6.2.6_HouseIM_PostHaircut': ['6.2.6_HouseIM_PostHaircut'],
    '6.2.7_HouseIM_PreHaircut': ['6.2.7_HouseIM_PreHaircut'],
    '6.2.7_HouseIM_PostHaircut': ['6.2.7_HouseIM_PostHaircut'],
    '6.2.8_HouseIM_PreHaircut': ['6.2.8_HouseIM_PreHaircut'],
    '6.2.8_HouseIM_PostHaircut': ['6.2.8_HouseIM_PostHaircut'],
    '6.2.9_HouseIM_PreHaircut': ['6.2.9_HouseIM_PreHaircut'],
    '6.2.9_HouseIM_PostHaircut': ['6.2.9_HouseIM_PostHaircut'],
    '6.2.10_HouseIM_PreHaircut': ['6.2.10_HouseIM_PreHaircut'],
    '6.2.10_HouseIM_PostHaircut': ['6.2.10_HouseIM_PostHaircut'],
    '6.2.11_HouseIM_PreHaircut': ['6.2.11_HouseIM_PreHaircut'],
    '6.2.11_HouseIM_PostHaircut': ['6.2.11_HouseIM_PostHaircut'],
    '6.2.12_HouseIM_PreHaircut': ['6.2.12_HouseIM_PreHaircut'],
    '6.2.12_HouseIM_PostHaircut': ['6.2.12_HouseIM_PostHaircut'],
    '6.2.13_HouseIM_PreHaircut': ['6.2.13_HouseIM_PreHaircut'],
    '6.2.13_HouseIM_PostHaircut': ['6.2.13_HouseIM_PostHaircut'],
    '6.2.14_HouseIM_PreHaircut': ['6.2.14_HouseIM_PreHaircut'],
    '6.2.14_HouseIM_PostHaircut': ['6.2.14_HouseIM_PostHaircut'],
    '6.2.15_HouseIM_PreHaircut': ['6.2.15_HouseIM_PreHaircut'],
    '6.2.15_HouseIM_PostHaircut': ['6.2.15_HouseIM_PostHaircut'],

    '6.2.1_ClientIM_PreHaircut': ['6.2.1_ClientIM_PreHaircut'],
    '6.2.1_ClientIM_PostHaircut': ['6.2.1_ClientIM_PostHaircut'],
    '6.2.2_ClientIM_PreHaircut': ['6.2.2_ClientIM_PreHaircut'],
    '6.2.2_ClientIM_PostHaircut': ['6.2.2_ClientIM_PostHaircut'],
    '6.2.3_ClientIM_PreHaircut': ['6.2.3_ClientIM_PreHaircut'],
    '6.2.3_ClientIM_PostHaircut': ['6.2.3_ClientIM_PostHaircut'],
    '6.2.4_ClientIM_PreHaircut': ['6.2.4_ClientIM_PreHaircut'],
    '6.2.4_ClientIM_PostHaircut': ['6.2.4_ClientIM_PostHaircut'],
    '6.2.5_ClientIM_PreHaircut': ['6.2.5_ClientIM_PreHaircut'],
    '6.2.5_ClientIM_PostHaircut': ['6.2.5_ClientIM_PostHaircut'],
    '6.2.6_ClientIM_PreHaircut': ['6.2.6_ClientIM_PreHaircut'],
    '6.2.6_ClientIM_PostHaircut': ['6.2.6_ClientIM_PostHaircut'],
    '6.2.7_ClientIM_PreHaircut': ['6.2.7_ClientIM_PreHaircut'],
    '6.2.7_ClientIM_PostHaircut': ['6.2.7_ClientIM_PostHaircut'],
    '6.2.8_ClientIM_PreHaircut': ['6.2.8_ClientIM_PreHaircut'],
    '6.2.8_ClientIM_PostHaircut': ['6.2.8_ClientIM_PostHaircut'],
    '6.2.9_ClientIM_PreHaircut': ['6.2.9_ClientIM_PreHaircut'],
    '6.2.9_ClientIM_PostHaircut': ['6.2.9_ClientIM_PostHaircut'],
    '6.2.10_ClientIM_PreHaircut': ['6.2.10_ClientIM_PreHaircut'],
    '6.2.10_ClientIM_PostHaircut': ['6.2.10_ClientIM_PostHaircut'],
    '6.2.11_ClientIM_PreHaircut': ['6.2.11_ClientIM_PreHaircut'],
    '6.2.11_ClientIM_PostHaircut': ['6.2.11_ClientIM_PostHaircut'],
    '6.2.12_ClientIM_PreHaircut': ['6.2.12_ClientIM_PreHaircut'],
    '6.2.12_ClientIM_PostHaircut': ['6.2.12_ClientIM_PostHaircut'],
    '6.2.13_ClientIM_PreHaircut': ['6.2.13_ClientIM_PreHaircut'],
    '6.2.13_ClientIM_PostHaircut': ['6.2.13_ClientIM_PostHaircut'],
    '6.2.14_ClientIM_PreHaircut': ['6.2.14_ClientIM_PreHaircut'],
    '6.2.14_ClientIM_PostHaircut': ['6.2.14_ClientIM_PostHaircut'],
    '6.2.15_ClientIM_PreHaircut': ['6.2.15_ClientIM_PreHaircut'],
    '6.2.15_ClientIM_PostHaircut': ['6.2.15_ClientIM_PostHaircut'],

    'TotalIM_6.2.1_PreHaircut': ['6.2.1_TotalIM_PreHaircut', '6.2.1_PreHaircut', 'TotalIM_6.2.1_PreHaircut_1'],
    'TotalIM_6.2.1_PostHaircut': ['6.2.1_TotalIM_PostHaircut', '6.2.1_PostHaircut', 'TotalIM_6.2.1_PostHaircut_1'],
    'TotalIM_6.2.2_PreHaircut': ['6.2.2_TotalIM_PreHaircut', '6.2.2_PreHaircut', 'TotalIM_6.2.2_PreHaircut_1'],
    'TotalIM_6.2.2_PostHaircut': ['6.2.2_TotalIM_PostHaircut', '6.2.2_PostHaircut', 'TotalIM_6.2.2_PostHaircut_1'],
    'TotalIM_6.2.3_PreHaircut': ['6.2.3_TotalIM_PreHaircut', '6.2.3_PreHaircut', 'TotalIM_6.2.3_PreHaircut_1'],
    'TotalIM_6.2.3_PostHaircut': ['6.2.3_TotalIM_PostHaircut', '6.2.3_PostHaircut', 'TotalIM_6.2.3_PostHaircut_1'],
    'TotalIM_6.2.4_PreHaircut': ['6.2.4_TotalIM_PreHaircut', '6.2.4_PreHaircut', 'TotalIM_6.2.4_PreHaircut_1'],
    'TotalIM_6.2.4_PostHaircut': ['6.2.4_TotalIM_PostHaircut', '6.2.4_PostHaircut', 'TotalIM_6.2.4_PostHaircut_1'],
    'TotalIM_6.2.5_PreHaircut': ['6.2.5_TotalIM_PreHaircut', '6.2.5_PreHaircut', 'TotalIM_6.2.5_PreHaircut_1'],
    'TotalIM_6.2.5_PostHaircut': ['6.2.5_TotalIM_PostHaircut', '6.2.5_PostHaircut', 'TotalIM_6.2.5_PostHaircut_1'],
    'TotalIM_6.2.6_PreHaircut': ['6.2.6_TotalIM_PreHaircut', '6.2.6_PreHaircut', 'TotalIM_6.2.6_PreHaircut_1'],
    'TotalIM_6.2.6_PostHaircut': ['6.2.6_TotalIM_PostHaircut', '6.2.6_PostHaircut', 'TotalIM_6.2.6_PostHaircut_1'],
    'TotalIM_6.2.7_PreHaircut': ['6.2.7_TotalIM_PreHaircut', '6.2.7_PreHaircut', 'TotalIM_6.2.7_PreHaircut_1'],
    'TotalIM_6.2.7_PostHaircut': ['6.2.7_TotalIM_PostHaircut', '6.2.7_PostHaircut', 'TotalIM_6.2.7_PostHaircut_1'],
    'TotalIM_6.2.8_PreHaircut': ['6.2.8_TotalIM_PreHaircut', '6.2.8_PreHaircut', 'TotalIM_6.2.8_PreHaircut_1'],
    'TotalIM_6.2.8_PostHaircut': ['6.2.8_TotalIM_PostHaircut', '6.2.8_PostHaircut', 'TotalIM_6.2.8_PostHaircut_1'],
    'TotalIM_6.2.9_PreHaircut': ['6.2.9_TotalIM_PreHaircut', '6.2.9_PreHaircut', 'TotalIM_6.2.9_PreHaircut_1'],
    'TotalIM_6.2.9_PostHaircut': ['6.2.9_TotalIM_PostHaircut', '6.2.9_PostHaircut', 'TotalIM_6.2.9_PostHaircut_1'],
    'TotalIM_6.2.10_PreHaircut': ['6.2.10_TotalIM_PreHaircut', '6.2.10_PreHaircut', 'TotalIM_6.2.10_PreHaircut_1'],
    'TotalIM_6.2.10_PostHaircut': ['6.2.10_TotalIM_PostHaircut', '6.2.10_PostHaircut', 'TotalIM_6.2.10_PostHaircut_1'],
    'TotalIM_6.2.11_PreHaircut': ['6.2.11_TotalIM_PreHaircut', '6.2.11_PreHaircut', 'TotalIM_6.2.11_PreHaircut_1'],
    'TotalIM_6.2.11_PostHaircut': ['6.2.11_TotalIM_PostHaircut', '6.2.11_PostHaircut', 'TotalIM_6.2.11_PostHaircut_1'],
    'TotalIM_6.2.12_PreHaircut': ['6.2.12_TotalIM_PreHaircut', '6.2.12_PreHaircut', 'TotalIM_6.2.12_PreHaircut_1'],
    'TotalIM_6.2.12_PostHaircut': ['6.2.12_TotalIM_PostHaircut', '6.2.12_PostHaircut', 'TotalIM_6.2.12_PostHaircut_1'],
    'TotalIM_6.2.13_PreHaircut': ['6.2.13_TotalIM_PreHaircut', '6.2.13_PreHaircut', 'TotalIM_6.2.13_PreHaircut_1'],
    'TotalIM_6.2.13_PostHaircut': ['6.2.13_TotalIM_PostHaircut', '6.2.13_PostHaircut', 'TotalIM_6.2.13_PostHaircut_1'],
    'TotalIM_6.2.14_PreHaircut': ['6.2.14_TotalIM_PreHaircut', '6.2.14_PreHaircut', 'TotalIM_6.2.14_PreHaircut_1'],
    'TotalIM_6.2.14_PostHaircut': ['6.2.14_TotalIM_PostHaircut', '6.2.14_PostHaircut', 'TotalIM_6.2.14_PostHaircut_1'],
    'TotalIM_6.2.15_PreHaircut': ['6.2.15_TotalIM_PreHaircut', '6.2.15_PreHaircut', 'TotalIM_6.2.15_PreHaircut_1'],
    'TotalIM_6.2.15_PostHaircut': ['6.2.15_TotalIM_PostHaircut', '6.2.15_PostHaircut', 'TotalIM_6.2.15_PostHaircut_1'],

    '7.1.2_SizeAndCompositionOfQualifyingLiquidResources': ['7.1.2_SizeAndCompositionOfQualifyingLiquidResources'],
    '7.1.3_SizeAndCompositionOfQualifyingLiquidResources': ['7.1.3_SizeAndCompositionOfQualifyingLiquidResources'],
    '7.1.4_SizeAndCompositionOfQualifyingLiquidResources': ['7.1.4_SizeAndCompositionOfQualifyingLiquidResources'],
    '7.1.5_SizeAndCompositionOfQualifyingLiquidResources': ['7.1.5_SizeAndCompositionOfQualifyingLiquidResources'],
    '7.1.6_SizeAndCompositionOfQualifyingLiquidResources': ['7.1.6_SizeAndCompositionOfQualifyingLiquidResources'],
    '7.1.7_SizeAndCompositionOfQualifyingLiquidResources': ['7.1.7_SizeAndCompositionOfQualifyingLiquidResources'],
    '7.1.8_SizeAndCompositionOfQualifyingLiquidResources': ['7.1.8_SizeAndCompositionOfQualifyingLiquidResources'],
    '7.1.9_SizeAndCompositionOfQualifyingLiquidResources': ['7.1.9_SizeAndCompositionOfQualifyingLiquidResources'],

    '7.3.1_PaymentObligationMax': ['7.3.1_PaymentObligationMax'],
    '7.3.4_PaymentObligationMax': ['7.3.4_PaymentObligationMax'],
    '7.3.5_PaymentObligationMax': ['7.3.5_PaymentObligationMax'],
    '7.3.1_SameDayPayment_Total': ['7.3.1_SameDayPayment_Total'],
    '7.3.4_SameDayPayment_Total': ['7.3.4_SameDayPayment_Total'],
    '7.3.5_SameDayPayment_Total': ['7.3.5_SameDayPayment_Total'],
    '7.3.1_IntraDayPayment_Total': ['7.3.1_IntraDayPayment_Total'],
    '7.3.4_IntraDayPayment_Total': ['7.3.4_IntraDayPayment_Total'],
    '7.3.5_IntraDayPayment_Total': ['7.3.5_IntraDayPayment_Total'],
    '7.3.1_MultiDayPayment_Total': ['7.3.1_MultiDayPayment_Total'],
    '7.3.4_MultiDayPayment_Total': ['7.3.4_MultiDayPayment_Total'],
    '7.3.5_MultiDayPayment_Total': ['7.3.5_MultiDayPayment_Total'],
    '7.3.1_SameDayPayment': ['7.3.1_SameDayPayment'],
    '7.3.4_SameDayPayment': ['7.3.4_SameDayPayment'],
    '7.3.5_SameDayPayment': ['7.3.5_SameDayPayment'],
    '7.3.1_IntraDayPayment': ['7.3.1_IntraDayPayment'],
    '7.3.4_IntraDayPayment': ['7.3.4_IntraDayPayment'],
    '7.3.5_IntraDayPayment': ['7.3.5_IntraDayPayment'],
    '7.3.1_MultiDayPayment': ['7.3.1_MultiDayPayment'],
    '7.3.4_MultiDayPayment': ['7.3.4_MultiDayPayment'],
    '7.3.5_MultiDayPayment': ['7.3.5_MultiDayPayment'],

    # 20.x
    '20.1.1': ['20.1.1', '20_1_1'],
    '20.2.1': ['20.2.1', '20_2_1'],
    '20.3.1': ['20.3.1_nan', '20_3_1', '20.3.1'],
    '20.3.1_PreHaircut': ['20.3.1_PreHaircut'],
    '20.3.1_PostHaircut': ['20.3.1_PostHaircut'],
    '20.4.1.1': ['20.4.1.1', '20_4_1_1'],
    '20.4.1.2': ['20.4.1.2', '20_4_1_2'],
    '20.4.1.3': ['20.4.1.3', '20_4_1_3'],
    '20.4.2': ['20.4.2', '20_4_2'],
    '20.4.3': ['20.4.3', '20_4_3'],
    '20.5.1.1': ['20.5.1.1', '20_5_1_1'],
    '20.5.1.2': ['20.5.1.2', '20_5_1_2'],
    '20.6.1.1': ['20.6.1.1', '20_6_1_1'],
    '20.6.1.2': ['20.6.1.2', '20_6_1_2'],
    '20.7.1': ['20.7.1', '20_7_1'],
    '20.7.2': ['20.7.2', '20_7_2'],
}


def build_23x_totals_and_drop_parts(df: pd.DataFrame) -> pd.DataFrame:
    
    base_prefixes = [
        "23.1.1", "23.1.2", 
        "23.2.1", "23.2.2", "23.2.3", "23.2.4", 
        "23.3.1", "23.3.2"
    ]
    
    
    norm_map = {str(c).strip(): c for c in df.columns}
    
    for prefix in base_prefixes:
        base_col = norm_map.get(prefix)
        
        
        part_cols = [real_name for norm_name, real_name in norm_map.items() 
                     if norm_name.startswith(f"{prefix}_") and not norm_name.endswith("_total")]
        
        if not part_cols and base_col is None:
            continue
            
        logging.info(f"Aggregiere Variable {prefix} ({len(part_cols)} Unterkategorien gefunden)")
        
        total = None
        
        if part_cols:
            parts_numeric = df[part_cols].apply(pd.to_numeric, errors="coerce")
            total = parts_numeric.sum(axis=1, skipna=True, min_count=1)
            
        
        if base_col is not None:
            base_values = pd.to_numeric(df[base_col], errors="coerce")
            if total is None:
                total = base_values
            else:
                
                total = total.fillna(base_values)
                
        
        df[f"{prefix}_total"] = total
        
        
        cols_to_drop = part_cols + ([base_col] if base_col else [])
        df.drop(columns=cols_to_drop, inplace=True, errors="ignore")
        
    return df



def standardize_columns_using_map(df: pd.DataFrame, column_map: dict) -> pd.DataFrame:

    df = df.copy()

    for target, aliases in column_map.items():
        
        norm_map = {str(c).strip(): c for c in df.columns}

        candidates = []

        
        if target in df.columns:
            candidates.append(target)

       
        for alias in aliases:
            real_col = norm_map.get(str(alias).strip())
            if real_col is not None and real_col not in candidates and real_col in df.columns:
                candidates.append(real_col)

        if not candidates:
            continue

        
        candidates = [c for c in candidates if c in df.columns]

        if not candidates:
            continue

        
        if len(candidates) == 1:
            df[target] = df[candidates[0]]
        else:
            df[target] = df[candidates].bfill(axis=1).iloc[:, 0]

        
        drop_cols = [c for c in candidates if c != target]
        if drop_cols:
            df.drop(columns=drop_cols, inplace=True, errors="ignore")

    return df

def combine_ccp_datasets(input_folder, output_path):
    all_files = sorted(
    [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.xlsx')]
    )
    frames = []

    for file in all_files:
        try:
           
            df = pd.read_excel(file)
            logging.info(f"LOADING: {os.path.basename(file)}")
            frames.append(df)
        except Exception as e:
            logging.error(f"ERROR WHILE LOADING {file}: {e}")

    if not frames:
        logging.warning("NO FILES FOUND")
        return

    combined = pd.concat(frames, ignore_index=True)

   
    combined = build_23x_totals_and_drop_parts(combined)

    
    combined = standardize_columns_using_map(combined, column_map)

   
    base_prefixes = ["23.1.1", "23.1.2", "23.2.1", "23.2.2", "23.2.3", "23.2.4", "23.3.1", "23.3.2"]
    total_cols = [f"{p}_total" for p in base_prefixes]

    allowed_cols = set(column_map.keys()) | set(total_cols)
    keep = [c for c in combined.columns if c in allowed_cols]
    combined = combined[keep]

    
    meta = ['ReportDate', 'CCP', 'ClearingService', 'DefaultFund', 'Currency']
    existing_meta = [c for c in meta if c in combined.columns]
    
    
    existing_totals = [c for c in total_cols if c in combined.columns]
    
   
    others = [c for c in combined.columns if c not in existing_meta and c not in existing_totals]
    
    combined = combined[existing_meta + existing_totals + others]

    
    combined.to_excel(output_path, index=False)
    logging.info(f"Erfolgreich gespeichert unter: {output_path}")


if __name__ == "__main__":
    combine_ccp_datasets(DIRECTORY, OUTPUT)