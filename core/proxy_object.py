import json
import clacks


# ----------------------------------------------------------------------------------------------------------------------
class ClacksRPCObjectProxy(object):

    server: clacks.ClientProxyBase
    guid: str

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, **kwargs):
        self.guid = kwargs.get('guid')
        self.server = None

        self.attrs = dict()

        for kw in kwargs:
            self.attrs[kw] = kwargs[kw]

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
