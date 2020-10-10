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
NEW_CONFIRMED_CASES = WEEKLY_PERCENT_POSITIVE + 1
NEW_CASES = NEW_CONFIRMED_CASES + 1
CUMULATIVE_CASES = NEW_CASES + 1
WEEKLY_NEW_CASES = CUMULATIVE_CASES + 1
CURRENTLY_HOSPITALIZED = WEEKLY_NEW_CASES + 1
WEEKLY_AVE_HOSPITALIZED = CURRENTLY_HOSPITALIZED + 1
CURRENT_ICU = WEEKLY_AVE_HOSPITALIZED + 1
WEEKLY_AVE_ICU = CURRENT_ICU + 1
CURRENT_VENTILATORS = WEEKLY_AVE_ICU + 1
WEEKLY_AVE_VENTILATORS = CURRENT_VENTILATORS + 1
CUMULATIVE_DEATHS = WEEKLY_AVE_VENTILATORS + 1
NEW_DEATHS = CUMULATIVE_DEATHS + 1
WEEKLY_DEATHS = NEW_DEATHS + 1
CUMULATIVE_TESTS = WEEKLY_DEATHS + 1

COVID_19_WEEKLY_REPORT = 20
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
AGE_0_19_NEW = AGE_0_19_CASES + 1
AGE_0_19_DEATHS = AGE_0_19_NEW + 1
AGE_0_19_NEW_DEATHS = AGE_0_19_DEATHS + 1
AGE_0_19_HOSP = AGE_0_19_NEW_DEATHS + 1
AGE_20_29_CASES = AGE_0_19_HOSP + 1
AGE_20_29_NEW = AGE_20_29_CASES + 1
AGE_20_29_DEATHS = AGE_20_29_NEW + 1
AGE_20_29_NEW_DEATHS = AGE_20_29_DEATHS + 1
AGE_20_29_HOSP = AGE_20_29_NEW_DEATHS + 1
AGE_30_39_CASES = AGE_20_29_HOSP + 1
AGE_30_39_NEW = AGE_30_39_CASES + 1
AGE_30_39_DEATHS = AGE_30_39_NEW + 1
AGE_30_39_NEW_DEATHS = AGE_30_39_DEATHS + 1
AGE_30_39_HOSP = AGE_30_39_NEW_DEATHS + 1
AGE_40_49_CASES = AGE_30_39_HOSP + 1
AGE_40_49_NEW = AGE_40_49_CASES + 1
AGE_40_49_DEATHS = AGE_40_49_NEW + 1
AGE_40_49_NEW_DEATHS = AGE_40_49_DEATHS + 1
AGE_40_49_HOSP = AGE_40_49_NEW_DEATHS + 1
AGE_50_59_CASES = AGE_40_49_HOSP + 1
AGE_50_59_NEW = AGE_50_59_CASES + 1
AGE_50_59_DEATHS = AGE_50_59_NEW + 1
AGE_50_59_NEW_DEATHS = AGE_50_59_DEATHS + 1
AGE_50_59_HOSP = AGE_50_59_NEW_DEATHS + 1
AGE_60_69_CASES = AGE_50_59_HOSP + 1
AGE_60_69_NEW = AGE_60_69_CASES + 1
AGE_60_69_DEATHS = AGE_60_69_NEW + 1
AGE_60_69_NEW_DEATHS = AGE_60_69_DEATHS + 1
AGE_60_69_HOSP = AGE_60_69_NEW_DEATHS + 1
AGE_70_79_CASES = AGE_60_69_HOSP + 1
AGE_70_79_NEW = AGE_70_79_CASES + 1
AGE_70_79_DEATHS = AGE_70_79_NEW + 1
AGE_70_79_NEW_DEATHS = AGE_70_79_DEATHS + 1
AGE_70_79_HOSP = AGE_70_79_NEW_DEATHS + 1
AGE_80_PLUS_CASES = AGE_70_79_HOSP + 1
AGE_80_PLUS_NEW = AGE_80_PLUS_CASES + 1
AGE_80_PLUS_DEATHS = AGE_80_PLUS_NEW + 1
AGE_80_PLUS_NEW_DEATHS = AGE_80_PLUS_DEATHS + 1
AGE_80_PLUS_HOSP = AGE_80_PLUS_NEW_DEATHS + 1
AGE_NOT_AVAIL_CASES = AGE_80_PLUS_HOSP + 1
AGE_NOT_AVAIL_NEW = AGE_NOT_AVAIL_CASES + 1
AGE_NOT_AVAIL_DEATHS = AGE_NOT_AVAIL_NEW + 1
AGE_NOT_AVAIL_NEW_DEATHS = AGE_NOT_AVAIL_DEATHS + 1
AGE_NOT_AVAIL_HOSP = AGE_NOT_AVAIL_NEW_DEATHS + 1
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


