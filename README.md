# Doxy-my-docs

[![Build status](https://ci.appveyor.com/api/projects/status/f90rhviaxvrnvaju/branch/master?svg=true)](https://ci.appveyor.com/project/Ducatel/doxy-my-docs/branch/master)
[![Docker Pull](https://img.shields.io/docker/pulls/tracesoftware/doxy-my-docs.svg)](https://hub.docker.com/r/tracesoftware/doxy-my-docs/)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)

Doxy-my-docs is an command line programm which can be use for building dev documentation with doxygen and publish it to [HostMyDocs](https://github.com/TraceSoftwareInternational/HostMyDocs) server.

## How to use it

### Execution

There are 3 differents way for using it:

1. Use the docker image [tracesoftware/doxy-my-docs](https://hub.docker.com/r/tracesoftware/doxy-my-docs/). Example:
````bash
docker run -ti --rm -v "`pwd`/tests/assets:/usr/src/data" tracesoftware\doxy-my-docs --config-file="data/doxy-my-docs.json"
````
2. Use Single executable (Windows only)
    * Download it in release tab
    * Use it in command line, example `doxy-my-docs.exe --config-file=doxy-my-docs.json`
3. Use source
    * Download the source from release tab
    * Download requirements `pip install pipenv && pipenv install`
    * Use it in command line, example `python doxy-my-docs.py --config-file=doxy-my-docs.json`
    
### Configuration

You can configure this with arguments in command line

````
usage: doxy-my-docs.py [-h] [--debug] [--config-file CONFIG_FILE]
                       [--address ADDRESS] [--port PORT] [--disable-tls]
                       [--login LOGIN] [--password PASSWORD]
                       [--doxygen DOXYGEN] [--doxyfile DOXYFILE]
                       [--language LANGUAGE]
                       [--project-version PROJECT_VERSION] [--name NAME]

optional arguments:
  -h, --help            show this help message and exit
  --debug               Display the debug information
  --config-file CONFIG_FILE
                        Path to configuration file. If other arguments are
                        presents, they will overload the file configuration

HostMyDocs configuration:
  --address ADDRESS     The url (or IP) of the targeted HostMyDocs server
  --port PORT           The port on the targeted HostMyDocs server
  --disable-tls         If present HostMyDocs server will be used with HTTP
  --login LOGIN         The login for HostMyDocs REST API
  --password PASSWORD   The password for HostMyDocs REST API

Doxygen configuration:
  --doxygen DOXYGEN     Path to the doxygen executable. If not present,
                        doxygen will be searched in path
  --doxyfile DOXYFILE   Path to the doxyfile you want to user

Project configuration:
  --language LANGUAGE   Language of the documentation
  --project-version PROJECT_VERSION
                        Version of the project documentation will be created
                        in HostMyDocs. By default will use the
                        'PROJECT_NUMBER' value in Doxyfile
  --name NAME           Name of the project will be created in HostMyDocs. By
                        default will use the 'PROJECT_NAME' value in Doxyfile
````

Or you can use a configuration file like:

````json
{
    "debug": true,
    "hostMyDocs" : {
        "address" : "127.0.0.1",
        "port": 8080,
        "disable-tls": false,
        "login": "login",
        "password": "password"
    },
    "doxygen" : {
        "doxygen": "C:\\Program Files\\doxygen\\bin\\doxygen.exe",
        "doxyfile": "./Doxyfile"
    },
    "project" : {
        "language": "C++",
        "version": "1.2.3.4",
        "name": "MyNiceProject"
    }
}
````

If you use command line args + configuration file, command line args will be use in priority

