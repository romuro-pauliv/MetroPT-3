# |--------------------------------------------------------------------------------------------------------------------|
# |                                                                                  app/analysis/daily_periodicity.py |
# |                                                                                                    encoding: UTF-8 |
# |                                                                                                     Python v: 3.10 |
# |--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from datetime   import datetime, timedelta
import numpy    as np
import pandas   as pd

from config.config_vars import FeaturesNames, ConfigTimestamp

from log.genlog import genlog
# |--------------------------------------------------------------------------------------------------------------------|


class SplitbyPeriod(object):
    def __init__(self, feature: str, df: pd.DataFrame, datetime_range: timedelta) -> None:
        """
        Initializes the SplitbyPeriod class.
        Args:
            feature (str)               : The name of the DataFrame column to be used as the feature series.
            df (pd.DataFrame)           : The DataFrame containing the data.
            datetime_range (timedelta)  : The time range to split the periods.
        """
        self.df             : pd.DataFrame  = df
        self.feature_name   : str           = feature
        self.timedelta_range: timedelta     = datetime_range
        
        self.serie: pd.DataFrame = self.df[self.feature_name]
        
        self.timestamp_str : pd.Series = self.df[FeaturesNames.TIMESTAMP]
        self.timestamp_pddt: pd.Series = pd.to_datetime(self.df[FeaturesNames.TIMESTAMP], format=ConfigTimestamp.FORMAT)
        
        self.global_datetime_min: datetime = datetime.strptime(self.timestamp_str.values[0] , ConfigTimestamp.FORMAT)
        self.global_datetime_max: datetime = datetime.strptime(self.timestamp_str.values[-1], ConfigTimestamp.FORMAT)
        
        self.t: list[np.ndarray] = []
        self.x: list[np.ndarray] = []
        self.y: list[np.ndarray] = []
        
        self.min_datetime_loop: datetime = self.global_datetime_min
        self.max_datetime_loop: datetime = self.global_datetime_min + self.timedelta_range
    
    def _get_subset(self) -> tuple[pd.Series]:
        """
        Gets a subset of the feature series based on the current date range.
        Returns:
            tuple[pd.Series, pd.Series]: (serie, timestamp) The subset of the resource series 
                                         within the current date range.
        """
        serie: pd.Series = self.serie[
            (self.timestamp_pddt >= self.min_datetime_loop) & (self.timestamp_pddt < self.max_datetime_loop)
        ]
        timestamp: pd.Series = self.timestamp_pddt[
            (self.timestamp_pddt >= self.min_datetime_loop) & (self.timestamp_pddt < self.max_datetime_loop)
        ]
        return serie, timestamp
    
    def _append_period(self, subset: tuple[pd.Series]) -> None:
        """
        Adds the current subset to periods X and Y.
        Args:
            subset (tuple[pd.Series, pd.Series]): The subset of the resource series to be added 
                                                  and respective timestamp.
        """
        self.t.append(subset[1].values)
        self.y.append(subset[0].values)
        self.x.append(np.arange(len(subset[0])))
    
    def _update_min_max_datetime_loop(self) -> None:
        """
        Updates the minimum and maximum limits of the current date range for the next period.
        """
        self.min_datetime_loop: datetime = self.max_datetime_loop
        self.max_datetime_loop: datetime = self.max_datetime_loop + self.timedelta_range
    
    def run(self) -> None:
        """
        Performs the process of splitting the DataFrame into periods defined by the time interval.
        """
        while True:
            if self.max_datetime_loop >= self.global_datetime_max:
                break
            self._append_period(self._get_subset())              
            self._update_min_max_datetime_loop()
            genlog.log(True, f"subset [{self.min_datetime_loop} -> {self.max_datetime_loop}]", True)
    
    def get_periods(self) -> None:
        """
        Returns the periods X and Y.
        Returns:
            tuple[list[np.ndarray], list[np.ndarray]]: The X and Y periods.
        """
        return self.x, self.y, self.t
    
    def get_concatenate_period(self) -> None:
        """
        Retunrs the concatenated period X and Y
        Returns:
            tuple[np.ndarray, np.ndarray]: The concatenated X and Y periods.
        """
        return np.concatenate(self.x), np.concatenate(self.y), np.concatenate(self.t)