"""
Things that can be improved:
- Thread use on execute different algorithms concurrently

TODO List
- Solve "ValueError: could not convert string to float: 'x'" using mushroom data (Scikit)
- Add Azure ML provider
- Use same train/test split seed on all executions
- Return same result structure from different providers
- Use same hiperparameters for the same algorithm on different providers
- CSS on Front
- Beautify result display

TEST: When values from target feature are not str nor int
"""
import os

import cherrypy

from WebServer import WebServer, GetOptionsService, SetOptionsService

if __name__ == '__main__':
    if not os.path.exists('temp'):
        os.makedirs('temp')

    if not os.path.exists('log'):
        os.makedirs('log')

    server_conf = {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8080,
        'log.access_file': 'log/access.log',
        'log.error_file': 'log/error.log'
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
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'public'
        }
    }
    cherrypy.config.update(server_conf)

    webapp = WebServer()
    webapp.get_options = GetOptionsService()
    webapp.set_options = SetOptionsService()
    cherrypy.quickstart(webapp, '/', app_conf)