def append_weekly_report_to_data_set(row, indices, data_set, weekly_ct, what, by_what):
    """
    Add te weekly data for some demographic (by age, by race, by ethnicity). While these are
    being added, sum them to make sure they sum to the case count for the week (helps identify
    data transcription errors).

    :param row: ([str], required) The row of data to be processed
    :param indices: ([int], required) The indices in the row to be added to that data set.
    :param data_set: ([[int]], required) The data set.
    :param weekly_ct: (int, required) The case count used in data validation.
    :param what: (str, required) The label of the thing being added (cases, deaths,
    hospitalizations), used in unexpected condition messaging.
    :param by_what: (str, required) The name of the demographic axis, used in unexpected
    condition messaging.
    :return:
    """
    total_count = 0
    for i in range(len(indices)):
        count = int(row[indices[i]])
        if count < 0:
            count = 0
        data_set[i].append(count)
        total_count += count
    if weekly_ct != total_count and what != 'new':
        print(f'expected {what} by {by_what} to sum to {weekly_ct}, summed to {total_count}')


def strip_graph_data_set(labels, data_set, title):
    """
    Make a strip graph of a data set. This is generally used to visualize shifts in the
    demographics

    :param labels:
    :param data_set:
    :param title:
    :return:
    """
    plt.clf()
    plt.title(title)
    plt.xlabel('week')
    plt.ylabel('count')
    # Make data
    data = pd.DataFrame({labels[i]: data_set[i] for i in range(len(labels))},
                        index=range(1, len(data_set[0]) + 1))
    # # We need to transform the data from raw data to percentage (fraction)
    # as_percent = data.divide(data.sum(axis=1), axis=0)
    # Make the plot
    tic_spacing = 2
    plt.xticks(np.arange(0, len(data_set[0]), tic_spacing))
    plt.grid(b=True, which='major', color='#aaaaff', linestyle='-')
    plt.stackplot(range(1, len(data_set[0]) + 1), *[data[label] for label in labels], labels=labels)
    plt.legend(loc='upper left')
    plt.margins(0, 0)
    plt.show()
    plt.pause(0.1)


def normalized_strip_graph_data_set(labels, data_set, title):
    """
    Make a strip graph of a data set. This is generally used to visualize shifts in the
    demographics

    :param labels:
    :param data_set:
    :param title:
    :return:
    """
    plt.clf()
    plt.title(title)
    plt.xlabel('week')
    plt.ylabel('percentage')
    tic_spacing = 2
    plt.xticks(np.arange(0, len(data_set[0]), tic_spacing))
    plt.grid(b=True, which='major', color='#aaaaff', linestyle='-')
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


weekly_tests = []
weekly_new_confirmed_cases = []
weekly_new_cases = []
weekly_ave_hospitalized = []
weekly_ave_icu = []
weekly_ave_ven = []
weekly_new_deaths = []

cum_weekly_cases = []
cum_weekly_hosp = []
cum_weekly_deaths = []

# Weekly data from daily data
# The weekly summary  reported by age
age_labels = ['0-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80+', 'unknown']
CASES_BY_AGE_INDS = [AGE_0_19_CASES, AGE_20_29_CASES, AGE_30_39_CASES, AGE_40_49_CASES, AGE_50_59_CASES,
                     AGE_60_69_CASES, AGE_70_79_CASES, AGE_80_PLUS_CASES, AGE_NOT_AVAIL_CASES]
cases_by_age = [[] for _ in age_labels]

