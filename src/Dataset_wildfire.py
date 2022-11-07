from __future__ import annotations

import string

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno
import xarray as xr
from typing import Hashable
from typing import (
    Mapping
    , Any
    , Callable
    )
from xarray.core.indexes import Index
from xarray.core.variable import Variable

class Dataset_wildfire(xr.Dataset):

    __slots__ = ()

    def __init__(
            self,
            # could make a VariableArgs to use more generally, and refine these
            # categories
            data_vars: Mapping[Any, Any] | None = None,
            coords: Mapping[Any, Any] | None = None,
            attrs: Mapping[Any, Any] | None = None,
    ) -> None:
        self.super().__init__(data_vars = data_vars, coords = coords, attrs = attrs)
        return None

    @classmethod
    def cast(cls, cast_object: xr.Dataset) -> Dataset_wildfire:
        """Cast an xarray.Dataset into a Dataset_wildfire."""
        assert isinstance(cast_object, xr.Dataset)
        cast_object.__class__ = cls
        assert isinstance(cast_object, Dataset_wildfire)
        return cast_object

    def stat_missing_data_variable(self, variable) -> string:
        return f'{variable}:' \
               f'\n\t  percentage : {self[variable].isnull().sum().values / self[variable].size * 100}' \
               f'\n\t  count : {self[variable].isnull().sum().values.ravel()[0]} / {self[variable].size}'

    def stat_missing_data(self) -> string:
        _tmp="MISSING DATA :"
        for var in list(self.keys()):
            _tmp += f'\n\t{self.stat_missing_data_variable(var)}'
        return _tmp
