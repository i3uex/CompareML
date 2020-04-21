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

    cherrypy.config.update("global.ini")

    webapp = WebServer()
    webapp.get_options = GetOptionsService()
    webapp.set_options = SetOptionsService()
    webapp.get_default_dataset_headers = GetDefaultDatasetHeadersService()
    cherrypy.quickstart(webapp, '/', "app.ini")
