#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import doxygen
import logging
import os

import sys

from doxymydocs import configurationEnum, AppConfiguration
from typing import Optional


def __update_doxygen_config() -> str:
    """
    Update the doxygen configuration from the configuration

    :return: The path to the updated doxygen configuration
    """

    logging.info("update Doxygen configuration")

    doxyfile = AppConfiguration().get_doxygen_config()[configurationEnum.Doxygen.DOXYFILE]
    logging.debug("Doxyfile: {}".format(doxyfile))

    project_config = AppConfiguration().get_project_config()

    doxygen_config_parser = doxygen.ConfigParser()
    doxygen_configuration = doxygen_config_parser.load_configuration(doxyfile)

    if configurationEnum.Project.VERSION in project_config:
        logging.debug("Update PROJECT_NUMBER from {} to {}".format(doxygen_configuration['PROJECT_NUMBER'], project_config[configurationEnum.Project.VERSION]))
        doxygen_configuration['PROJECT_NUMBER'] = project_config[configurationEnum.Project.VERSION]

    if configurationEnum.Project.NAME in project_config:
        logging.debug("Update PROJECT_NAME from {} to {}".format(doxygen_configuration['PROJECT_NAME'], project_config[configurationEnum.Project.NAME]))
        doxygen_configuration['PROJECT_NAME'] = project_config[configurationEnum.Project.NAME]

    doxyfile_updated = os.path.join(doxyfile, ".updated")
    doxygen_config_parser.store_configuration(doxygen_configuration, doxyfile_updated)
    return doxyfile_updated


def __build_doxygen_doc(doxyfile_path: str) -> Optional[str]:
    """
    Build the doxygen configuration using the doxyfile passed in arg

    :param doxyfile_path: The Doxyfile you want to use
    :return: The path to the documentation in zip format
    """

    logging.info("Build Doxygen documentation")
    logging.debug("Doxyfile: {}".format(doxyfile_path))

    doxy_builder = doxygen.Generator(
        doxyfile_path,
        doxygen_path=AppConfiguration().get_doxygen_config()[configurationEnum.Doxygen.DOXYGEN] if configurationEnum.Doxygen.DOXYGEN in AppConfiguration().get_doxygen_config() else None
    )

    return doxy_builder.build(clean=True, generate_zip=True)


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    app_config = AppConfiguration().get_config()
    if configurationEnum.General.DEBUG in app_config and app_config[configurationEnum.General.DEBUG]:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug("Configuration loaded: {}".format(app_config))

    doxyfile_path = __update_doxygen_config()
    zip_archive_path = __build_doxygen_doc(doxyfile_path)
    if zip_archive_path is None:
        logging.fatal("Error during generation of documentation, exit program code 1")
        sys.exit(1)




