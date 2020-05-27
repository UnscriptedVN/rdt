"""The Ren'Py Distribution Tools is a Python module that aims to make distribution of Ren'Py visual
    novel projects easier by automating it with Python utilities and classes.

## Getting Started

### Quick Start: Install via PyPI/Poetry

To install via PyPI:

```
pip install renpy-distribute-tools
```

Or, if you're using a Poetry project, just add the dependency:

```
poetry add renpy-distribute-tools
```

## What's included

The Ren'Py Distribution Tools set comes with utilities that make it easy to do the following:

- Modifying a visual novel's `Info.plist` with an identifier and copyright field.
- Code-signing the visual novel binaries in the Mac app with entitlements.
- Creating a ZIP copy of the Mac app and sending it to Apple's notarization servers.
- Verifying the status of a notarization request.
- Stapling the notarization ticket to a macOS app.
- Publishing content to Itch.io.
"""
__version__ = '0.4.0'

from renpy_distribute_tools.fixed_zipfile import ZipFile, MyZipFile
from renpy_distribute_tools.plist import fix_plist
from renpy_distribute_tools.apple import package_app_zip, \
    upload_to_notary, build_pkg, staple, code_sign, check_notary_status
from renpy_distribute_tools.util import deprecated, file_exists, find_mac_build, verify_built_files
from renpy_distribute_tools.itch import Butler, ButlerPlatformType, DEFAULT_TAG_RULES
