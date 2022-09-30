import pytest  # import pytest


# definition of  test for testing the time range of a list of xarray datasets
def test_time_range(ds_list):
    # test if the time range of a list of xarray datasets is the same
    # input: ds_list: list of xarray datasets
    # output: True if the time range is the same, False if not the same
    # example: test_time_range([ds1,ds2,ds3])
    assert len(ds_list) > 1, "The length of the list should be larger than 1"
    for i in range(len(ds_list) - 1):
        assert ds_list[i].time[-1] == ds_list[i + 1].time[0], "The time range of the list is not the same"
    return True


# definition of  test for testing the time resolution is daily of a list of xarray datasets
def test_daily_resolution(ds_list):
    # test if the time resolution of a list of xarray datasets is daily
    # input: ds_list: list of xarray datasets
    # output: True if the time resolution is daily, False if not daily
    # example: test_daily_resolution([ds1,ds2,ds3])
    assert len(ds_list) >= 1, "The length of the list should equal orlarger than 1"
    for i in range(len(ds_list) - 1):
        assert ds_list[i].time[1] - ds_list[i].time[0] == '1D', "The time resolution of the list is not daily"
    return True
