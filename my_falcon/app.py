import falcon
from .images import Resource

api = application = falcon.API()

# This code creates my WSGI application and aliases it as api.
# Gunicorn by default expects 'application' to be name of the variable.

# A WSGI application is just a callable with a well-defined signature so that you can host the application with any web server that understands the WSGI protocol.


#  POST        /players/45301f54/achievements
# └──────┘    └────────────────────────────────┘
#  Action            Resource Identifier


# Falcon uses Python classes to represent resources. In practice, these classes act as controllers in your application.

# Each requested URL is mapped to a specific resource.

images = Resource()
api.add_route('/images', images)

# 'add_route()' expects an instance of the resource class, not the class itself. The same instance is used for all requests. This strategy improves performace and reduces memory usage, but this also means that if you host your application with a threaded web server, resources and thier dependencies must be thread-safe.

# Like a GET responder, there is OPTIONS responder. If a resource does not include its own OPTIONS responder, the framework provides a default implementation. Therefore, OPTIONS is always included in the list of allowable methods.

"""
In other Python web frameworks, we may be used to using decorators to setup up your routes. Falcon's particular approach provides the following benefits:
    * The URL structure of the application is centralized. This makes it easier to reason about and maintain the API over time.
    * The use of resource classes maps somewhat natutally to the REST architectural style, in which a URL is used to identify a resource only, not the action to perform on that resource.
    * Resource class methods provide a uniform interface that does not have to be reinvented (and maintained) from class to class and application to application.
"""

