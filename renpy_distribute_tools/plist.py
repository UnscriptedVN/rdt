"""
    This module contains some utilities that help fix the property lists
    in the macOS versions of a Ren'Py project.
"""
import plistlib


def fix_plist(plist_file: str, identifier: str, p_copyright: str):
    """Add the bundle identifier and copyright text to a Ren'Py-built macOS app's Info.plist.

    Args:
        plist_file (str): The path to the plist file to modify
        identifier (str): The bundle identifier to set the app to
        p_copyright (str): The human-readable copyright text to attach
    """
    with open(plist_file, 'rb') as file_obj:
        properties = plistlib.load(file_obj)

    properties["CFBundleIdentifier"] = identifier
    properties["NSHumanReadableCopyright"] = p_copyright

    with open(plist_file, 'wb') as file:
        plistlib.dump(properties, file)
