from typing import Iterable
from clacks import ClientProxyBase

# ----------------------------------------------------------------------------------------------------------------------
class ClacksRPCProxyClient(ClientProxyBase):

    # ------------------------------------------------------------------------------------------------------------------
    def __dir__(self) -> Iterable[str]:
        result = super(ClacksRPCProxyClient, self).__dir__()
        server_dir = self.question('getattr__', key='__dir__', guid=None).response
        result += server_dir()
        result = sorted(list(set(result)))
        return result

    # ------------------------------------------------------------------------------------------------------------------
    def __getattr__(self, key):
        if key.startswith('__'):
            return self.question(f'getattr__', key=key.lstrip('__'), guid=None).response

        if key in self.__dict__:
            return self.__dict__.get(key)

        if self.__dict__['proxy_commands'].get(key):
            return self.proxy_commands.get(key)

        return self.question(f'getattr__', key=key, guid=None).response
