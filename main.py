"""
TODO List
- CSS
- Modify README.md with description and license
- Allow example dataset selection
- Use same hiperparameters for the same algorithm on different providers
- Return same result structure from different providers
- Add file size limit (1 MB)
- make JSON all API returns?
"""
import os

import cherrypy

from WebServer import WebServer, GetOptionsService, SetOptionsService, GetDefaultDatasetHeadersService

if __name__ == '__main__':
    if not os.path.exists('temp'):
        os.makedirs('temp')

    if not os.path.exists('log'):
        os.makedirs('log')

    server_conf = {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8080,
        'log.access_file': 'log/access.log',
        'log.error_file': 'log/error.log',
        'environment': 'production',
    }

    app_conf = {
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
        },
        '/get_options': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/set_options': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/get_default_dataset_headers': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'public'
        }
    }
    cherrypy.config.update(server_conf)

    webapp = WebServer()
    webapp.get_options = GetOptionsService()
    webapp.set_options = SetOptionsService()
    webapp.get_default_dataset_headers = GetDefaultDatasetHeadersService()
    cherrypy.quickstart(webapp, '/', app_conf)
