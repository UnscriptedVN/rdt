"""The `itch` module contains the code necessary to push projects to Itch.io using the butler
    tool.
"""
import subprocess as proc
import enum


class ButlerPlatformType(enum.Enum):
    """Enumerations for platform types."""
    WINDOWS = "win"
    DARWIN = "mac"
    LINUX = "linux"
    OTHER = ""


DEFAULT_TAG_RULES = {
    "win": ButlerPlatformType.WINDOWS,
    "mac": ButlerPlatformType.DARWIN,
    "linux": ButlerPlatformType.LINUX
}


class Butler(object):
    """The handler for publishing content to Itch.io using Butler.

    Attributes:
        author (str): The itch.io username that is publishing content.
        project (str): The project that the author is publishing content for.
        bin (str): The path to the Butler executable.
        tag_rules (dict): A dictionary containing rules for additional tags.
    """

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
        self.tag_rules = DEFAULT_TAG_RULES.copy()
        self.bin = kwargs["exec"] if "exec" in kwargs else "butler"

    def push(self, file: str, **kwargs):
        """Push the file to the Itch.io page.

        Arguments:
            file (str): The path to the file to push.
            **kwargs: Arbitrary keyword arguments

        Kwargs:
            user_version (str): The user version to use, if any.
            with_tag_rule (str): The tag rule to use. This is used as a channel.
            with_custom_tag (str): The tag to use at the end of the tag rule name.
        """
        channel = self.author + "/" + self.project

        if "with_tag_rule" in kwargs:
            tag: ButlerPlatformType = self.tag_rules.get(
                kwargs["with_tag_rule"], ButlerPlatformType.OTHER)
            channel += ":" + tag.value

        if "with_custom_tag" in kwargs:
            channel += "-" + kwargs["with_custom_tag"]

        command = [self.bin, "push", file, channel]

        if "user_version" in kwargs:
            command += ["--userversion", kwargs["user_version"]]
        return proc.check_call(command)

    def add_tag_rule(self, name: str, platform: ButlerPlatformType):
        """Create a new rule for the project's channel tags.

        Arguments:
            name (str): The rule that will determine what platform to store it under.
            platform (ButlerPlatformType): The platform for that rule.
        """
        self.tag_rules[name] = platform
