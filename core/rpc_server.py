from .cache import retrieve_object
from clacks import ServerBase, ServerCommand


# ----------------------------------------------------------------------------------------------------------------------
class ClacksRPCServer(ServerBase):

    # ------------------------------------------------------------------------------------------------------------------
    def index__(self, guid):
        obj = retrieve_object(guid)
        if not obj:
            raise KeyError(f'object with guid {guid} could not be found!')
        return obj.__index__()

    # ------------------------------------------------------------------------------------------------------------------
    def next__(self, guid):
        obj = retrieve_object(guid)
        if not obj:
            raise KeyError(f'object with guid {guid} could not be found!')
        return obj.__next__()

    # ------------------------------------------------------------------------------------------------------------------
    def iter__(self, guid):
        obj = retrieve_object(guid)
        if not obj:
            raise KeyError(f'object with guid {guid} could not be found!')
        return obj.__iter__()

    # ------------------------------------------------------------------------------------------------------------------
    def call__(self, guid, *args, **kwargs):
        obj = retrieve_object(guid)
        if not obj:
            raise KeyError(f'object with guid {guid} could not be found!')
        if not args and not kwargs:
            return obj()
        if args and not kwargs:
            return obj(*args)
        if kwargs and not args:
            return obj(**kwargs)
        return obj(*args, **kwargs)

    # ------------------------------------------------------------------------------------------------------------------
    def getattr__(self, key: str, guid: bytes):
        obj = retrieve_object(guid)
        if not obj:
            raise KeyError(f'object with guid {guid} could not be found!')
        return getattr(obj, key)

    # ------------------------------------------------------------------------------------------------------------------
    def __getattr__(self, item):
        # type: (str) -> object
        """
        Overridden attribute getter magic method that helps to ensure commands can be called by calling them as
        functions directly on the server instance. This helps with RPYC servers as well.

        :param item: the name of the attribute to get
        :type item: str

        :return: Whatever value is returned by the attribute
        :rtype: object
        """
        if item in self.__dict__:
            return self.__dict__[item]

        for interface in self.interfaces.values():
            if hasattr(interface, item):
                return getattr(interface, item)

        raise AttributeError(item)

    # ------------------------------------------------------------------------------------------------------------------
    def get_command(self, key):  # type: (str) -> ServerCommand | None
        """
        Unlike the basic ServerBase class, the RPC Server instead dynamically decides whether a request can result
        in a response at the time of its request.
        """
        value = super(ClacksRPCServer, self).get_command(key)

        if isinstance(value, ServerCommand):
            return value

        value = getattr(self, key)

        if not value:
            raise AttributeError(key)

        _value = value
        if not callable(value):
            # -- construct a quick function wrapper to return the value
            def fn():
                return value
            _value = fn

        # -- if the returned value is not a server command, return instead a ProxyCommand
        return ServerCommand.construct(self, _value)
