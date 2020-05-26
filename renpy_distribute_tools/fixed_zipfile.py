"""
    This module contains a customized version of the `ZipFile` object
    to properly handle extraction of macOS apps so that permissions aren't
    stripped.
"""
import os
from zipfile import ZipFile as PyZipFile, ZipInfo
from renpy_distribute_tools.util import deprecated


class ZipFile(PyZipFile):
    """The ZipFile class is a patched version of the ZipFile class in the `zipfile` module that
        retains the attribute permissions for files.
    """

    def extract(self, member, path=None, pwd=None):
        if not isinstance(member, ZipInfo):
            member = self.getinfo(member)

        if path is None:
            path = os.getcwd()

        ret_val = self._extract_member(member, path, pwd)
        attr = member.external_attr >> 16
        if attr != 0:
            os.chmod(ret_val, attr)
        return ret_val

    def extractall(self, path=None, members=None, pwd=None):
        if members is None:
            members = self.namelist()

        if path is None:
            path = os.getcwd()
        else:
            path = os.fspath(path)

        for zipinfo in members:
            self.extract(zipinfo, path, pwd)


@deprecated("MyZipFile has been renamed to ZipFile.")
class MyZipFile(ZipFile):
    """The MyZipFile class is a patched version of the ZipFile class in the `zipfile` module that
        retains the attribute permissions for files.
    """
