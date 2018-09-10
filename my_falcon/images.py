# import json

import io
import os
import uuid
import mimetypes

import falcon
import msgpack

class Resource(object):

    _CHUNK_SIZE_BYTES = 4096

    # The resource object must now be initialized with a path used during POST.
    def __init__(self, storage_path):
        self._storage_path = storage_path
        # modified `app.py` and passed in a path to the initializer.

    def on_get(self, req, resp):
        doc = {
            'images': [
                {
                    'href': '/images/1eaf6ef1-7f2d-4ecc-a8d5-6e8adba7cc0e.png'
                }
            ]
        }

        # resp.body = json.dumps(doc, ensure_ascii=False)

        resp.data = msgpack.packb(doc, use_bin_type=True)
        # NOTE the use of `resp.data` in lieu of `resp.body`. If you assign a bytestring to the later, Falcon will figure it out, but you can realize a small performance gain by assigning directly to `resp.data`.

        resp.content_type = falcon.MEDIA_MSGPACK
        # The `falcon` module provides a number of constants for common media types, including `falcon.MEDIA_JSON`, `falcon.MEDIA_XML`, etc.

        # The following line can be ommitted because 200 is the default status returned by the framework, but it is included here to illistrate how this may be overridden as needed.
        resp.status = falcon.HTTP_200
    
    # For any HTTP method you want your resource to support, simply add an `on_*()` method to the class.

    # on_get(), on_post(), on_head(), etc are called `responders`.

    def on_post(self, req,resp):
        ext = mimetypes.guess_extension(req.content_type)
        name = '{uuid}{ext}'.format(uuid=uuid.uuid4(), ext=ext)
        # Generate a unique name for the image
        image_path = os.path.join(self._storage_path, name)

        with io.open(image_path, 'wb') as image_file:
            while True:
                chunk = req.stream.read(self._CHUNK_SIZE_BYTES)
                # reading from `req.stream`
                # It's called `stream` instead of `body` to emphasize that you are really reading from an input stream; by default Falcon does not spool or decode request data, instead giving you direct access to the incoming binary stream provided by the WSGI server.
                if not chunk:
                    break
                
                image_file.write(chunk)
                # writing it out on `image_file`
        
        resp.status = falcon.HTTP_201
        resp.location = '/images/' + name
        # We used `falcon.HTTP_201` to set the response status to "201 Created". We could also use `falcon.HTTP_CREATED` alias.

        # The `Request` and `Response` classes contain convent attributes for reading and setting common headers, but you can always access any header by name with the `req.get_header()` and `resp.set_header()` methods.