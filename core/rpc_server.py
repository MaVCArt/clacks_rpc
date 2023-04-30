from clacks import ServerBase


# ----------------------------------------------------------------------------------------------------------------------
class ClacksRPCServer(ServerBase):

    REQUIRED_INTERFACES = [
        'standard',
        'rpc_core',
    ]
