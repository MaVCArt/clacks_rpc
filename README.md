# clacks_rpc

Clacks Library that uses the clacks framework's extensibility to create an RPC-like proxy interface that can wrap
objects for RPC programming.

It uses a similar approach to PyRPC, in that it uses recognized "encoders" to serialize / deserialize any object type
it knows how to do so with, and wraps any other type of object in a "remote object" class which functions as its own
mini-proxy server.

All these mini-proxy-server-objects are parented to the main Proxy server they are created by, and have a server-side
GUID paired with them that tells the server which object is being accessed.

Each new object that is assigned a GUID on the server layer is then assigned a weakref pointer, which ensures it is not
stopped from being garbage collected.

## Setting up a Clacks-RPC server

### Server

```python
import clacks
import clacks_rpc

handler = clacks.SimpleRequestHandler(clacks_rpc.ClacksRPCMarshaller())
server = clacks.ServerBase('foobar', False, threaded_digest=True)
server.register_interface_by_key('standard')
server.register_interface_by_key('rpc_core')
server.register_handler('localhost', 9000, handler)
server.start(blocking=True)
```

### Client

```python
import clacks
import clacks_rpc

handler = clacks.SimpleRequestHandler(clacks_rpc.ClacksRPCMarshaller())
proxy = clacks_rpc.ClacksRPCProxyClient(('localhost', 9000), handler, connect=True)
print(proxy.list_commands())
```
