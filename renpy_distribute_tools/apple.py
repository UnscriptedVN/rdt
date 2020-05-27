"""The `apple` module contains important utilities to make signing, notarizing, and building
    packages for macOS easier.

The functions in this module require a device running macOS with Xcode 10 or higher.
"""
import os
import subprocess
from sys import platform
from functools import wraps


def darwin_only(call):
    """A decorator for macOS-specific commands.

    This should be used to denote that a function only works on macOS due to reliance on built-in
        tools from macOS or Xcode.
    """
    @wraps(call)
    def darwin_call(*args, **kwargs):
        if platform.lower() != "darwin":
            raise OSError("Function %s only works on macOS." % (call))
        return call(*args, **kwargs)
    return darwin_call


@darwin_only
def package_app_zip(app: str):
    """Create a ZIP file of the app.

    Args:
        app (str): The path to the macOS to make an archive of
    """
    if os.path.isdir(app):
        zip_commands = ["ditto", "-c", "-k", "--rsrc",
                        "--keepParent", app, app + ".zip"]
        subprocess.check_call(zip_commands)
    else:
        raise NotADirectoryError(
            "The .app file is either missing or not present.")


@darwin_only
def build_pkg(app: str, identity: str, package_name: str):
    """Create an installable package from a macOS app.

    By default, it will create an app package that installs to `/Applications/`. This package
        installer can also be used to submit an app to the Mac App Store.

    If the package name isn't a file path, `.pkg` will automatically be appended at the end of the
        name.

    Args:
        app (str): The path to the app to create a package of.
        identity (str): The identity to sign the package with
        package_name (str): The name or path of the resulting package.
    """
    package_file = package_name
    if ".pkg" not in package_name:
        package_file = package_name + ".pkg"
    commands = ["productbuild", "--component", app,
                "/Applications", "--sign", identity, package_file]
    return subprocess.check_call(commands)


@darwin_only
def code_sign(identity: str, app_directory: str, **kwargs):
    """Digitally sign a macOS application with a signing identity and any entitlements.

    Args:
        identity (str): The identity to use during signing, usually a Developer ID.
        app_directory (str): The path to the macOS application for signing.
        **kwargs: Arbitrary keyword arguments.

    Kwargs:
        entitlements (str): (Optional) The path to the entitlements the app should be signed with.
        enable_hardened_runtime (bool): Whether to sign the app with the hardened runtime on.
    """
    commands = ["codesign",
                "--timestamp",
                "--deep",
                "--force",
                "--no-strict",
                "--sign",
                identity,
                app_directory]

    if "entitlements" in kwargs:
        commands.append("--entitlements")
        commands.append(kwargs["entitlements"])

    if "enable_hardened_runtime" in kwargs and kwargs["enable_hardened_runtime"]:
        commands.append("--options=runtime")

    return subprocess.check_call(commands)


@darwin_only
def upload_to_notary(app: str,
                     identifier: str,
                     username: str,
                     password: str,
                     **kwargs) -> str:
    """Upload a macOS application archive to Apple's notary service for notarization.

    Args:
        app (str): The path to the macOS application to send to Apple.
        identifier (str): The bundle identifier of the application.
        username (str): The username (email address) of the Apple ID to notarize under.
        password (str): The password of the Apple ID to notarize under.
        **kwargs: Arbitrary keyword arguments.

    Kwargs:
        provider (str): The App Store Connect or iTunes Connect provider associated with the Apple
            ID used to sign the app.
    Returns:
        uuid_str (str): The request UUID.
    """
    package_app_zip(app)
    commands = ["xcrun", "altool", "-t", "osx", "-f", app + ".zip",
                "--notarize-app", "--primary-bundle-id", identifier,
                "-u", username, "-p", password]

    if "provider" in kwargs:
        commands += ["-itc_provider", kwargs["provider"]]

    result = subprocess.check_output(  # pylint:disable=unexpected-keyword-arg
        commands, text=True)
    os.remove(app + ".zip")

    result = result.split("\n")
    trimmed = result[1:]
    if len(trimmed) < 1:
        return ""
    return trimmed[0].replace("RequestUUID = ", "")


@darwin_only
def check_notary_status(uuid: str, username: str, password: str) -> int:
    """Get the notarization status of a given UUID.

    Arguments:
        uuid (str): The UUID of the app to check the status of.
        username (str): The user that submitted the notarization request.
        password (str): The password to use to sign into Apple.

    Returns:
        status (int): The status code associated with the UUID notarization request. A code of `-1`
            indicates that getting the status code failed, either because the item could not be
            found or because no status code has been given yet.
    """
    result = subprocess.check_output(  # pylint:disable=unexpected-keyword-arg
        ["xcrun", "altool", "--notarization-info", uuid, "-u", username, "-p", password], text=True)
    status = [x for x in result.replace(
        "  ", "").split("\n") if "Status Code" in x]

    if len(status) < 1:
        return -1

    status = status[0].replace("Status Code", "").replace(" ", "").split(":")
    while '' in status:
        status.remove('')

    if len(status) < 1:
        return -1
    return int(status[0])


@darwin_only
def staple(app: str):
    """Staple a notarization ticket to a notarized app.

    Args:
        app (str): The path of the macOS app to staple the ticket to.
    """
    commands = ["xcrun", "stapler", "staple", app]
    return subprocess.check_call(commands)
