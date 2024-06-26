# Log Control |--------------------------------------------------------------------------------------------------------|
from log.genlog             import genlog
genlog.active_verbose()
genlog.active_color()
# |--------------------------------------------------------------------------------------------------------------------|

# |--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                    app/__main__.py |
# |                                                                                                    encoding: UTF-8 |
# |                                                                                                     Python v: 3.10 |
# |--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from resources.read_csv import ReadCSV
import pandas as pd
# |--------------------------------------------------------------------------------------------------------------------|

reader  : ReadCSV = ReadCSV()
df      : pd.DataFrame = reader.read("MetroPT3(AirCompressor)")

from analysis.daily_periodicity import SplitbyPeriod
from datetime import timedelta, datetime


a: SplitbyPeriod = SplitbyPeriod("Oil_temperature", df, timedelta(hours=2))
a.global_datetime_max = datetime(2020, 2, 4, 0, 0, 0)
a.run()
x, y, t = a.get_periods()




# | WorkBench |-------------------------------------------------------------------------------------------------------|
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import numpy as np

from sklearn.ensemble import GradientBoostingRegressor

for i in range(len(x)):
    FIG: tuple[Figure, tuple[Axes]] = plt.subplots(nrows=2, figsize=(16, 8))
    
    x_: np.ndarray = x[i]
    y_: np.ndarray = y[i]
    
    clf: GradientBoostingRegressor = GradientBoostingRegressor(n_estimators=500, max_depth=10)
    clf.fit(x_.reshape(-1, 1), y_)
    y_p: np.ndarray = clf.predict(x_.reshape(-1, 1))
    
    
    FIG[1][0].scatter(x_, y_, s=0.2)
    FIG[1][0].plot(x_, y_p, color="red", linewidth=0.5)
    
    
    
    
    FIG[1][0].grid(True, "both")
    FIG[1][1].grid(True, "both")
    
    plt.show()
    plt.clf()