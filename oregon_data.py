"""
This is a program that reads a .csv file that is a compilation of data from the Oregon Health Authority found
in the COVID-19 Daily Update reports and COVID-19 Weekly Reports. The fist ste of columns are from the daily
reports, and the second set of columns is from the Weekly Reports.
"""
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

HEADER_ROWS = 4

# Column IDs
DATE = 0

COVID_19_DAILY_UPDATE = 1
TESTS = COVID_19_DAILY_UPDATE
WEEKLY_TESTS = TESTS + 1
POSITIVE = WEEKLY_TESTS + 1
PERCENT_POSITIVE = POSITIVE + 1
WEEKLY_PERCENT_POSITIVE = PERCENT_POSITIVE + 1
NEW_CASES = WEEKLY_PERCENT_POSITIVE + 1
WEEKLY_NEW_CASES = NEW_CASES + 1
CURRENTLY_HOSPITALIZED = WEEKLY_NEW_CASES + 1
CUMULATIVE_DEATHS = CURRENTLY_HOSPITALIZED + 1
NEW_DEATHS = CUMULATIVE_DEATHS + 1
WEEKLY_DEATHS = NEW_DEATHS + 1
CUMULATIVE_TESTS = WEEKLY_DEATHS + 1

COVID_19_WEEKLY_REPORT = 13
CUMULATIVE_CASES = COVID_19_WEEKLY_REPORT
CUMULATIVE_DEATHS = CUMULATIVE_CASES + 1
CUMULATIVE_HOSPITALIZATION = CUMULATIVE_DEATHS + 1
CONTACT_WITH_CONFIRMED_YES = CUMULATIVE_HOSPITALIZATION + 1
CONTACT_WITH_CONFIRMED_NO = CONTACT_WITH_CONFIRMED_YES + 1
CONGREGATE_LIVING_YES = CONTACT_WITH_CONFIRMED_NO + 1
CONGREGATE_LIVING_NO = CONGREGATE_LIVING_YES + 1
HEALTH_CARE_WORKER_YES = CONGREGATE_LIVING_NO + 1
HEALTH_CARE_WORKER_NO = HEALTH_CARE_WORKER_YES + 1
PATIENT_CARE_YES = HEALTH_CARE_WORKER_NO + 1
PATIENT_CARE_NO = PATIENT_CARE_YES + 1
TRAVEL_RELATED_YES = PATIENT_CARE_NO + 1
TRAVEL_RELATED_NO = TRAVEL_RELATED_YES + 1
UNDERLYING_CONDITIONS_YES = TRAVEL_RELATED_NO + 1
UNDERLYING_CONDITIONS_NO = UNDERLYING_CONDITIONS_YES + 1
MALE_PERCENT = UNDERLYING_CONDITIONS_NO + 1
FEMALE_PERCENT = MALE_PERCENT + 1
AGE_0_19_CASES = FEMALE_PERCENT + 1
AGE_0_19_DEATHS = AGE_0_19_CASES + 1
AGE_0_19_HOSP = AGE_0_19_DEATHS + 1
AGE_20_29_CASES = AGE_0_19_HOSP + 1
AGE_20_29_DEATHS = AGE_20_29_CASES + 1
AGE_20_29_HOSP = AGE_20_29_DEATHS + 1
AGE_30_39_CASES = AGE_20_29_HOSP + 1
AGE_30_39_DEATHS = AGE_30_39_CASES + 1
AGE_30_39_HOSP = AGE_30_39_DEATHS + 1
AGE_40_49_CASES = AGE_30_39_HOSP + 1
AGE_40_49_DEATHS = AGE_40_49_CASES + 1
AGE_40_49_HOSP = AGE_40_49_DEATHS + 1
AGE_50_59_CASES = AGE_40_49_HOSP + 1
AGE_50_59_DEATHS = AGE_50_59_CASES + 1
AGE_50_59_HOSP = AGE_50_59_DEATHS + 1
AGE_60_69_CASES = AGE_50_59_HOSP + 1
AGE_60_69_DEATHS = AGE_60_69_CASES + 1
AGE_60_69_HOSP = AGE_60_69_DEATHS + 1
AGE_70_79_CASES = AGE_60_69_HOSP + 1
AGE_70_79_DEATHS = AGE_70_79_CASES + 1
AGE_70_79_HOSP = AGE_70_79_DEATHS + 1
AGE_80_PLUS_CASES = AGE_70_79_HOSP + 1
AGE_80_PLUS_DEATHS = AGE_80_PLUS_CASES + 1
AGE_80_PLUS_HOSP = AGE_80_PLUS_DEATHS + 1
AGE_NOT_AVAIL_CASES = AGE_80_PLUS_HOSP + 1
AGE_NOT_AVAIL_DEATHS = AGE_NOT_AVAIL_CASES + 1
AGE_NOT_AVAIL_HOSP = AGE_NOT_AVAIL_DEATHS + 1
WHITE_CASES = AGE_NOT_AVAIL_HOSP + 1
WHITE_DEATHS = WHITE_CASES + 1
WHITE_HOSP = WHITE_DEATHS + 1
BLACK_CASES = WHITE_HOSP + 1
BLACK_DEATHS = BLACK_CASES + 1
BLACK_HOSP = BLACK_DEATHS + 1
ASIAN_CASES = BLACK_HOSP + 1
ASIAN_DEATHS = ASIAN_CASES + 1
ASIAN_HOSP = ASIAN_DEATHS + 1
NATIVE_CASES = ASIAN_HOSP + 1
NATIVE_DEATHS = NATIVE_CASES + 1
NATIVE_HOSP = NATIVE_DEATHS + 1
ISLAND_CASES = NATIVE_HOSP + 1
ISLAND_DEATHS = ISLAND_CASES + 1
ISLAND_HOSP = ISLAND_DEATHS + 1
OTHER_CASES = ISLAND_HOSP + 1
OTHER_DEATHS = OTHER_CASES + 1
OTHER_HOSP = OTHER_DEATHS + 1
GT1_RACE_CASES = OTHER_HOSP + 1
GT1_RACE_DEATHS = GT1_RACE_CASES + 1
GT1_RACE_HOSP = GT1_RACE_DEATHS + 1
RACE_NOT_AVAIL_CASES = GT1_RACE_HOSP + 1
RACE_NOT_AVAIL_DEATHS = RACE_NOT_AVAIL_CASES + 1
RACE_NOT_AVAIL_HOSP = RACE_NOT_AVAIL_DEATHS + 1
HISPANIC_CASES = RACE_NOT_AVAIL_HOSP + 1
HISPANIC_DEATHS = HISPANIC_CASES + 1
HISPANIC_HOSP = HISPANIC_DEATHS + 1
NON_HISPANIC_CASES = HISPANIC_HOSP + 1
NON_HISPANIC_DEATHS = NON_HISPANIC_CASES + 1
NON_HISPANIC_HOSP = NON_HISPANIC_DEATHS + 1
UNK_ETHNICITY_CASES = NON_HISPANIC_HOSP + 1
UNK_ETHNICITY_DEATHS = UNK_ETHNICITY_CASES + 1
UNK_ETHNICITY_HOSP = UNK_ETHNICITY_DEATHS + 1

