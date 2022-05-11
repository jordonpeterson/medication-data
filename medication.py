"""
Create a function that returns true if ALL of the following conditions are met:
(1) Drug group A, B, C and D overlap by 7 or more days consecutively. For All Drugs
(2) The last day of the overlap must be within 30 days look back from 03/31.
   Jan                            Feb                         March
                                                        1234567890123456789012345678901234567
   123456789012345678901234567890112345678901234567890123456781234567890123456789012345678901
1: 111111111111111111111111    111111111111111111111111111111
2:                                                          11111
3:                                                111111111111111111111111111111
4:                                   111111111111111111111111111111
5:                                111111111111111111111111111111   111111111111111111111111111111
"""

"""
MORE HINT
|------------Jan---------------|------------Feb-------------|-----------Mar---------------|
1234567890123456789012345678901123456789012345678901234567891234567890123456789012345678901
0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
1111111111111111111111100000111111111111111111111111111111000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000001111100000000000000000000000000000
0000000000000000000000000000000000000000000000011111111111111111111111111111100000000000000
0000000000000000000000000000000000000000000001111111111111111111111111111110000000000000000
0000000000000000000000000000000111111111111111111111111111111000011111111111111111111111111  


A: 1111111100000000000000000000000000000
B: 1111111111111111111111100000000000000
C: 1111111111111111111110000000000000000
D: 1111111000011111111111111111111111111
S: 4444444322233333333332211111111111111
"""

from datetime import datetime, timedelta
import copy


def str_to_date(date_str) -> datetime:
    return datetime.strptime(date_str, '%Y-%m-%d')


def sets_overlap(setA, setB) -> bool:
    overlap = set(setA).intersection(set(setB))
    return len(overlap) > 0


def calculate_consecutive_fill_periods_for_drugs(med):
    drug_period = calculate_fill_periods_for_drugs(med)
    med['concurrentDrugPeriods'] = calculate_overlapping_fill_periods_for_drug(drug_period)


def calculate_overlapping_fill_periods_for_drug(fill_periods) -> list:
    """
    Calculates lists of concurrent periods out of a list of datetimes
    :param fill_periods: A list of datetimes
    :rtype: list of lists of datetimes
    """
    list_of_streaks = []
    fill_periods.sort()
    while len(fill_periods) > 0:
        longest_concurrent_streak = [fill_periods.pop(0)]
        copied_list = copy.deepcopy(fill_periods)
        for date in copied_list:
            last_concurrent_date_in_sequence = longest_concurrent_streak[-1]
            if last_concurrent_date_in_sequence == date:
                continue
            if last_concurrent_date_in_sequence + timedelta(days=1) == date:
                fill_periods.remove(date)
                longest_concurrent_streak.append(date)
        list_of_streaks.append(longest_concurrent_streak)

    return list_of_streaks


def calculate_fill_periods_for_drugs(med) -> list:
    """
    Determines what days a patient is estimated to have taken medication on
    :rtype: list of datetimes
    """
    fill_periods = []
    for fill in med['fills']:
        initial_fill_date = str_to_date(fill['fillDate'])
        days_supply = int(fill['daysSupply'])
        for day in range(days_supply):
            fill_periods.append(initial_fill_date + timedelta(days=day))
    return fill_periods


def calculate_overlap_period(end_date, num_days_look_back) -> list:
    """
    :rtype: list of datetimes
    """
    relevant_drug_periods = []
    end = str_to_date(end_date)
    lookback = int(num_days_look_back) + 1
    for day in range(lookback):
        relevant_drug_periods.append(end - timedelta(days=day))
    return relevant_drug_periods


def are_drugs_overlapping(meds, target_drug_groups, min_overlap_days, num_days_lookback, end_date) -> bool:
    """
    :param meds: List of dict presenting a medication.
    :param target_drug_groups: Set. Containing target drug groups.
    :param min_overlap_days: int. Minimum number of days when all target drug groups overlap
    :param num_days_lookback: int. Number of days from end_date in which the last day of overlap must occurred.
    :param end_date: datetime. Reference date.
    """
    relevant_drug_period = calculate_overlap_period(end_date, num_days_lookback)
    for med in meds:
        calculate_consecutive_fill_periods_for_drugs(med)
        if sets_overlap(med['drugGroup'], target_drug_groups) and check_if_periods_overlap(relevant_drug_period,
                                                                                           med,
                                                                                           min_overlap_days):
            return True

    return False


def check_if_periods_overlap(relevant_drug_period, med, min_overlap_days) -> bool:
    """

    :param relevant_drug_period: list of days in relevant drug period
    :param med: list of medications containing a concurrentDrugPeriods: list
    :param min_overlap_days: integer
    :return: boolean
    """
    for overlap in med['concurrentDrugPeriods']:
        overlapping_period = set(overlap).intersection(relevant_drug_period)
        if len(overlapping_period) >= min_overlap_days:
            return True
    return False
