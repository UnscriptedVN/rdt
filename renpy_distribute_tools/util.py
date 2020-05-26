"""This module contains some basic utilities to locate Ren'Py distributables and to find the macOS
    version of a VN.
"""
import os
import warnings
from typing import Optional, Callable
from functools import wraps


def deprecated(message: str = ""):
    """Mark a function as deprecated.

    This is used as a decorator to mark some functions as deprecated without needing to import
        warnings repeatedly. The function that uses the decorator will be called but will display
        a deprecation warning with a supplied message.

    Arguments:
        message (str): The message or reason for deprecation. Defaults to a generic statement
            generated by the function's name.

    Returns:
        warnable (Callable): The function with a warning wrapper.
    """
    def warnable(call: Callable):
        @wraps(call)
        def do_call(*args, **kwargs):
            warnings.warn(message if message else call.__name__ + " is deprecated.",
                          category=DeprecationWarning)
            call(*args, **kwargs)
        return do_call
    return warnable


@deprecated(message="Please use isfile or is from the os.path module.")
def file_exists(directory: str = os.getcwd(), item: str = '') -> Optional[str]:
    """Determine whether a file exists in a certain directory.

    **Note**: This function is being deprecated in favor of the utilities provided in the `os` 
        module.

    Args:
        dir (str): The directory to search in.
        item (str): The item to search for in the directory.
    Returns:
        fname (str): File name if it's found or `None` if it doesn't find anything
    """
    cwd = os.listdir(directory)
    for listed_item in cwd:
        if item in listed_item:
            return listed_item
    return None


def verify_built_files(directory: str = os.getcwd()) -> bool:
    """Determine if the Ren'Py distributions have been built already by looking for the `-dists`
        directory.

    This function will check if the directory exists in itself.

    Args:
        dir (str): The directory to search.

    Returns:
        isdir (bool): Whether the directory exists or not.
    """
    return os.path.isdir(directory + "-dists")


def find_mac_build(directory: str) -> bool:
    """Determine whether the macOS builds have been created.

    Args:
        dir (str): The directory to search in

    Returns:
        isfile (bool): Whether the macOS ZIP file exists.
    """
    return os.path.isfile(directory + "-mac.zip")