def append_to_data_set(row, labels, indices, data_set, weekly_ct, what, by_what):
    total_count = 0
    for i in range(len(labels)):
        count = int(row[indices[i]])
        data_set[i].append(count)
        total_count += count
    if weekly_ct != total_count:
        print(f'expected {what} by {by_what} to sum to {weekly_ct}, summed to {total_count}')


def strip_graph_data_set(labels, data_set, title):
    plt.clf()
    plt.title(title)
    plt.xlabel('week')
    plt.ylabel('percentage')
    # Make data
    data = pd.DataFrame({labels[i]: data_set[i] for i in range(len(labels))},
                        index=range(1, len(data_set[0]) + 1))
    # We need to transform the data from raw data to percentage (fraction)
    as_percent = data.divide(data.sum(axis=1), axis=0)
    # Make the plot
    plt.stackplot(range(1, len(data_set[0]) + 1), *[as_percent[label] for label in labels], labels=labels)
    plt.legend(loc='upper left')
    plt.margins(0, 0)
    plt.show()
    plt.pause(0.1)


weekly_cases = []
weekly_hosp = []
weekly_deaths = []

# The weekly summary  reported by age
age_labels = ['0-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80+', 'unknown']
CASES_BY_AGE_INDS = [AGE_0_19_CASES, AGE_20_29_CASES, AGE_30_39_CASES, AGE_40_49_CASES, AGE_50_59_CASES,
                     AGE_60_69_CASES, AGE_70_79_CASES, AGE_80_PLUS_CASES, AGE_NOT_AVAIL_CASES]
cases_by_age = [[] for _ in age_labels]

HOSP_BY_AGE_INDS = [AGE_0_19_HOSP, AGE_20_29_HOSP, AGE_30_39_HOSP, AGE_40_49_HOSP, AGE_50_59_HOSP,
                    AGE_60_69_HOSP, AGE_70_79_HOSP, AGE_80_PLUS_HOSP, AGE_NOT_AVAIL_HOSP]
hosp_by_age = [[] for _ in age_labels]

DEATHS_BY_AGE_INDS = [AGE_0_19_DEATHS, AGE_20_29_DEATHS, AGE_30_39_DEATHS, AGE_40_49_DEATHS, AGE_50_59_DEATHS,
                      AGE_60_69_DEATHS, AGE_70_79_DEATHS, AGE_80_PLUS_DEATHS, AGE_NOT_AVAIL_DEATHS]
deaths_by_age = [[] for _ in age_labels]

