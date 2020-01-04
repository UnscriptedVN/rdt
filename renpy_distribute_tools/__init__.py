__version__ = '0.2.0'

from renpy_distribute_tools.fixed_zipfile import MyZipFile
from renpy_distribute_tools.plist import fix_plist
from renpy_distribute_tools.apple import package_app_zip, upload_to_notary, build_pkg, staple, code_sign
from renpy_distribute_tools.util import file_exists, find_mac_build, verify_built_files