NEW_BY_AGE_INDS = [AGE_0_19_NEW, AGE_20_29_NEW, AGE_30_39_NEW, AGE_40_49_NEW, AGE_50_59_NEW,
                   AGE_60_69_NEW, AGE_70_79_NEW, AGE_80_PLUS_NEW, AGE_NOT_AVAIL_NEW]
new_by_age = [[] for _ in age_labels]

NEW_DEATHS_BY_AGE_INDS = [AGE_0_19_NEW_DEATHS, AGE_20_29_NEW_DEATHS, AGE_30_39_NEW_DEATHS, AGE_40_49_NEW_DEATHS,
                          AGE_50_59_NEW_DEATHS, AGE_60_69_NEW_DEATHS, AGE_70_79_NEW_DEATHS, AGE_80_PLUS_NEW_DEATHS,
                          AGE_NOT_AVAIL_NEW_DEATHS]
new_deaths_by_age = [[] for _ in age_labels]

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
ethnicity_labels = ['hispanic', 'non-hispanic', 'unknown']
CASES_BY_ETHNICITY_INDS = [HISPANIC_CASES, NON_HISPANIC_CASES, UNK_ETHNICITY_CASES]
cases_by_ethnicity = [[] for _ in ethnicity_labels]

HOSP_BY_ETHNICITY_INDS = [HISPANIC_HOSP, NON_HISPANIC_HOSP, UNK_ETHNICITY_HOSP]
hosp_by_ethnicity = [[] for _ in ethnicity_labels]

DEATHS_BY_ETHNICITY_INDS = [HISPANIC_DEATHS, NON_HISPANIC_DEATHS, UNK_ETHNICITY_DEATHS]
deaths_by_ethnicity = [[] for _ in ethnicity_labels]

