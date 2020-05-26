"""The `itch` module contains the code necessary to push projects to Itch.io using the butler
    tool.
"""
import subprocess as proc


class Butler(object):
    """A class representation of the Butler from Itch.io."""

    def __init__(self, author, project, **kwargs):
        """Initialize a Butler class.

        Arguments:
            author (str): The itch.io user that will submit a project.
            project (str): The project that the user will submit.

        Kwargs:
            exec (str): The path to the Butler executable file. Defaults to "butler".
        """
        self.author = author
        self.project = project
        self.bin = kwargs["exec"] if "exec" in kwargs else "butler"

    def push(self, file: str, **kwargs):
        """Push the file to the Itch.io page.

        Arguments:
            file (str): The path to the file to push.
            **kwargs: Arbitrary keyword arguments

        Kwargs:
            user_version (str): The user version to use, if any.
        """
        command = [self.bin, file, self.author + "/" + self.project]
        if "user_version" in kwargs:
            command += ["--userversion", kwargs["user_version"]]
        return proc.check_call(command)
