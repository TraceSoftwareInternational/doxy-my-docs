#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import argparse
import sys
from doxymydocs import configurationEnum


class CommandLineParser:
    """
    This class is used to configure the command line option available for this programme
    """

    def __init__(self):
        self.cmdline_parser = argparse.ArgumentParser()
        self.parsed_cmd_line = None

        self.__add_general_option()
        self.__add_hmd_config_option()
        self.__add_doxygen_option()
        self.__add_project_option()

    def __add_general_option(self):
        """ Add global configuration of application """
        self.cmdline_parser.add_argument("--debug", action='store_true', help="Display the debug information")
        self.cmdline_parser.add_argument("--config-file", dest="config_file", action='store',
                                         help="Path to configuration file. If other arguments are presents, they will overload the file configuration")

    def __add_hmd_config_option(self):
        """ Initialize option for HostMyDocs configuration """

        group = self.cmdline_parser.add_argument_group('HostMyDocs configuration')
        group.add_argument("--address", action='store', help="The url (or IP) of the targeted HostMyDocs server")
        group.add_argument("--port", action='store', type=int, help="The port on the targeted HostMyDocs server")
        group.add_argument("--disable-tls", dest="disable_tls", action='store_true', help="If present HostMyDocs server will be used with HTTP")
        group.add_argument("--login", action='store', help=" The login for HostMyDocs REST API")
        group.add_argument("--password", action='store', help=" The password for HostMyDocs REST API")

    def __add_doxygen_option(self):
        """ Initialize option for Doxygen configuration """

        group = self.cmdline_parser.add_argument_group('Doxygen configuration')
        group.add_argument("--doxygen", action='store', help="Path to the doxygen executable. If not present, doxygen will be searched in path")
        group.add_argument("--doxyfile", action='store', help="Path to the doxyfile you want to user")

    def __add_project_option(self):
        """ Initialize option for project configuration """

        group = self.cmdline_parser.add_argument_group('Project configuration')
        group.add_argument("--language", action='store', help="Language of the documentation")
        group.add_argument("--project-version", dest="project_version", action='store',
                           help="Version of the project documentation will be created in HostMyDocs. By default will use the 'PROJECT_NUMBER' value in Doxyfile")
        group.add_argument("--name", action='store', help="Name of the project will be created in HostMyDocs. By default will use the 'PROJECT_NAME' value in Doxyfile")

    def parse(self, args=sys.argv[1:]):
        """
        Parse the command line

        :param args: The list of args you want to parse
        :return: The parsed command line
        """
        if self.parsed_cmd_line is None:
            self.parsed_cmd_line = self.cmdline_parser.parse_args(args)

        return self.parsed_cmd_line

    def parse_to_dict(self) -> dict:
        """
        Parse the command lien and export it in dict form

        :return: A dict which represent the command line
        """

        self.parse()
        config = self.__parse_general_option()
        config[configurationEnum.HostMyDocs.HOST_MY_DOCS] = self.__parse_hmd_config_option()
        config[configurationEnum.Doxygen.DOXYGEN] = self.__parse_doxygen_config_option()
        config[configurationEnum.Project.PROJECT] = self.__parse_project_config_option()

        return config

    def __parse_general_option(self) -> dict:
        """
        Parse the general options and convert them into dict

        :return: The dict which contains the representation of cmd line option
        """
        config = {}

        if self.parsed_cmd_line.debug:
            config[configurationEnum.General.DEBUG] = True

        if self.parsed_cmd_line.config_file:
            config[configurationEnum.General.CONFIG_FILE] = self.parsed_cmd_line.config_file

        return config

    def __parse_hmd_config_option(self) -> dict:
        """
       Parse the HostMyDocs options and convert them into dict

       :return: The dict which contains the representation of cmd line option
       """

        config = {}
        if self.parsed_cmd_line.address:
            config[configurationEnum.HostMyDocs.ADDRESS] = self.parsed_cmd_line.address

        if self.parsed_cmd_line.port:
            config[configurationEnum.HostMyDocs.PORT] = self.parsed_cmd_line.port

        if self.parsed_cmd_line.disable_tls:
            config[configurationEnum.HostMyDocs.DISABLE_TLS] = self.parsed_cmd_line.disable_tls

        if self.parsed_cmd_line.login:
            config[configurationEnum.HostMyDocs.LOGIN] = self.parsed_cmd_line.login

        if self.parsed_cmd_line.password:
            config[configurationEnum.HostMyDocs.PASSWORD] = self.parsed_cmd_line.password

        return config

    def __parse_doxygen_config_option(self) -> dict:
        """
        Parse the Doxygen options and convert them into dict

        :return: The dict which contains the representation of cmd line option
        """

        config = {}
        if self.parsed_cmd_line.doxygen:
            config[configurationEnum.Doxygen.DOXYGEN] = self.parsed_cmd_line.doxygen

        if self.parsed_cmd_line.doxyfile:
            config[configurationEnum.Doxygen.DOXYFILE] = self.parsed_cmd_line.doxyfile

        return config

    def __parse_project_config_option(self) -> dict:
        """
        Parse the project options and convert them into dict

        :return: The dict which contains the representation of cmd line option
        """

        config = {}
        if self.parsed_cmd_line.language:
            config[configurationEnum.Project.LANG] = self.parsed_cmd_line.language

        if self.parsed_cmd_line.project_version:
            config[configurationEnum.Project.VERSION] = self.parsed_cmd_line.project_version

        if self.parsed_cmd_line.name:
            config[configurationEnum.Project.NAME] = self.parsed_cmd_line.name

        return config
