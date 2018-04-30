#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from doxymydocs import CommandLineParser
import logging
import os
import json
from doxymydocs.exceptions import BadConfigurationError


class AppConfiguration:
    """
    Use  this class to get the configuration of the application
    """

    __config = {}
    """ Dict which contains the configuration of application """

    @classmethod
    def get_config(cls) -> dict:
        """
        Get the application configuration

        :return: The application configuration
        :raise FileNotFoundError: If the config file path in parameter cannot be found
        :raise BadConfigurationError: If an error was found in the configuration
        """

        if not cls.__config:
            cls().__load()

        return cls.__config

    def __load(self):
        """
        Load the configuration

        :raise FileNotFoundError: If the config file path in parameter cannot be found
        :raise BadConfigurationError: If an error was found in the configuration
        """

        cmd_args = CommandLineParser().parse_to_dict()

        if "config_file" in cmd_args:
            self.__init_from_config_file(cmd_args['config_file'])

        self.__init_from_command_line_args(cmd_args)
        self.__config_is_valid()


    def __init_from_command_line_args(self, cmd_args: dict):
        """
        Init the configuration using the command line arguments

        :param cmd_args: The parsed command line args
        """

        logging.debug("Load from command line")
        AppConfiguration.__config = AppConfiguration.__dict_merge(cmd_args, AppConfiguration.__config)

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
            AppConfiguration.__config = json.load(json_data_file)

    @classmethod
    def __config_is_valid(cls):
        """
        Check if the app configuration is valid

        :raise BadConfigurationError: If the configuration is invalid
        """

        if not all(key in cls.__config['hostMyDocs'] for key in ['address', 'login', 'password']):
            raise BadConfigurationError("Missing field in 'hostMyDocs' configuration")

        if 'doxyfile' not in cls.__config['doxygen']:
            raise BadConfigurationError("Missing field 'doxyfile' in 'doxygen' configuration")

        if 'language' not in cls.__config['project']:
            raise BadConfigurationError("Missing field 'language' in 'project' configuration")



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
