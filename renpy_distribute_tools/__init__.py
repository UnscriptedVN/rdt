"""This module contains all of the tools necessary to make Ren'Py
    visual novel distribution less of a hassle.

The overall premise of this module is to provide utilities that make
distribution of Ren'Py visual novels, particularly for macOS, easier.
"""
__version__ = '0.2.2'

from renpy_distribute_tools.fixed_zipfile import MyZipFile
from renpy_distribute_tools.plist import fix_plist
from renpy_distribute_tools.apple import package_app_zip, \
                                         upload_to_notary, build_pkg, staple, code_sign
from renpy_distribute_tools.util import file_exists, find_mac_build, verify_built_files
