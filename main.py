"""
TODO List
- CSS
- Modify README.md with description and license
- Allow example dataset selection
- Use same hyperparameters for the same algorithm on different providers
- Return same result structure from different providers
- Add file size limit (1 MB)
- make JSON all API returns?
"""
from constants import *
import argparse
import os

import cherrypy

from WebServer import WebServer, GetOptionsService, SetOptionsService, GetDefaultDatasetHeadersService


def parse_arguments():
    program_description = "CompareML Server"
    argument_parser = argparse.ArgumentParser(description=program_description)
    argument_parser.add_argument("-e", "--environment", help="name of the environment the server runs in")

    arguments = argument_parser.parse_args()

    environment = DEFAULT_ENVIRONMENT
    if arguments.environment:
        environment = arguments.environment

    return environment


def error_page_500(status, message, traceback, version):
    return f"{message}"


def start_server(environment):
    if not os.path.exists('temp'):
        os.makedirs('temp')

    if not os.path.exists('log'):
        os.makedirs('log')

    global_config_filename = f"global-{environment}.ini"
    cherrypy.config.update(global_config_filename)
    cherrypy.config.update({'error_page.500': error_page_500})

    webapp = WebServer()
    webapp.get_options = GetOptionsService()
    webapp.set_options = SetOptionsService()
    webapp.get_default_dataset_headers = GetDefaultDatasetHeadersService()
    cherrypy.quickstart(webapp, '/', "app.ini")


def main():
    environment = parse_arguments()
    start_server(environment)


if __name__ == '__main__':
    main()
