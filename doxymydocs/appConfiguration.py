#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from copy import deepcopy

from doxymydocs import CommandLineParser
import logging
import os
import json
from doxymydocs.exceptions import BadConfigurationError
from doxymydocs import configurationEnum


class AppConfiguration:
    """
    Use  this class to get the configuration of the application
    """

    __config = {}
    """ Dict which contains the configuration of application """

    @classmethod
    def get_config(cls) -> dict:
        """
        Get all application configuration

        :return: The application configuration
        :raise FileNotFoundError: If the config file path in parameter cannot be found
        :raise BadConfigurationError: If an error was found in the configuration
        """

        if not cls.__config:
            cls().__load()

        return cls.__config

    @classmethod
    def get_project_config(cls) -> dict:
        """
        Get the configuration about project

        :return: The project configuration
        :raise FileNotFoundError: If the config file path in parameter cannot be found
        :raise BadConfigurationError: If an error was found in the configuration
        """

        return cls.get_config()[configurationEnum.Project.PROJECT]

    @classmethod
    def get_doxygen_config(cls) -> dict:
        """
        Get the configuration about Doxygen

        :return: The Doxygen configuration
        :raise FileNotFoundError: If the config file path in parameter cannot be found
        :raise BadConfigurationError: If an error was found in the configuration
        """

        return cls.get_config()[configurationEnum.Doxygen.DOXYGEN]

    @classmethod
    def get_hmd_config(cls) -> dict:
        """
        Get the configuration about HostMyDocs

        :return: The HostMyDocs configuration
        :raise FileNotFoundError: If the config file path in parameter cannot be found
        :raise BadConfigurationError: If an error was found in the configuration
        """

        return cls.get_config()[configurationEnum.HostMyDocs.HOST_MY_DOCS]

    def __load(self):
        """
        Load the configuration

        :raise FileNotFoundError: If the config file path in parameter cannot be found
        :raise BadConfigurationError: If an error was found in the configuration
        """

        cmd_args = CommandLineParser().parse_to_dict()

        if configurationEnum.General.CONFIG_FILE in cmd_args:
            self.__init_from_config_file(cmd_args[configurationEnum.General.CONFIG_FILE])

        self.__init_from_command_line_args(cmd_args)
        self.__config_is_valid()

    def __init_from_command_line_args(self, cmd_args: dict):
        """
        Init the configuration using the command line arguments

        :param cmd_args: The parsed command line args
        """

        logging.debug("Load from command line")
        type(self).__config = self.__dict_merge(type(self).__config, cmd_args)

    @staticmethod
    def __json_hook_convert_key_to_enum_value(dict_entry: dict) -> dict:
        """
        Hook for json.load(object_hook) which convert key string to enum value
        :param dict_entry: The dict which want to be converted
        :return: The converted dict
        """
        return {configurationEnum.string_to_config_enum_value(key): value for (key, value) in dict_entry.items()}

    def __init_from_config_file(self, config_file: str):
        """
        Init the configuration from the configuration file

        :param config_file: Path to the json configuration file
        """

        logging.info("Init config from {}".format(config_file))

        if not os.path.exists(config_file) or not os.path.isfile(config_file):
            err_msg = "Configuration file doesn't exist or not a file. {}".format(config_file)
            logging.error(err_msg)
            raise FileNotFoundError(err_msg)

        with open(config_file, 'r') as json_data_file:
            type(self).__config = {k: v for (k, v) in json.load(json_data_file, object_hook=self.__json_hook_convert_key_to_enum_value).items() if k != configurationEnum.StringEnum.UNDEFINED}

    def __config_is_valid(self):
        """
        Check if the app configuration is valid

        :raise BadConfigurationError: If the configuration is invalid
        """
        if not all(key in type(self).__config[configurationEnum.HostMyDocs.HOST_MY_DOCS] for key in [configurationEnum.HostMyDocs.ADDRESS, configurationEnum.HostMyDocs.LOGIN, configurationEnum.HostMyDocs.PASSWORD]):
            raise BadConfigurationError("Missing field in 'hostMyDocs' configuration")

        if configurationEnum.Doxygen.DOXYFILE not in type(self).__config[configurationEnum.Doxygen.DOXYGEN]:
            raise BadConfigurationError("Missing field '{}' in '{}' configuration".format(configurationEnum.Doxygen.DOXYFILE, configurationEnum.Doxygen.DOXYGEN))

        if configurationEnum.Project.LANG not in type(self).__config[configurationEnum.Project.PROJECT]:
            raise BadConfigurationError("Missing field '{}' in '{}' configuration".format(configurationEnum.Project.LANG, configurationEnum.Project.PROJECT))

    @staticmethod
    def __dict_merge(source, destination):
        """
        run me with nosetests --with-doctest file.py
            >>> a = { 'first' : { 'all_rows' : { 'pass' : 'dog', 'number' : '1' } } }
            >>> b = { 'first' : { 'all_rows' : { 'fail' : 'cat', 'number' : '5' } } }
            >>> merge(b, a) == { 'first' : { 'all_rows' : { 'pass' : 'dog', 'fail' : 'cat', 'number' : '5' } } }
        True
        """
        for key, value in source.items():
            if isinstance(value, dict):
                node = destination.setdefault(key, {})
                AppConfiguration.__dict_merge(value, node)
            else:
                destination[key] = value

        return destination
