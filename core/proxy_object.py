import json
import clacks


# ----------------------------------------------------------------------------------------------------------------------
class ClacksRPCObjectProxy(object):
    """
    This class functions as a sort of mini-proxy server. It implements most object magic methods that python works with,
    and in so doing allows a user to operate on an object that only exists server-side as if the object existed on the
    client.

    However, this being a `clacks` environment, all RPC calls are routed through the standard command layer, ensuring
    that most object attributes are inaccessible, unless exposed by an interface method.
    """

    server: clacks.ClientProxyBase
    guid: str
    attrs: dict

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, **kwargs):
        self.guid = kwargs.get('guid')
        self.server = None

        self.attrs = dict()

        for kw in kwargs:
            self.attrs[kw] = kwargs[kw]

    # ------------------------------------------------------------------------------------------------------------------
    def __del__(self):
        return self.server.question('del__', guid=self.guid).response

    # ------------------------------------------------------------------------------------------------------------------
    def __repr__(self):
        data = json.dumps(self.attrs, sort_keys=True)
        return f'| [ClacksRPCObjectProxy] {data} |'

    # ------------------------------------------------------------------------------------------------------------------
    def __index__(self):
        return self.server.question('index__', guid=self.guid).reponse

    # ------------------------------------------------------------------------------------------------------------------
    def __iter__(self):
        return self.server.question('iter__', guid=self.guid).response

    # ------------------------------------------------------------------------------------------------------------------
    def __next__(self):
        try:
            response = self.server.question('next__', guid=self.guid).response
            return response
        except Exception as e:
            if 'StopIteration' in str(e):
                raise StopIteration
        raise Exception

    # ------------------------------------------------------------------------------------------------------------------
    def __call__(self, *args, **kwargs):
        return self.server.question('call__', guid=self.guid, *args, **kwargs).response

    # ------------------------------------------------------------------------------------------------------------------
    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__.get(item)
        return self.server.question('getattr__', key=item, guid=self.guid).response
