import plistlib

# noinspection PyDeprecation
def fix_plist(plist_file: str, identifier: str, p_copyright: str):
    """
    Add the bundle identifier and copyright text to a Ren'Py-built macOS app's Info.plist.

    :param plist_file: The path to the plist file to modify
    :param identifier: The bundle identifier to set the app to
    :param p_copyright: The human-readable copyright text to attach
    """
    plist = plistlib.readPlist(plist_file)
    plist['CFBundleIdentifier'] = identifier
    plist['NSHumanReadableCopyright'] = p_copyright
    plistlib.writePlist(plist, plist_file)
