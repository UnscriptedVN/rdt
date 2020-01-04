"""
    This module contains some utilities that help fix the property lists
    in the macOS versions of a Ren'Py project.
"""
import plistlib

# noinspection PyDeprecation
def fix_plist(plist_file: str, identifier: str, p_copyright: str):
    """Add the bundle identifier and copyright text to a Ren'Py-built macOS app's Info.plist.

    Args:
        plist_file: The path to the plist file to modify
        identifier: The bundle identifier to set the app to
        p_copyright: The human-readable copyright text to attach
    """
    plist = plistlib.readPlist(plist_file)
    plist['CFBundleIdentifier'] = identifier
    plist['NSHumanReadableCopyright'] = p_copyright
    plistlib.writePlist(plist, plist_file)
