# |--------------------------------------------------------------------------------------------------------------------|
# |                                                                                         app/resources/read_arff.py |
# |                                                                                                    encoding: UTF-8 |
# |                                                                                                     Python v: 3.10 |
# |--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from scipy.io   import arff
from pathlib    import PosixPath, Path

import pandas   as pd

from resources.bin_manager  import BinManager
from config.config_vars     import ConfigPath, ConfigExtension
from log.genlog             import genlog
# |--------------------------------------------------------------------------------------------------------------------|

class ReadARFF(object):
    """
    A class to read ARFF files and cache the data in binary format for quicker access.

    This class reads ARFF files from a specified directory, converts them to
    pandas DataFrames, and uses a BinManager instance to cache the data for
    future access.
    """
    def __init__(self) -> None:
        """
        Initialize the ReadARFF instance.

        This sets the root path for ARFF files and the file extension,
        and initializes a BinManager instance for managing binary file caching.
        """
        self.root_path  : PosixPath = ConfigPath.DATA
        self.ext        : str       = ConfigExtension.DATA
        
        self.BinManager: BinManager = BinManager()
    
    def read(self, filename: str) -> pd.DataFrame:
        """
        Read the ARFF file and return it as a pandas DataFrame.

        This method checks if a cached binary version of the file exists. If it
        does, it loads the DataFrame from the binary file. Otherwise, it reads
        the ARFF file, converts it to a DataFrame, caches it, and returns it.

        Args:
            filename (str): The name of the ARFF file (without extension) to read.

        Returns:
            pd.DataFrame: The ARFF file data as a pandas DataFrame.
        """
        if self.BinManager.get_bin_filenames(filename):
            return self.BinManager.get(filename)

        path_: PosixPath = Path(self.root_path, f"{filename}{self.ext}")
        data: pd.DataFrame = pd.DataFrame(arff.loadarff(path_)[0])
        genlog.log(True, f"read {path_}", True)
        self.BinManager.post(filename, data)
        return data