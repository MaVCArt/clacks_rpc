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
