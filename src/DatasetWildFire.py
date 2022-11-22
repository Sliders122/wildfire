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


class DatasetWildFire(xr.Dataset):
    """
    A multi-dimensional, in memory, array database extended from Xarray.Dataset.
    It is used specifically to process data for the WildFire Project.

    A dataset resembles an in-memory representation of a NetCDF file, and consists of variables, coordinates and
     attributes which together form a self describing dataset.
    Dataset implements the mapping interface with keys given by variable names and values given by DataArray objects for
     each variable name.
    One dimensional variables with name equal to their dimension are index coordinates used for label based indexing.

    To load data from a file or file-like object, use the open_dataset function.

    Parameters
    ----------

    data_vars : dict-like, optional
        A mapping from variable names to :py:class:`~xarray.DataArray`
        objects, :py:class:`~xarray.Variable` objects or to tuples of
        the form ``(dims, data[, attrs])`` which can be used as
        arguments to create a new ``Variable``. Each dimension must
        have the same length in all variables in which it appears.
        The following notations are accepted:
        - mapping {var name: DataArray}
        - mapping {var name: Variable}
        - mapping {var name: (dimension name, array-like)}
        - mapping {var name: (tuple of dimension names, array-like)}
        - mapping {dimension name: array-like}
          (it will be automatically moved to coords, see below)
        Each dimension must have the same length in all variables in
        which it appears.

    coords : dict-like, optional
        Another mapping in similar form as the `data_vars` argument,
        except the each item is saved on the dataset as a "coordinate".
        These variables have an associated meaning: they describe
        constant/fixed/independent quantities, unlike the
        varying/measured/dependent quantities that belong in
        `variables`. Coordinates values may be given by 1-dimensional
        arrays or scalars, in which case `dims` do not need to be
        supplied: 1D arrays will be assumed to give index values along
        the dimension with the same name.
        The following notations are accepted:
        - mapping {coord name: DataArray}
        - mapping {coord name: Variable}
        - mapping {coord name: (dimension name, array-like)}
        - mapping {coord name: (tuple of dimension names, array-like)}
        - mapping {dimension name: array-like}
          (the dimension name is implicitly set to be the same as the
          coord name)
        The last notation implies that the coord name is the same as
        the dimension name.

    attrs : dict-like, optional
        Global attributes to save on this dataset.

    """

    __slots__ = ()

    def __init__(
            self,
            # could make a VariableArgs to use more generally, and refine these
            # categories
            data_vars: Mapping[Any, Any] | None = None,
            coords: Mapping[Any, Any] | None = None,
            attrs: Mapping[Any, Any] | None = None,
    ) -> None:
        self.super().__init__(data_vars=data_vars, coords=coords, attrs=attrs)

    @classmethod
    def cast(cls, cast_object: xr.Dataset) -> DatasetWildFire:
        """
        Cast an xarray.Dataset into a DatasetWildFire.

        Parameters
        ----------
        cast_object : xr.Dataset
            The Xarray.Dataset that needs to be cast

        Return: DatasetWildFire
        ---------
        The new object
        """
        assert isinstance(cast_object, xr.Dataset)
        cast_object.__class__ = cls
        assert isinstance(cast_object, DatasetWildFire)
        return cast_object

    def stat_print_missing_data_variable(self, variable: string) -> string:
        """
        Statistical methods used to print the percentage and number of missing data for a given variable of the Dataset

        Parameters
        ----------
        variable : string
            The variable on which we want to return the stats

        Return: string
        ---------
        The formatted string used to print the information
        """
        return f'{variable}:' \
               f'\n\t  percentage : {self[variable].isnull().sum().values / self[variable].size * 100}' \
               f'\n\t  count : {self[variable].isnull().sum().values.ravel()[0]} / {self[variable].size}'

    def stat_print_missing_data(self) -> string:
        """
        Statistical methods used to print the percentage and number of missing data for every variables of the Dataset

        Return: string
        ---------
        The formatted string used to print the information
        """
        _tmp = "MISSING DATA :"
        for var in list(self.keys()):
            _tmp += f'\n\t{self.stat_print_missing_data_variable(var)}'
        return _tmp


    def fbfill(self
               , variables: list = []
               , dims: list = ["x", "y", "time"]
               , flimit: int = 1
               , blimit: int = 1
               , max_occurence: int = -1
               ) -> DatasetWildFire:
        """
        A recursive function that remove the nan values on a datacube.

        It first apply a forward fill with a limit of *flimit*
        Then a bakward fill with a limit of *blimit*
        on the *coords* of a *datacube*
        untill there is no more nan or until *max_occurence* is reached

        Parameters
        ----------
        variables : list, default []
            Specify upon which variable of the dataset we want to fill.
            if empty it will contain all the variables of the dataset.

        dims : list, default ["x", "y", "time"]
            Specifies the dimension along which to propagate values when filling.

        flimit : integer, default 1
            The maximum number of consecutive NaN values to forward fill.
            In other words, if there is a gap with more than this number of consecutive NaNs,
            it will only be partially filled.
            Must be greater than 0 or None for no limit.
            Must be None or greater than or equal to axis length if filling along chunked axes (dimensions).

        blimit : integer, default 1
            The maximum number of consecutive NaN values to backward fill.
            In other words, if there is a gap with more than this number of consecutive NaNs,
            it will only be partially filled.
            Must be greater than 0 or None for no limit.
            Must be None or greater than or equal to axis length if filling along chunked axes (dimensions).

        max_occurence : integer, default -1
            The maximum number of time the filling will be processed.
            If the number is negative the filling will be done untill there is no more Nan value in the datacube.

        """

        #if variables is empty it means the filling will be done upon all the variables of the dataset
        if len(variables) == 0:
            variables = list(self.keys())

        _datacube = self.copy()

        # for all the variables
        for _var in variables:
            # on all the variable dimension
            for _dim in self[_var].dims:
                # if the variables dimension is in the targeted dimensions
                if _dim in dims:
                    self[_var] = self[_var].ffill(_dim, limit=flimit)
                    self[_var] = self[_var].bfill(_dim, limit=blimit)

        # # If the original datacube has not been changed from the copy after the filling
        # # or if the maximum occurence wanted is reached
        if self.equals(_datacube) or max_occurence == 0:
            return self

        # recursive on the _datacube
        return self.fbfill(variables = variables
                           , dims=dims
                           , flimit=flimit
                           , blimit=blimit
                           , max_occurence=max_occurence - 1
                      )

    # Function to clip a datasets to the area of interest
    def clip_to_aoi(self, aoi):
        """Clips the dataset to the area of interest

         Parameters
        ----------
        aoi : list, default []
            Specify upon which variable of the dataset we want to fill.
            if empty it will contain all the variables of the dataset."""
        "
        self.rio.clip(aoi.geometry.apply(mapping), aoi.crs)