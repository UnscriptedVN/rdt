"""This module contains important utilities to make signing, notarizing, and
    building packages for macOS easier.

    Note: These functions require macOS and Xcode 10 or higher.
"""
import os
import subprocess
from sys import platform
from functools import wraps

def darwin_only(call):
    """A decorator for macOS-specific commands.

    This should be used to denote that a function only works on
    macOS due to reliance on built-in tools from macOS or Xcode.
    """
    @wraps(call)
    def darwin_call():
        if platform.lower() != "darwin":
            raise OSError("Function %s only works on macOS." % (call))
        call()
    return darwin_call

@darwin_only
def package_app_zip(app: str):
    """Create a ZIP file of the app.

        Args:
            app: The path to the macOS to make an archive of
    """
    if os.path.isdir(app):
        zip_commands = ["ditto", "-c", "-k", "--rsrc", "--keepParent", app, app + ".zip"]
        subprocess.check_call(zip_commands)
    else:
        raise NotADirectoryError("The .app file is either missing or not present.")

@darwin_only
def build_pkg(app: str, identity: str, package_name: str):
    """Create an installable package from a macOS app.

    By default, it will create an app package that installs to `/Applications/`.
    This package installer can also be used to submit an app to the Mac App Store.

    If the package name isn't a file path, `.pkg` will automatically be appended
    at the end of the name.

    Args:
        app: The path to the app to create a package of.
        identity: The identity to sign the package with
        package_name: The name or path of the resulting package.
    """
    package_file = package_name
    if ".pkg" not in package_name:
        package_file = package_name + ".pkg"
    commands = ["productbuild", "--component", app,
                "/Applications", "--sign", identity, package_file]
    return subprocess.check_call(commands)

@darwin_only
def code_sign(identity: str, 
              app_directory: str, 
              entitlements: str = None, 
              enable_hardened_runtime: bool = False):
    """Digitally sign a macOS application with a signing identity and any entitlements.

    Args:
        identity: The identity to use during signing, usually a Developer ID
        app_directory: The path to the macOS application for signing
        entitlements: (Optional) The path to the entitlements the app should be signed with
    """
    commands = ["codesign",
                "--timestamp",
                "--deep",
                "--force",
                "--no-strict",
                "--sign",
                identity,
                app_directory]

    if entitlements is not None:
        commands.append("--entitlements")
        commands.append(entitlements)

    if enable_hardened_runtime:
        commands.append("--options=runtime")

    return subprocess.check_call(commands)

@darwin_only
def upload_to_notary(app: str, identifier: str, username: str, password: str, provider: str = None):
    """Upload a macOS application archive to Apple's notary service for notarization.

    Args:
        app: The path to the macOS application to send to Apple.
        identifier: The bundle identifier of the application.
        username: The username (email address) of the Apple ID to notarize under.
        password: The password of the Apple ID to notarize under.
        provider: (Optional) The App Store Connect or iTunes Connect provider
    associated with the Apple ID.
    """
    package_app_zip(app)
    commands = ["xcrun", "altool", "-t", "osx", "-f", app + ".zip",
                "--notarize-app", "--primary-bundle-id", identifier,
                "-u", username, "-p", password]

    if provider is not None:
        commands.append("-itc_provider")
        commands.append(provider)

    subprocess.check_call(commands)
    os.remove(app + ".zip")

@darwin_only
def staple(app: str):
    """Staple a notarization ticket to a notarized app.

    Args:
        app: The path of the macOS app to staple the ticket to.
    """
    commands = ["xcrun", "stapler", "staple", app]
    return subprocess.check_call(commands)
