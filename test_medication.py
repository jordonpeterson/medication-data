import unittest
from medication import *


class MyTestCase(unittest.TestCase):

    def test_do_two_consecutive_one_day_fill_periods_overlap(self):
        meds = [
            {
                "genericName": "overlap",
                "drugGroup": ["A", "E"],
                "fills": [
                    {
                        "fillDate": "2022-01-01",
                        "daysSupply": "1"
                    }
                ]
            },
            {
                "genericName": "overlap1",
                "drugGroup": ["A", "E"],
                "fills": [
                    {
                        "fillDate": "2022-01-02",
                        "daysSupply": "1"
                    }
                ]
            }
        ]

        res = are_drugs_overlapping(meds,
                                    {'A', 'B', 'C', 'D'},
                                    1,
                                    30,
                                    '2022-01-31')
        self.assertTrue(res)

    def test_same_day_one_day_fills_overlap(self):
        meds = [
            {
                "genericName": "overlap",
                "drugGroup": ["A", "E"],
                "fills": [
                    {
                        "fillDate": "2022-01-01",
                        "daysSupply": "1"
                    }
                ]
            },
            {
                "genericName": "overlap1",
                "drugGroup": ["A", "E"],
                "fills": [
                    {
                        "fillDate": "2022-01-01",
                        "daysSupply": "1"
                    }
                ]
            }
        ]

        res = are_drugs_overlapping(meds,
                                    {'A', 'B', 'C', 'D'},
                                    1,
                                    30,
                                    '2022-01-31')
        self.assertTrue(res)

    def test_does_not_overlap_if_drug_groups_dont_match(self):
        meds = [
            {
                "genericName": "overlap",
                "drugGroup": ["DONT", "OVERLAP"],
                "fills": [
                    {
                        "fillDate": "2022-01-01",
                        "daysSupply": "1"
                    }
                ]
            },
        ]
        res = are_drugs_overlapping(meds,
                                    {'A', 'B', 'C', 'D'},
                                    1,
                                    30,
                                    '2022-01-31')
        self.assertFalse(res)

    def test_does_not_overlap_if_there_are_less_than_required_overlapping_days_in_period(self):
        meds = [
            {
                "genericName": "overlap",
                "drugGroup": ["A", "E"],
                "fills": [
                    {
                        "fillDate": "2022-01-01",
                        "daysSupply": "1"
                    }
                ]
            },
            {
                "genericName": "overlap1",
                "drugGroup": ["A", "E"],
                "fills": [
                    {
                        "fillDate": "2022-01-02",
                        "daysSupply": "1"
                    }
                ]
            }
        ]

        res = are_drugs_overlapping(meds,
                                    {'A', 'B', 'C', 'D'},
                                    3,
                                    30,
                                    '2022-01-31')
        self.assertFalse(res)

    def test_does_not_overlap_if_a_concurrent_streak_of_days_does_not_have_sufficient_days_in_lookback_period(self):
        meds = [
            {
                "genericName": "overlap",
                "drugGroup": ["A", "E"],
                "fills": [
                    {
                        "fillDate": "2022-01-01",
                        "daysSupply": "1"
                    }
                ]
            },
            {
                "genericName": "overlap1",
                "drugGroup": ["A", "E"],
                "fills": [
                    {
                        "fillDate": "2021-12-31",
                        "daysSupply": "1"
                    }
                ]
            }
        ]

        res = are_drugs_overlapping(meds,
                                    {'A', 'B', 'C', 'D'},
                                    2,
                                    30,
                                    '2022-01-31')
        self.assertFalse(res)

    def test_overlaps_past_year_month_boundaries(self):
        meds = [
            {
                "genericName": "overlap",
                "drugGroup": ["A", "E"],
                "fills": [
                    {
                        "fillDate": "2022-01-01",
                        "daysSupply": "1"
                    },
                    {
                        "fillDate": "2021-12-31",
                        "daysSupply": "1"
                    }
                ]
            }
        ]

        res = are_drugs_overlapping(meds,
                                    {'A', 'B', 'C', 'D'},
                                    2,
                                    31,
                                    '2022-01-31')
        self.assertTrue(res)

    def test_does_not_overlap_if_target_drug_groups_is_empty(self):
        meds = [
            {
                "genericName": "overlap",
                "drugGroup": ["A", "E"],
                "fills": [
                    {
                        "fillDate": "2022-01-01",
                        "daysSupply": "30"
                    }
                ]
            }
        ]

        res = are_drugs_overlapping(meds,
                                    {},
                                    2,
                                    31,
                                    '2022-01-31')
        self.assertFalse(res)

    def test_does_not_overlap_if_multiple_drug_fill_periods_exist_in_relevant_period_but_are_not_consecutive(self):
        meds = [
            {
                "genericName": "overlap",
                "drugGroup": ["A", "E"],
                "fills": [
                    {
                        "fillDate": "2022-01-01",
                        "daysSupply": "10"
                    },
                    {
                        "fillDate": "2022-01-12",
                        "daysSupply": "10"
                    },
                    {
                        "fillDate": "2022-01-23",
                        "daysSupply": "10"
                    }
                ]
            }
        ]

        res = are_drugs_overlapping(meds,
                                    {'A', 'B', 'C', 'D'},
                                    11,
                                    31,
                                    '2022-01-31')
        self.assertFalse(res)

    def test_overlaps_past_year_month_boundaries(self):
        meds = [
            {
                "genericName": "overlap",
                "drugGroup": ["A", "E"],
                "fills": [
                    {
                        "fillDate": "2022-01-01",
                        "daysSupply": "1"
                    },
                    {
                        "fillDate": "2021-12-31",
                        "daysSupply": "1"
                    }
                ]
            }
        ]

        res = are_drugs_overlapping(meds,
                                    {'A', 'B', 'C', 'D'},
                                    2,
                                    31,
                                    '2022-01-31')
        self.assertTrue(res)

    def test_overlaps_past_year(self):
        result = are_drugs_overlapping(self.meds1,
                                       {'A', 'B', 'C', 'D'},
                                       7,
                                       30,
                                       '2020-03-31')
        self.assertTrue(result)

    def test_multiple_dates_correctly_sorted_into_array(self):
        result = calculate_fill_periods_for_drugs({"fills": [
            {
                "fillDate": "2022-01-01",
                "daysSupply": "5"
            },
            {
                "fillDate": "2022-01-06",
                "daysSupply": "5"
            },
            {
                "fillDate": "2022-01-11",
                "daysSupply": "7"
            }
        ]})
        self.assertEqual(len(result), 17)

    def test_calculate_overlap_period_of_30_days(self):
        result = calculate_overlap_period("2022-01-31", 30)
        self.assertEqual(31, len(result))
        self.assertTrue(str_to_date("2022-01-31") in result)
        self.assertTrue(str_to_date("2022-01-01") in result)
        self.assertFalse(str_to_date("2022-02-01") in result)
        self.assertFalse(str_to_date("2021-12-31") in result)

    def test_calculate_overlap_period_of_zero(self):
        result = calculate_overlap_period("2022-01-31", 0)
        self.assertEqual(1, len(result))
        self.assertTrue(str_to_date("2022-01-31") in result)

    def test_calculate_overlap_over_year_month_boundary(self):
        result = calculate_overlap_period("2022-01-01", 1)
        self.assertEqual(2, len(result))
        self.assertTrue(str_to_date("2022-01-01") in result)
        self.assertTrue(str_to_date("2021-12-31") in result)

    def test_single_dates_correctly_sorted_into_array(self):
        result = calculate_fill_periods_for_drugs({"fills": [
            {
                "fillDate": "2022-01-01",
                "daysSupply": "5"
            }
        ]})
        self.assertEqual(len(result), 5)

    def calculate_consecutive_periods_drugs_were_used(self):
        result = calculate_fill_periods_for_drugs({"fills": [
            {
                "fillDate": "2022-01-01",
                "daysSupply": "5"
            },
            {
                "fillDate": "2022-01-06",
                "daysSupply": "5"
            },
            {
                "fillDate": "2022-01-11",
                "daysSupply": "7"
            }
        ]})
        x = calculate_overlapping_fill_periods_for_drug(result)
        self.assertTrue(x)

    def test_getting_list_of_streaks(self):
        result = calculate_overlapping_fill_periods_for_drug(self.overlapping_fill_periods)
        self.assertEqual(3, len(result[0]))
        self.assertEqual(2, len(result[1]))

    def test_concurrent_drug_periods_calculated_correctly(self):
        med = {
            "genericName": "overlap",
            "drugGroup": ["A", "E"],
            "fills": [
                {
                    "fillDate": "2022-01-01",
                    "daysSupply": "7"
                }
            ]
        }
        calculate_consecutive_fill_periods_for_drugs(med)
        self.assertEqual(7, len(med['concurrentDrugPeriods'][0]))

    def test_check_if_periods_overlap_returns_true_when_there_are_dates_in_common(self):
        med = {
            "genericName": "overlap",
            "drugGroup": ["A", "E"],
            "fills": [
                {
                    "fillDate": "2022-01-01",
                    "daysSupply": "7"
                }
            ],
            'concurrentDrugPeriods': [{'2022-01-01', '2022-01-02'}]
        }
        result = check_if_periods_overlap({'2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04'}, med, 2)
        self.assertEqual(True, result)

    def test_check_if_periods_overlap_returns_false_when_there_are_not_dates_in_common(self):
        med = {
            'concurrentDrugPeriods': [{'2021-01-01', '2021-01-02'}]
        }
        result = check_if_periods_overlap({'2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04'}, med, 2)
        self.assertEqual(False, result)

    overlapping_fill_periods = [str_to_date("2022-01-01"),
                                str_to_date("2022-01-02"),
                                str_to_date("2022-01-03"),
                                str_to_date("2022-01-05"),
                                str_to_date("2022-01-06")]

    meds1 = [
        {
            "genericName": "drug1",
            "drugGroup": ["A", "E"],
            "fills": [
                {
                    "fillDate": "2019-12-25",
                    "daysSupply": "30"
                },
                {
                    "fillDate": "2020-01-29",
                    "daysSupply": "30"
                }
            ]
        },
        {
            "genericName": "drug2",
            "drugGroup": ["A"],
            "fills": [
                {
                    "fillDate": "2020-02-27",
                    "daysSupply": "5"
                }
            ]
        },
        {
            "genericName": "drug3",
            "drugGroup": ["B", "K"],
            "fills": [
                {
                    "fillDate": "2020-02-17",
                    "daysSupply": "30"
                }
            ]
        },
        {
            "genericName": "drug4",
            "drugGroup": ["C"],
            "fills": [
                {
                    "fillDate": "2020-02-15",
                    "daysSupply": "30"
                }
            ]
        },
        {
            "genericName": "drug5",
            "drugGroup": ["D"],
            "fills": [
                {
                    "fillDate": "2020-02-01",
                    "daysSupply": "30"
                },
                {
                    "fillDate": "2020-03-06",
                    "daysSupply": "30"
                }
            ]
        }
    ]


if __name__ == '__main__':
    unittest.main()
