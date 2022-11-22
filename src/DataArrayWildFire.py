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
from xarray.core import dtypes
from xarray.core.variable import Variable


class DataArrayWildFire(xr.DataArray):
    """
       N-dimensional array with labeled coordinates and dimensions.
       DataArrayWildFire provides a wrapper around numpy ndarrays that uses
       labeled dimensions and coordinates to support metadata aware
       operations. The API is similar to that for the pandas Series or
       DataFrame, but DataArray objects can have any number of dimensions,
       and their contents have fixed data types.
       Additional features over raw numpy arrays:
       - Apply operations over dimensions by name: ``x.sum('time')``.
       - Select or assign values by integer location (like numpy):
         ``x[:10]`` or by label (like pandas): ``x.loc['2014-01-01']`` or
         ``x.sel(time='2014-01-01')``.
       - Mathematical operations (e.g., ``x - y``) vectorize across
         multiple dimensions (known in numpy as "broadcasting") based on
         dimension names, regardless of their original order.
       - Keep track of arbitrary metadata in the form of a Python
         dictionary: ``x.attrs``
       - Convert to a pandas Series: ``x.to_series()``.
       Getting items from or doing mathematical operations with a
       DataArray always returns another DataArray.
       Parameters
       ----------
       data : array_like
           Values for this array. Must be an ``numpy.ndarray``, ndarray
           like, or castable to an ``ndarray``. If a self-described xarray
           or pandas object, attempts are made to use this array's
           metadata to fill in other unspecified arguments. A view of the
           array's data is used instead of a copy if possible.
       coords : sequence or dict of array_like, optional
           Coordinates (tick labels) to use for indexing along each
           dimension. The following notations are accepted:
           - mapping {dimension name: array-like}
           - sequence of tuples that are valid arguments for
             ``xarray.Variable()``
             - (dims, data)
             - (dims, data, attrs)
             - (dims, data, attrs, encoding)
           Additionally, it is possible to define a coord whose name
           does not match the dimension name, or a coord based on multiple
           dimensions, with one of the following notations:
           - mapping {coord name: DataArray}
           - mapping {coord name: Variable}
           - mapping {coord name: (dimension name, array-like)}
           - mapping {coord name: (tuple of dimension names, array-like)}
       dims : Hashable or sequence of Hashable, optional
           Name(s) of the data dimension(s). Must be either a Hashable
           (only for 1D data) or a sequence of Hashables with length equal
           to the number of dimensions. If this argument is omitted,
           dimension names are taken from ``coords`` (if possible) and
           otherwise default to ``['dim_0', ... 'dim_n']``.
       name : str or None, optional
           Name of this array.
       attrs : dict_like or None, optional
           Attributes to assign to the new instance. By default, an empty
           attribute dictionary is initialized.
    """

    __slots__ = ()

    def __init__(
            self,
            data: Any = dtypes.NA,
            coords: Sequence[Sequence[Any] | pd.Index | DataArray]
                    | Mapping[Any, Any]
                    | None = None,
            dims: Hashable | Sequence[Hashable] | None = None,
            name: Hashable | None = None,
            attrs: Mapping | None = None,
            # internal parameters
            indexes: dict[Hashable, Index] | None = None,
            fastpath: bool = False,
    ) -> None:
        self.super().__init__(data = data
                              , coords = coords
                              , dims = dims
                              , nam = name
                              , attrs = attrs
                              , indexes = indexes
                              , fastpath = fastpath
                              )

    @classmethod
    def cast(cls, cast_object: xr.DataArray) -> DataArrayWildFire:
        """
        Cast an xarray.DataArray into a DataArrayWildFire.
        Parameters
        ----------
        cast_object : xr.DataArray
            The Xarray.DataArray that needs to be cast
        Return: DataArrayWildFire
        ---------
        The new object
        """
        assert isinstance(cast_object, xr.DataArray)
        cast_object.__class__ = cls
        assert isinstance(cast_object, DataArrayWildFire)
        return cast_object

    def print_crs(self) -> None:
        """Prints the crs of the dataray
        Parameters
        ----------
        Return: none
        ---------
        """
        print(self.rio.crs)
        return None

    def define_crs(self, crs=2154) -> Union[xarray.Dataset, xarray.DataArray]:
        """Defines a crs for the dataray
        Parameters
        ----------
        crs: default 2154
            Anything accepted by `rasterio.crs.CRS.from_user_input`

        Return: Union[xarray.Dataset, xarray.DataArray]
            Modified dataset with CF compliant CRS information.
        ---------
        """
        return self.rio.write_crs(crs, inplace=True)

    def reproject_to_lambert93(self) -> xr.DataArray:
        """Reprojects a dataray from longlat to Lambert93
        Parameters
        ----------
        Return: xr.DataArray
            The reprojected DataArray.
        ---------
        """
        return self.rio.reproject("EPSG:2154")

    def interpolate_to_common_grid(self, common_grid) -> xr.DataArray:
        """Interpolates the dataray to a common grid
        Parameters
        ----------
        common_grid : :obj:`xarray.DataArray` | :obj:`xarray.Dataset`
            DataArray of the target resolution and projection.
        Return: xr.DataArray
            Contains the data from the src_data_array, reprojected to match match_data_array.
        ---------
        """
        return self.rio.reproject_match(common_grid, resampling=rasterio.enums.Resampling.bilinear)

    def interpolate_to_common_grid_categorical(self, common_grid) -> xr.DataArray:
        """Interpolates the categorical dataray to a common grid
       Parameters
        ----------
        common_grid : :obj:`xarray.DataArray` | :obj:`xarray.Dataset`
            DataArray of the target resolution and projection.
        Return: xr.DataArray
            Contains the data from the src_data_array, reprojected to match match_data_array.
        ---------
        """
        return self.rio.reproject_match(common_grid, resampling=rasterio.enums.Resampling.mode)

    def resample_to_daily(self) -> DataArrayResample:
        """Resamples the dataray to daily values
        Parameters
        ----------
        Return: core.resample.DataArrayResample
            This object resampled.
        ---------
        """
        return self.resample(time="1D").interpolate("linear")

    # Definition of a function to resample catagorical variables to daily values
    def resample_to_daily_categorical(self) -> DataArrayResample:
        """Resamples the categorical dataray to daily values
        Parameters
        ----------
        Return: core.resample.DataArrayResample
            This object resampled.
        ---------
        """
        return dataray.resample(time="1D").nearest()