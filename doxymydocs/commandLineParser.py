#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import argparse
import sys


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
        config['hostMyDocs'] = self.__parse_hmd_config_option()
        config['doxygen'] = self.__parse_doxygen_config_option()
        config['project'] = self.__parse_project_config_option()

        return config

    def __parse_general_option(self) -> dict:
        """
        Parse the general options and convert them into dict

        :return: The dict which contains the representation of cmd line option
        """
        config = {}

        if self.parsed_cmd_line.debug:
            config['debug'] = True

        if self.parsed_cmd_line.config_file:
            config['config_file'] = self.parsed_cmd_line.config_file

        return config

    def __parse_hmd_config_option(self) -> dict:
        """
       Parse the HostMyDocs options and convert them into dict

       :return: The dict which contains the representation of cmd line option
       """

        config = {}
        if self.parsed_cmd_line.address:
            config['address'] = self.parsed_cmd_line.address

        if self.parsed_cmd_line.port:
            config['port'] = self.parsed_cmd_line.port

        if self.parsed_cmd_line.disable_tls:
            config['disable-tls'] = self.parsed_cmd_line.disable_tls

        if self.parsed_cmd_line.login:
            config['login'] = self.parsed_cmd_line.login

        if self.parsed_cmd_line.password:
            config['password'] = self.parsed_cmd_line.password

        return config

    def __parse_doxygen_config_option(self) -> dict:
        """
        Parse the Doxygen options and convert them into dict

        :return: The dict which contains the representation of cmd line option
        """

        config = {}
        if self.parsed_cmd_line.doxygen:
            config['doxygen'] = self.parsed_cmd_line.doxygen

        if self.parsed_cmd_line.doxyfile:
            config['doxyfile'] = self.parsed_cmd_line.doxyfile

        return config

    def __parse_project_config_option(self) -> dict:
        """
        Parse the project options and convert them into dict

        :return: The dict which contains the representation of cmd line option
        """

        config = {}
        if self.parsed_cmd_line.language:
            config['language'] = self.parsed_cmd_line.language

        if self.parsed_cmd_line.project_version:
            config['version'] = self.parsed_cmd_line.project_version

        if self.parsed_cmd_line.name:
            config['name'] = self.parsed_cmd_line.name

        return config
