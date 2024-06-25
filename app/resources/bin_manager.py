# |--------------------------------------------------------------------------------------------------------------------|
# |                                                                                       app/resources/bin_manager.py |
# |                                                                                                    encoding: UTF-8 |
# |                                                                                                     Python v: 3.10 |
# |--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import pickle
import os

from pathlib    import PosixPath, Path
from typing     import Any

from config.config_vars     import ConfigPath, ConfigExtension
from log.genlog             import genlog
# |--------------------------------------------------------------------------------------------------------------------|


class BinManager(object):
    def __init__(self) -> None:
        """
        Initialize a BinManager instance.
        
        This sets the path for the binary files and ensures that 
        the directory exists by creating it if necessary.
        """
        self.path       : PosixPath     = ConfigPath.BIN
        self.sub_path   : str           = str(self.path).split("/")[-1]
        self.ext        : str           = ConfigExtension.BIN
        self._create_bin_dir()
                
    def _create_bin_dir(self) -> None:
        """
        Create the directory for binary files if it does not already exist.
        
        This method ensures that the directory specified by `self.path` is 
        created. If the directory already exists, no action is taken.
        """
        if self.sub_path not in os.listdir(ConfigPath.ROOT):
            os.mkdir(self.path)
            genlog.log(True, self.path, True)
            return None
        genlog.log(True, "already exists", True)
    
    def post(self, filename: str, file: Any) -> None:
        """
        Save a file as a binary object.
        
        This method serializes and saves the provided file object to a binary 
        file with the given filename in the directory specified by `self.path`.
        
        Args:
            filename (str): The name of the file (without extension) to save.
            file (Any): The file object to be serialized and saved.
        """
        path_: PosixPath = Path(self.path, f"{filename}{self.ext}")
        with open(path_, "wb") as f:
            pickle.dump(file, f)
            genlog.log(True, f"write {path_}", False)
            f.close()
    
    def get_bin_filenames(self, filename: str) -> bool:
        """
        Check if a binary file with the given filename exists in the directory.

        This method checks if a file with the specified filename (including the
        binary file extension) exists in the directory specified by `self.path`.

        Args:
            filename (str): The name of the file (without extension) to check.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        return True if f"{filename}{self.ext}" in os.listdir(self.path) else False
    
    def get(self, filename: str) -> Any:
        """
        Retrieve a binary file.
        
        This method deserializes and loads a file object from a binary file 
        with the given filename in the directory specified by `self.path`.
        
        Args:
            filename (str): The name of the file (without extension) to load.
        
        Returns:
            Any: The deserialized file object.
        """
        path_: PosixPath = Path(self.path, f"{filename}{self.ext}")
        with open(path_, "rb") as f:
            file: Any = pickle.load(f)
            genlog.log(True, f"read {path_}", False)
            f.close()
        return file