with open('./data/oregon/oregon.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    row_index = 0
    last_weeks_death = 0
    for row in reader:
        row_index += 1
        if row_index <= HEADER_ROWS:
            # skip the header rows
            continue

        if row[TESTS] != '' and row[WEEKLY_TESTS] != '':
            # This is a weekly average or newly added value that we computed from the daily values
            weekly_growth = row[WEEKLY_NEW_CASES]
            print(f'Weekly from dailies {row[DATE]} {weekly_growth}')
            weekly_tests.append(int(row[WEEKLY_TESTS].replace(',', '')))
            # weekly_new_confirmed_cases = []
            weekly_new_cases.append(int(weekly_growth.replace(',', '')))
            weekly_ave_hospitalized.append(float(row[WEEKLY_AVE_HOSPITALIZED]))
            weekly_ave_icu.append(0.0 if row[WEEKLY_AVE_ICU] == '' else float(row[WEEKLY_AVE_ICU]))
            weekly_ave_ven.append(0.0 if row[WEEKLY_AVE_VENTILATORS] == '' else float(row[WEEKLY_AVE_VENTILATORS]))
            weekly_new_deaths.append(int(row[WEEKLY_DEATHS].replace(',', '')))

        if row[CUMULATIVE_CASES] != '':
            # This is a weekly report row - accumulate weekly data for plotting.
            this_weeks_cases = int(row[CUMULATIVE_CASES])
            print(f'Weekly Summary Report {row[DATE]} {this_weeks_cases}')
            cum_weekly_cases.append(this_weeks_cases)
            append_weekly_report_to_data_set(row, CASES_BY_AGE_INDS, cases_by_age, this_weeks_cases,
                                             'cases', 'age')
            append_weekly_report_to_data_set(row, NEW_BY_AGE_INDS, new_by_age, this_weeks_cases,
                                             'new', 'age')
            append_weekly_report_to_data_set(row, CASES_BY_RACE_INDS, cases_by_race, this_weeks_cases,
                                             'cases', 'race')
            append_weekly_report_to_data_set(row, CASES_BY_ETHNICITY_INDS, cases_by_ethnicity,
                                             this_weeks_cases, 'cases', 'ethnicity')

            if row[AGE_0_19_DEATHS] != '':
                # This is a weekly report that includes hospitalizations and deaths for the cases by ages,
                # cases by race, and cases by ethnicity.
                this_weeks_hosp = int(row[CUMULATIVE_HOSPITALIZATION])
                cum_weekly_hosp.append(this_weeks_hosp)
                this_weeks_death = int(row[CUMULATIVE_DEATHS])
                cum_weekly_deaths.append(this_weeks_death)
                append_weekly_report_to_data_set(row, HOSP_BY_AGE_INDS, hosp_by_age, this_weeks_hosp,
                                                 'hospitalizations', 'age')
                append_weekly_report_to_data_set(row, DEATHS_BY_AGE_INDS, deaths_by_age, this_weeks_death,
                                                 'deaths', 'age')
                append_weekly_report_to_data_set(row, NEW_DEATHS_BY_AGE_INDS, new_deaths_by_age,
                                                 this_weeks_death - last_weeks_death,
                                                 'new deaths', 'age')
                append_weekly_report_to_data_set(row, HOSP_BY_RACE_INDS, hosp_by_race, this_weeks_hosp,
                                                 'hospitalizations', 'race')
                append_weekly_report_to_data_set(row, DEATHS_BY_RACE_INDS, deaths_by_race, this_weeks_death,
                                                 'deaths', 'race')
                append_weekly_report_to_data_set(row, HOSP_BY_ETHNICITY_INDS, hosp_by_ethnicity,
                                                 this_weeks_hosp, 'hospitalizations', 'ethnicity')
                append_weekly_report_to_data_set(row, DEATHS_BY_ETHNICITY_INDS, deaths_by_ethnicity,
                                                 this_weeks_death, 'deaths', 'ethnicity')
                last_weeks_death = this_weeks_death

plt.clf()
plt.title('weekly summary')
plt.xlabel('week')
plt.ylabel('count')
plt.grid(b=True, which='major', color='#aaaaff', linestyle='-')
plt.plot(weekly_new_cases, label='weekly new cases')
plt.plot(weekly_ave_hospitalized, label='ave hospitalized')
plt.plot(weekly_ave_icu, label='ave ICU')
plt.plot(weekly_ave_ven, label='ave intubated')
plt.plot(weekly_new_deaths, label='weekly new deaths')
plt.legend()
plt.show()
plt.pause(0.1)

# strip_graph_data_set(age_labels, cases_by_age, 'Cumulative Cases by Age')
normalized_strip_graph_data_set(age_labels, cases_by_age, 'Cumulative Cases by Age')
normalized_strip_graph_data_set(age_labels, new_by_age, 'Weekly Cases by Age')
# strip_graph_data_set(age_labels, deaths_by_age, 'Cumulative Deaths by Age')
normalized_strip_graph_data_set(age_labels, deaths_by_age, 'Deaths by Age')
normalized_strip_graph_data_set(age_labels, new_deaths_by_age, 'Weekly Deaths by Age')
# strip_graph_data_set(age_labels, hosp_by_age, 'Cumulative Hospitalizations by Age')
normalized_strip_graph_data_set(age_labels, hosp_by_age, 'Hospitalizations by Age')

# strip_graph_data_set(race_labels, cases_by_race, 'Cumulative Cases by Race')
# normalized_strip_graph_data_set(race_labels, cases_by_race, 'Cases by Race')
# strip_graph_data_set(race_labels, hosp_by_race, 'Cumulative Hospitalizations by Race')
# normalized_strip_graph_data_set(race_labels, hosp_by_race, 'Hospitalizations by Race')
# strip_graph_data_set(race_labels, deaths_by_race, 'Cumulative Deaths by Race')
# normalized_strip_graph_data_set(race_labels, deaths_by_race, 'Deaths by Race')

# strip_graph_data_set(ethnicity_labels, cases_by_ethnicity, 'Cumulative Cases by Ethnicity')
# normalized_strip_graph_data_set(ethnicity_labels, cases_by_ethnicity, 'Cases by Ethnicity')
# strip_graph_data_set(ethnicity_labels, hosp_by_ethnicity, 'Cumulative Hospitalizations by Ethnicity')
# normalized_strip_graph_data_set(ethnicity_labels, hosp_by_ethnicity, 'Hospitalizations by Ethnicity')
# strip_graph_data_set(ethnicity_labels, deaths_by_ethnicity, 'Cumulative Deaths by Ethnicity')
# normalized_strip_graph_data_set(ethnicity_labels, deaths_by_ethnicity, 'Deaths by Ethnicity')
