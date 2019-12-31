import os
import subprocess

def package_app_zip(app: str):
    """
    Create a ZIP file of the app.

    :param app: The path to the macOS to make an archive of
    """
    if os.path.isdir(app):
        zip_commands = ["ditto", "-c", "-k", "--rsrc", "--keepParent", app, app + ".zip"]
        subprocess.run(zip_commands)
    else:
        raise NotADirectoryError("The .app file is either missing or not present.")


def build_pkg(app: str, identity: str, package_name: str):
    """
    Create an installable package from a macOS app. By default, it will create an app package that installs
    to /Applications/. This package installer can also be used to submit an app to the Mac App Store.

    If the package name isn't a file path, `.pkg` will automatically be appended at the end of the name.

    :param app: The path to the app to create a package of.
    :param identity: The identity to sign the package with
    :param package_name: The name or path of the resulting package.
    """
    package_file = package_name
    if ".pkg" not in package_name:
        package_file = package_name + ".pkg"
    commands = ["productbuild", "--component", app, "/Applications", "--sign", identity, package_file]
    pkg = subprocess.run(commands)
    pkg.check_returncode()


def code_sign(identity: str, app_directory: str, entitlements: str = None):
    """
    Digitally sign a macOS application with a signing identity and any entitlements.

    :param identity: The identity to use during signing, usually a Developer ID
    :param app_directory: The path to the macOS application for signing
    :param entitlements: (Optional) The path to the entitlements the app should be signed with
    """
    commands = ["codesign", "--timestamp", "--deep", "--force", "--sign", identity, app_directory]
    
    if entitlements is not None:
        commands.append("--entitlements")
        commands.append(entitlements)
    
    codesign = subprocess.run(commands)
    codesign.check_returncode()


def upload_to_notary(app: str, identifier: str, username: str, password: str, provider: str = None):
    """
    Upload a macOS application archive to Apple's notary service for notarization.

    :param app: The path to the macOS application to send to Apple.
    :param identifier: The bundle identifier of the application.
    :param username: The username (email address) of the Apple ID to notarize under.
    :param password: The password of the Apple ID to notarize under.
    :param provider: (Optional) The App Store Connect or iTunes Connect provider associated with the Apple ID.
    """
    package_app_zip(app)
    commands = ["xcrun", "altool", "-t", "osx", "-f", app + ".zip",  "--notarize-app", "--primary-bundle-id", identifier, "-u", username, "-p", password]
    
    if provider is not None:
        commands.append("-itc_provider")
        commands.append(provider)
        
    notary = subprocess.run(commands)
    notary.check_returncode()
    os.remove(app + ".zip")


def staple(app: str):
    """
    Staple a notarization ticket to a notarized app.

    :param app: The path of the macOS app to staple the ticket to.
    """
    commands = ["xcrun", "stapler", "staple", app]
    stapler = subprocess.run(commands)
    stapler.check_returncode()
