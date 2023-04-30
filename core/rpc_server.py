from clacks import ServerBase


# ----------------------------------------------------------------------------------------------------------------------
class ClacksRPCServer(ServerBase):

    REQUIRED_INTERFACES = [
        'standard',
        'rpc_core',
    ]

    # ------------------------------------------------------------------------------------------------------------------
    def get_command(self, key):  # type: (str) -> ServerCommand
        cmd = super(ClacksRPCServer, self).get_command(key)
        if hasattr(cmd, 'rpc_hidden') and getattr(cmd, 'rpc_hidden'):
            raise AttributeError
        return cmd
