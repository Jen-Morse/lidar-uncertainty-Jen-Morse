# Import libraries for NEONDataLoader Class
import os

import pandas as pd
import geopandas as gpd
import rasterstats as rs
import xarray as xr
import rioxarray as rxr

class NEONDataLoader:
    """
    Parent class to load NEON tree height data.
    ----------

    Attributes:
    ----------

    base_dir_tmpl: str
        Base directory for data files.

    insitu_path_tmpl: str
        Path to insitu data files.

    chm_path_tmpl: str
        Path to LiDAR chm data files.

    plots_path_tmpl: str
        Path to centroids file.

    site_name: str
        Site name.

    id_col_name: str
        ID column name.

    formatting_dict: dict
        Dictionary to create file paths.

    id_mod: function
        Modifies ID column to include site name.
    """

    base_dir_tmpl = os.path.join(
        'california',
        'neon-{site_name_low}-site')

    insitu_path_tmpl = os.path.join(
        '{base_dir}',
        '2013',
        'insitu',
        'veg{separator}structure',
        'D17_2013_{site_name_up}_vegStr.csv')

    chm_path_tmpl = os.path.join(
        '{base_dir}',
        '2013',
        'lidar',
        '{site_name_up}_lidarCHM.tif')

    plots_path_tmpl = os.path.join(
        '{base_dir}',
        'vector_data',
        '{site_name_up}{plot}_centroids.shp')

    site_name = NotImplemented
    id_col_name = NotImplemented
    formatting_dict = NotImplemented
    id_mod = None

    def __init__(self):
        self.formatting_dict = self.formatting_dict
        self.formatting_dict['site_name_low'] = self.site_name.lower()
        self.formatting_dict['site_name_up'] = self.site_name.upper()
        self.formatting_dict['base_dir'] = (
            self.base_dir_tmpl.format(**self.formatting_dict))

        self.insitu_path = (
            self.insitu_path_tmpl.format(**self.formatting_dict))
        self.chm_path = (
            self.chm_path_tmpl.format(**self.formatting_dict))
        self.plots_path = (
            self.plots_path_tmpl.format(**self.formatting_dict))

        self._insitu_height_stats = None
        self._lidar_chm_stats = None
        self._height_stats = None

    @property
    def lidar_chm_stats(self):
        """
        Calculate max, mean tree height from LiDAR data.
        -------

        Returns:
        -------
        GeoPandasDataFrame: GeoDataFrame with max and mean tree heights.
        """
        if self._lidar_chm_stats is None:
            plots_gdf = gpd.read_file(self.plots_path)
            plots_gdf.geometry = plots_gdf.geometry.buffer(20)

            # Calculate Zonal statistics
            chm_stats = rs.zonal_stats(
                plots_gdf,
                self.chm_path,
                stats=['mean', 'max'],
                geojson_out=True,
                nodata=0,
                copy_properties=True)

            # Create GeoDataFrame
            self._lidar_chm_stats = (
                gpd.GeoDataFrame.from_features(chm_stats))

            # Rename GeoDataFram columns
            self._lidar_chm_stats.rename(
                columns={'max':'lidar_max', 'mean':'lidar_mean'},
                inplace=True)
            if not self.id_mod is None:
                self._lidar_chm_stats[self.id_col_name] = (
                    self._lidar_chm_stats[self.id_col_name]
                    .apply(self.id_mod))
        return self._lidar_chm_stats

    @property
    def insitu_height_stats(self):
        """ 
        Load and calculate insitu max and mean tree height data.
        -------
        Returns:
        -------
        DataFrame: df with insitu max and mean tree height columns.
        """
        if self._insitu_height_stats is None:
            self._insitu_height_stats = (
                pd.read_csv(self.insitu_path)
                .groupby('plotid')
                .stemheight
                .agg(['max', 'mean'])
                .rename(
                    columns={'max': 'insitu_max',
                             'mean': 'insitu_mean'}))
        return self._insitu_height_stats

    @property
    def height_stats(self):
        """
        Merge insitu data with LiDAR data.
        -------
        Returns:
        -------
        GeoPandasDataFrame: gdf with merged LiDAR and insitu data.
        """
        if self._height_stats is None:
            self._height_stats = (
                self.lidar_chm_stats
                .merge(
                    self.insitu_height_stats,
                    right_index=True,
                    left_on=self.id_col_name))
        return self._height_stats
