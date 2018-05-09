#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import logging
import sys
from typing import Optional

import doxygen
import hostmydocs
import os

from doxymydocs import configurationEnum, AppConfiguration


def __update_doxygen_config() -> (dict, str):
    """
    Update the doxygen configuration from the configuration

    :return: The doxygen configuration updated and the path to the updated doxygen config
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

    doxyfile_updated = doxyfile+".updated"
    logging.debug("Doxyfile updated: {}".format(doxyfile_updated))

    doxygen_config_parser.store_configuration(doxygen_configuration, doxyfile_updated)

    return doxygen_configuration, doxyfile_updated


def __build_doxygen_doc(doxygen_configuration: dict, doxyfile: str) -> Optional[hostmydocs.Documentation]:
    """
    Build the doxygen configuration using the doxyfile passed in arg

    :param doxygen_configuration: The dict which represent the updated doxygen config
    :param doxyfile: The path to the doxygen config updated
    :return: Documentations object ready to be uploaded. None if an error was occurred
    """

    logging.info("Build Doxygen documentation")

    doxygen_config = AppConfiguration().get_doxygen_config()
    doxy_builder = doxygen.Generator(
        doxyfile,
        doxygen_path=doxygen_config[configurationEnum.Doxygen.DOXYGEN] if configurationEnum.Doxygen.DOXYGEN in doxygen_config else None
    )

    zip_archive_path = doxy_builder.build(clean=True, generate_zip=True)

    logging.debug("Delete doxyfile: {}".format(doxyfile))
    os.remove(doxyfile)

    if zip_archive_path is None:
        logging.error("Impossible to build documentation")
        return None

    return hostmydocs.Documentation(
        name=doxygen_configuration['PROJECT_NAME'],
        zip_archive_path=zip_archive_path,
        language=AppConfiguration().get_project_config()[configurationEnum.Project.LANG],
        version=doxygen_configuration['PROJECT_NUMBER'],
    )


def __upload_doc_to_hmd(doc_to_upload: hostmydocs.Documentation) -> bool:
    """
    Upload the documentation to HostMyDocs server

    :param doc_to_upload:  The documentation you want to upload
    :return: True if done with success else false
    """

    logging.info("Upload documentation")
    logging.debug("Documentation: {}".format(doc_to_upload))

    hmd_config = AppConfiguration().get_hmd_config()
    hmd_server_config = hostmydocs.ServerConfig(
        address=hmd_config[configurationEnum.HostMyDocs.ADDRESS],
        port=hmd_config[configurationEnum.HostMyDocs.PORT] if configurationEnum.HostMyDocs.PORT in hmd_config else 443,
        api_login=hmd_config[configurationEnum.HostMyDocs.LOGIN],
        api_password=hmd_config[configurationEnum.HostMyDocs.PASSWORD],
        use_tls=not hmd_config[configurationEnum.HostMyDocs.DISABLE_TLS] if configurationEnum.HostMyDocs.DISABLE_TLS in hmd_config else False
    )

    logging.debug("Server config: {}".format(hmd_server_config))

    hmd_client = hostmydocs.Client(hmd_server_config)
    return hmd_client.upload_documentation(doc_to_upload)


def __set_working_dir():
    """
    Define the working dir to the folder where config file is store.
    If no config file used, not change the working dir
    """

    if configurationEnum.General.CONFIG_FILE in AppConfiguration().get_config():
        config_folder = os.path.dirname(AppConfiguration().get_config()[configurationEnum.General.CONFIG_FILE])
        logging.debug("Set current directory to config file directory: {}".format(config_folder))
        os.chdir(config_folder)


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    try:
        app_config = AppConfiguration().get_config()
        if configurationEnum.General.DEBUG in app_config and app_config[configurationEnum.General.DEBUG]:
            for handler in logging.root.handlers[:]:
                logging.root.removeHandler(handler)
            logging.basicConfig(level=logging.DEBUG)

        logging.debug("Configuration loaded: {}".format(app_config))

        __set_working_dir()

        doxy_config, doxyfile = __update_doxygen_config()
        doc = __build_doxygen_doc(doxy_config, doxyfile)
        if doc is None:
            logging.fatal("Error during generation of documentation, exit program code 1")
            sys.exit(1)

        if not __upload_doc_to_hmd(doc):
            logging.fatal("Error during upload of documentation, exit program code 2")
            sys.exit(2)

        logging.info("Process done with success")
    except Exception as e:
        logging.fatal("Exception throw, process will exit with code 3")
        logging.exception(e)
        sys.exit(3)