# weekly summary reported by race
race_labels = ['white', 'black', 'asian', 'native', 'islander', 'other', '>1 race', 'unknown']
CASES_BY_RACE_INDS = [WHITE_CASES, BLACK_CASES, ASIAN_CASES, NATIVE_CASES,
                      ISLAND_CASES, OTHER_CASES, GT1_RACE_CASES, RACE_NOT_AVAIL_CASES]
cases_by_race = [[] for _ in race_labels]

HOSP_BY_RACE_INDS = [WHITE_HOSP, BLACK_HOSP, ASIAN_HOSP, NATIVE_HOSP,
                     ISLAND_HOSP, OTHER_HOSP, GT1_RACE_HOSP, RACE_NOT_AVAIL_HOSP]
hosp_by_race = [[] for _ in race_labels]

DEATHS_BY_RACE_INDS = [WHITE_DEATHS, BLACK_DEATHS, ASIAN_DEATHS, NATIVE_DEATHS,
                       ISLAND_DEATHS, OTHER_DEATHS, GT1_RACE_DEATHS, RACE_NOT_AVAIL_DEATHS]
deaths_by_race = [[] for _ in race_labels]

# weekly summary reported by ethnicity
ethnicity_labels = ['hispanic','non-hispanic', 'unknown']
CASES_BY_ETHNICITY_INDS = [HISPANIC_CASES, NON_HISPANIC_CASES, UNK_ETHNICITY_CASES]
cases_by_ethnicity = [[] for _ in ethnicity_labels]

HOSP_BY_ETHNICITY_INDS = [HISPANIC_HOSP, NON_HISPANIC_HOSP, UNK_ETHNICITY_HOSP]
hosp_by_ethnicity = [[] for _ in ethnicity_labels]

DEATHS_BY_ETHNICITY_INDS = [HISPANIC_DEATHS, NON_HISPANIC_DEATHS, UNK_ETHNICITY_DEATHS]
deaths_by_ethnicity = [[] for _ in ethnicity_labels]

with open('./data/oregon/oregon.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    row_index = 0
    for row in reader:
        row_index += 1
        if row_index <= HEADER_ROWS:
            # skip the header rows
            continue

        if row[CUMULATIVE_CASES] != '':
            # This is a weekly report row - accumulate weekly data for plotting.
            this_weeks_cases = int(row[CUMULATIVE_CASES])
            print(f'{row[DATE]} {this_weeks_cases}')
            weekly_cases.append(this_weeks_cases)
            append_to_data_set(row, age_labels, CASES_BY_AGE_INDS, cases_by_age, this_weeks_cases,
                               'cases', 'age')
            append_to_data_set(row, race_labels, CASES_BY_RACE_INDS, cases_by_race, this_weeks_cases,
                               'cases', 'race')
            append_to_data_set(row, ethnicity_labels, CASES_BY_ETHNICITY_INDS, cases_by_ethnicity,
                               this_weeks_cases, 'cases', 'ethnicity')

            if row[AGE_0_19_DEATHS] != '':
                this_weeks_hosp = int(row[CUMULATIVE_HOSPITALIZATION])
                this_weeks_death = int(row[CUMULATIVE_DEATHS])
                append_to_data_set(row, age_labels, HOSP_BY_AGE_INDS, hosp_by_age, this_weeks_hosp,
                                   'hospitalizations', 'age')
                append_to_data_set(row, age_labels, DEATHS_BY_AGE_INDS, deaths_by_age, this_weeks_death,
                                   'deaths', 'age')
                append_to_data_set(row, race_labels, HOSP_BY_RACE_INDS, hosp_by_race, this_weeks_hosp,
                                   'hospitalizations', 'race')
                append_to_data_set(row, race_labels, DEATHS_BY_RACE_INDS, deaths_by_race, this_weeks_death,
                                   'deaths', 'race')
                append_to_data_set(row, ethnicity_labels, HOSP_BY_ETHNICITY_INDS, hosp_by_ethnicity,
                                   this_weeks_hosp, 'hospitalizations', 'ethnicity')
                append_to_data_set(row, ethnicity_labels, DEATHS_BY_ETHNICITY_INDS, deaths_by_ethnicity,
                                   this_weeks_death, 'deaths', 'ethnicity')

strip_graph_data_set(age_labels, cases_by_age, 'Cases by Age')
strip_graph_data_set(age_labels, hosp_by_age, 'Hospitalizations by Age')
strip_graph_data_set(age_labels, deaths_by_age, 'Deaths by Age')

strip_graph_data_set(race_labels, cases_by_race, 'Cases by Race')
strip_graph_data_set(race_labels, hosp_by_race, 'Hospitalizations by Race')
strip_graph_data_set(race_labels, deaths_by_race, 'Deaths by Race')

strip_graph_data_set(ethnicity_labels, cases_by_ethnicity, 'Cases by Ethnicity')
strip_graph_data_set(ethnicity_labels, hosp_by_ethnicity, 'Hospitalizations by Ethnicity')
strip_graph_data_set(ethnicity_labels, deaths_by_ethnicity, 'Deaths by Ethnicity')
