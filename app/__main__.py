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
a.global_datetime_max = datetime(2020, 2, 10, 0, 0, 0)
a.run()
x, y, t = a.get_periods()

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes

for i in range(len(x)):
    FIG: tuple[Figure, tuple[Axes]] = plt.subplots(nrows=2, figsize=(16, 8))
    
    
    mean: pd.Series = pd.Series(y[i]).rolling(1000).mean()
    std : pd.Series = pd.Series(y[i]).rolling(1000).std()
    
    FIG[1][0].scatter(t[i], y[i], s=0.2)
    FIG[1][0].plot(t[i], mean, color="red")
    FIG[1][1].scatter(t[i], (y[i]-mean), s=0.2)
    FIG[1][0].plot(t[i], (mean+3*std), color="red", alpha=0.2, linestyle="dashed")
    FIG[1][0].plot(t[i], (mean-3*std), color="red", alpha=0.2, linestyle="dashed")
    
    
    FIG[1][0].grid(True, "both")
    FIG[1][1].grid(True, "both")
    plt.show()
    plt.clf()