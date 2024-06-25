# |--------------------------------------------------------------------------------------------------------------------|
# |                                                                                         app/resources/read_arff.py |
# |                                                                                                    encoding: UTF-8 |
# |                                                                                                     Python v: 3.10 |
# |--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from pathlib    import PosixPath, Path

import pandas   as pd

from resources.bin_manager  import BinManager
from config.config_vars     import ConfigPath, ConfigExtension, ConfigCSV
from log.genlog             import genlog
# |--------------------------------------------------------------------------------------------------------------------|

class ReadCSV(object):
    """
    A class to read CSV files and cache the data in binary format for quicker access.

    This class reads CSV files from a specified directory, converts them to
    pandas DataFrames, and uses a BinManager instance to cache the data for
    future access.
    """
    def __init__(self) -> None:
        """
        Initialize the ReadCSV instance.

        This sets the root path for CSV files and the file extension,
        and initializes a BinManager instance for managing binary file caching.
        """
        self.data_path: PosixPath   = ConfigPath.DATA
        self.extension: str         = ConfigExtension.DATA
        
        self.BinManager: BinManager = BinManager()
    
    def read(self, filename: str) -> None:
        """
        Read the CSV file and return it as a pandas DataFrame.

        This method checks if a cached binary version of the file exists. If it
        does, it loads the DataFrame from the binary file. Otherwise, it reads
        the CSV file, converts it to a DataFrame, caches it, and returns it.

        Args:
            filename (str): The name of the CSV file (without extension) to read.

        Returns:
            pd.DataFrame: The CSV file data as a pandas DataFrame.
        """
        if self.BinManager.get_bin_filenames(filename):
            return self.BinManager.get(filename)
        
        path_: PosixPath = Path(self.data_path, f"{filename}{self.extension}")
        data: pd.DataFrame = pd.read_csv(path_, delimiter=ConfigCSV.DELIMITER)
        genlog.log(True, f"read {path_}", True)
        self.BinManager.post(filename, data)
        return data