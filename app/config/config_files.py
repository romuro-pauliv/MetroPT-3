# |--------------------------------------------------------------------------------------------------------------------|
# |                                                                                analysis/app/config/config_files.py |
# |                                                                                                    encoding: UTF-8 |
# |                                                                                                     Python v: 3.10 |
# |--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from pathlib import Path, PosixPath
import configparser
import os

from log.genlog import genlog
# |--------------------------------------------------------------------------------------------------------------------|


class ConfigFiles(object):
    """
    A class to read and distribute .ini files in Python instances.

    This class locates .ini files in a specified configuration directory,
    reads them using configparser, and makes them available as ConfigParser
    objects.
    """
    def __init__(self) -> None:
        """
        Initialize the ConfigFiles instance.

        This sets the path for configuration files to 'app/config' and
        initializes the process of locating and reading .ini files.
        """
        self.config_path: PosixPath = Path("app/config")
        self.ini_ext: str = "ini"

        self._get_ini_files_path()
        self._read_ini_files()
        
    def _get_ini_files_path(self) -> None:
        """
        Get the paths of .ini files in the configuration directory.

        This method populates the `self.ini_filepath` list with the paths of
        all .ini files found in the directory specified by `self.config_path`.
        """
        self.ini_filepath: list[str] = []
        [self.ini_filepath.append(fp) if self.ini_ext in fp else None for fp in os.listdir(self.config_path)]
    
    def _read_ini_files(self) -> None:
        """
        Read the .ini files and store them in a dictionary.

        This method reads each .ini file found by `_get_ini_files_path` using
        configparser and stores the resulting ConfigParser objects in the
        `self.ini` dictionary, keyed by the file name without extension.
        """
        self.ini: dict[str, configparser.ConfigParser] = {}
        for ini_filepath in self.ini_filepath:
            name: str = ini_filepath.split(".")[0]
            
            config: configparser.ConfigParser = configparser.ConfigParser()
            config.read(Path(self.config_path, ini_filepath))
            self.ini[name] = config
            genlog.log(True, f"read {ini_filepath}", True)
    
    @property
    def dot_ini(self) -> dict[str, configparser.ConfigParser]:
        return self.ini


configfiles: ConfigFiles = ConfigFiles()