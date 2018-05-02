#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from enum import Enum
from aenum import extend_enum


class StringEnum(Enum):
    """
    This enum represent an enum with string in value
    """

    def __str__(self):
        return self.value

class General(StringEnum):
    """ Contains the key for general config """

    DEBUG = "debug"
    CONFIG_FILE = "config_file"


class HostMyDocs(StringEnum):
    """ Contains the key for HostMyDocs config"""

    HOST_MY_DOCS = "hostMyDocs"
    ADDRESS = "address"
    PORT = "port"
    TLS = "disable-tls"
    LOGIN = "login"
    PASSWORD = "password"


class Doxygen(StringEnum):
    """ Contains the key for Doxygen config"""

    DOXYGEN = "doxygen"
    DOXYFILE = "doxyfile"


class Project(StringEnum):
    """ Contains the key for project config"""

    PROJECT = "project"
    LANG = "language"
    VERSION = "version"
    NAME = "name"

# Tricks for adding case to parent enumeration
extend_enum(StringEnum, 'UNDEFINED', 'UNDEFINED')


def string_to_config_enum_value(key: str) -> StringEnum:
    """
    Convert a String to the corresponding config enum entry

    :param key: The string you want to convert into enum entry
    :return: The Enum value corresponding to the input string or StringEnum.UNDEFINED if no match found
    """

    for enum_class in StringEnum.__subclasses__():
        try:
            enum_entry = enum_class(key)
        except ValueError:
            pass
        else:
            return enum_entry

    return StringEnum.UNDEFINED
