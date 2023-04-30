import clacks
from .cache import retrieve_object
from clacks import ServerInterface


# ----------------------------------------------------------------------------------------------------------------------
class ClacksRPCServerInterface(ServerInterface):
    """
    Core set of methods for use with the Clacks RPC server.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def obj_from_guid(self, guid):
        if guid is None:
            obj = self.server
        else:
            obj = retrieve_object(guid)
        if not obj:
            raise KeyError(f'object with guid {guid} could not be found!')
        return obj

    # ------------------------------------------------------------------------------------------------------------------
    def index__(self, guid):
        obj = self.obj_from_guid(guid)
        return obj.__index__()

    # ------------------------------------------------------------------------------------------------------------------
    def next__(self, guid):
        obj = self.obj_from_guid(guid)
        return obj.__next__()

    # ------------------------------------------------------------------------------------------------------------------
    def iter__(self, guid):
        obj = self.obj_from_guid(guid)
        return obj.__iter__()

    # ------------------------------------------------------------------------------------------------------------------
    def call__(self, guid, *args, **kwargs):
        obj = self.obj_from_guid(guid)

        if not args and not kwargs:
            return obj()

        if args and not kwargs:
            return obj(*args)

        if kwargs and not args:
            return obj(**kwargs)

        return obj(*args, **kwargs)

    # ------------------------------------------------------------------------------------------------------------------
    def getattr__(self, key: str, guid: str):
        obj = self.obj_from_guid(guid)
        return obj.__getattr__(key)


clacks.register_server_interface_type('rpc_core', interface_type=ClacksRPCServerInterface)
