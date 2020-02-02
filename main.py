"""
Things that can be improved:
- Thread use on execute different algorithms concurrently

TODO List
- Add Azure ML provider
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
    server_conf = {
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080
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
