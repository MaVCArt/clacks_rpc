from clacks import ClientProxyBase

# ----------------------------------------------------------------------------------------------------------------------
class ClacksRPCProxyClient(ClientProxyBase):

    # ------------------------------------------------------------------------------------------------------------------
    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__.get(key)

        if self.__dict__['proxy_commands'].get(key):
            return self.proxy_commands.get(key)

        return self.question(key).response
