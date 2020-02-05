# Ren'Py Distribution Tools

A set of tools to make Ren'Py distribution less of a pain in the arse.

[![MPL](https://img.shields.io/github/license/alicerunsonfedora/renpy-distribute-tools)](LICENSE.txt) 
![Python](https://img.shields.io/badge/python-3.7+-blue.svg) 

## Installing `renpy-distribute-tools`

To install via PyPI:

```
pip install renpy-distribute-tools
```

Or, if you're using a Poetry project, just add the dependency:

```
poetry add renpy-distribute-tools
```

## Building from source

Ren'Py Distribute Tools is a Poetry project and can be built using Poetry's `build` command.

1. Clone the repository.
2. In the root of the project, run `poetry install`.
3. Finally, run `poetry build`.

## What's included

The Ren'Py Distribution Tools set comes with utilities that make it easy to do the following:

- Modifying a visual novel's `Info.plist`.
- Code-signing the visual novel binaries in the Mac app with entitlements.
- Creating a ZIP copy of the Mac app and sending it to Apple's notarization servers.
- Stapling the notarization ticket to a macOS app.

## Usage

See the [documentation](https://alicerunsonfedora.github.io/renpy-distribute-tools) for more info.