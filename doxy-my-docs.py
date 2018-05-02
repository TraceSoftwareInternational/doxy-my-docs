#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import doxygen
import logging


from doxymydocs import configurationEnum, AppConfiguration


def __update_doxygen_config():
    """ Update the doxygen configuration from the configuration """

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

    doxygen_config_parser.store_configuration(doxygen_configuration, doxyfile)


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    app_config = AppConfiguration().get_config()
    if configurationEnum.General.DEBUG in app_config and app_config[configurationEnum.General.DEBUG]:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    logging.debug("Configuration loaded: {}".format(app_config))

    __update_doxygen_config()




