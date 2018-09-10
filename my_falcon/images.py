# import json
import falcon
import msgpack

class Resource(object):

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