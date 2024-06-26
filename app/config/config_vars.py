# |--------------------------------------------------------------------------------------------------------------------|
# |                                                                                          app/config/config_vars.py |
# |                                                                                                    encoding: UTF-8 |
# |                                                                                                     Python v: 3.10 |
# |--------------------------------------------------------------------------------------------------------------------|

# |--------------------------------------------------------------------------------------------------------------------|
from config.config_files import configfiles

from pathlib import PosixPath, Path
# |--------------------------------------------------------------------------------------------------------------------|

class ConfigPath(object):
    ROOT: PosixPath = Path(configfiles.dot_ini['paths']['posixpath']['root'])
    DATA: PosixPath = Path(configfiles.dot_ini['paths']['posixpath']['data'])
    BIN : PosixPath = Path(configfiles.dot_ini['paths']['posixpath']['serialization'])


class ConfigExtension(object):
    DATA: str = configfiles.dot_ini['paths']['extensions']['extension_data']
    BIN : str = configfiles.dot_ini['paths']['extensions']['extension_serialization']
    

class ConfigCSV(object):
    DELIMITER: str = configfiles.dot_ini['data']['csv_config']['delimiter']


class FeaturesNames(object):
    TIMESTAMP: str = configfiles.dot_ini['data']['features']['timestamp']
    OIL_TEMP : str = configfiles.dot_ini['data']['features']['oil_temperature']


class ConfigTimestamp(object):
    FORMAT: str = configfiles.dot_ini['data']['datetime_format']['timestamp_format']