# |--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                  app/log/genlog.py |
# |                                                                                                    encoding: UTF-8 |
# |                                                                                                     Python v: 3.10 |
# |--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from colorama   import Fore, Style
from datetime   import datetime
from typing     import Union

import inspect
# |--------------------------------------------------------------------------------------------------------------------|

class StringLog(object):
    """
    A class to generate formatted log messages with optional color coding.

    This class provides methods to create log messages with optional color 
    coding for different log components such as datetime, instance, method,
    and success status.
    """
    def __init__(self) -> None:
        """
        Initialize the StringLog instance.

        This sets the initial state of the color attribute to False.
        """
        self.color: bool = False
    
    def active_color(self) -> None:
        """
        Activate color coding for the log messages.

        This sets the color attribute to True, enabling color-coded log 
        messages.
        """
        self.color: bool = True
    
    def datetime_func(self) -> str:
        """
        Generate a formatted datetime string for the log message.

        Returns:
            str: A formatted datetime string with optional color coding.
        """
        if self.color:
            return f"[{Fore.CYAN}{datetime.now()}{Style.RESET_ALL}]"
        return f"[{datetime.now()}]"

    def instance_func(self, value: str) -> str:
        """
        Generate a formatted instance string for the log message.

        Args:
            value (str): The instance name to be formatted.

        Returns:
            str: A formatted instance string with optional color coding.
        """
        if self.color:
            return f"[{Fore.MAGENTA}{value}{Style.RESET_ALL}]"
        return f"[{value}]"
    
    def method_func(self, value: str) -> str:
        """
        Generate a formatted method string for the log message.

        Args:
            value (str): The method name to be formatted.

        Returns:
            str: A formatted method string with optional color coding.
        """
        if self.color:
            return f"({Fore.LIGHTMAGENTA_EX}{value}{Style.RESET_ALL})]"
        return f"({value})]"
    
    def success_color_func(self, value: Union[bool, str]) -> str:
        """
        Determine the color coding for the success status.

        Args:
            value (Union[bool, str]): The success status or custom string.

        Returns:
            str: A color code string for the success status.
        """
        if self.color:
            if isinstance(value, bool):
                return f"{Fore.GREEN if value else Fore.RED}"
            return f"{Fore.YELLOW}"
        return ""

    def success_func(self, value: Union[bool, str]) -> str:
        """
        Generate a formatted success status string for the log message.

        Args:
            value (Union[bool, str]): The success status or custom string.

        Returns:
            str: A formatted success status string with optional color coding.
        """
        if self.color:
            if isinstance(value, bool):
                return f"[{self.success_color_func(value)}{'SUCCESS' if value else 'FAILED'}{Style.RESET_ALL}]"
            return f"[{self.success_color_func(value)}{value.upper()}{Style.RESET_ALL}]"
        
        if isinstance(value, bool):
            return f"[{'SUCCESS' if value else 'FAILED'}]"
        return f"[{value.upper()}]"
        
    def info_func(self, value: str) -> str:
        """
        Generate a formatted info string for the log message.

        Args:
            value (str): The info message to be formatted.

        Returns:
            str: A formatted info string.
        """
        return value

class GenLog(StringLog):
    """
    A class to generate and print detailed log messages with verbosity control.

    This class extends StringLog to provide methods for generating and printing
    log messages with detailed information about the logging context and 
    optional verbosity control.
    """
    def __init__(self) -> None:
        """
        Initialize the GenLog instance.

        This sets the initial state of the verbose attribute to False and 
        initializes the base StringLog class.
        """
        self.verbose: bool = False
        super().__init__()
        
    def active_verbose(self) -> None:
        """
        Activate verbose mode for the log messages.

        This sets the verbose attribute to True, enabling detailed log 
        messages when verbosity is requested.
        """
        self.verbose: bool = True
    
    def log(self, status: bool, info: str, v: bool) -> None:
        """
        Generate and print a log message with contextual information.

        This method generates a log message with datetime, instance name,
        method name, success status, and additional info. It prints the log
        message based on the verbosity settings.

        Args:
            status (bool): The status of the operation [True -> Success, False -> Faild, or any string].
            info (str): Additional information to include in the log message.
            v (bool): Flag indicating whether to consider the verbosity setting [True = only verbosity]
        """
        frame = inspect.currentframe()
        outer_frame = inspect.getouterframes(frame)[1]
        method_name: str = outer_frame.function
        try:
            instance = outer_frame.frame.f_locals['self']
            class_name: str = instance.__class__.__name__
        except KeyError:
            class_name: str = "global"
        
        datetime_log: str = self.datetime_func()
        instance_log: str = self.instance_func(class_name)
        method_log: str = self.method_func(method_name)
        success_log: str = self.success_func(status)
        info_log: str = self.info_func(info)
        
        log: str = f"{datetime_log} {instance_log} {method_log} {success_log} | {info_log}"
        
        if v and self.verbose:
            print(log)

        if not v:
            print(log)



genlog: GenLog = GenLog()