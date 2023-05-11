import clacks_rpc
from clacks.tests import ClacksTestCase


class TestRPCServer(ClacksTestCase):

    marshaller_type = clacks_rpc.ClacksRPCMarshaller

    server_interfaces = ['standard', 'rpc_core']

    proxy_interfaces = []

    def build_client_instance(self):
        return clacks_rpc.ClacksRPCProxyClient(self.address, self.create_handler())

    def test_standard_commands(self):
        commands = self.client.list_commands()
        assert isinstance(commands, list)

    def test_get_proxy(self):
        command = self.client.get_command
        assert isinstance(command, clacks_rpc.ClacksRPCObjectProxy)
