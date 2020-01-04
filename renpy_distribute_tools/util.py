"""
    This module contains some basic utilities to locate Ren'Py
    distributables and to find the macOS version of a VN.
"""
import os

def file_exists(directory: str = os.getcwd(), item: str = ''):
    """Determine whether a file exists in a certain directory.

    Args:
        dir: The directory to search in.
        item: The item to search for in the directory.
    Returns:
        File name if it's found or `None` if it doesn't find anything
    """
    cwd = os.listdir(directory)
    for listed_item in cwd:
        if item in listed_item:
            return listed_item
    return None


def verify_built_files(directory: str = os.getcwd()):
    """Determine if the Ren'Py distributions have been built already by looking
    for the `-dists` directory.

    This function will check if the directory exists in itself.

    Args:
        dir: The directory to search.
    """
    return file_exists(directory=directory, item="-dists")


def find_mac_build(directory: str):
    """Determine whether the macOS builds have been created.

    Args:
        dir: The directory to search in
    """
    return file_exists(directory=directory, item="-mac")
