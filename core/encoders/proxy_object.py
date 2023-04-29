import json
from uuid import uuid4
from ..proxy_object import ClacksRPCObjectProxy
from ..cache import store_object, retrieve_object
from ..rpc_marshaller import ClacksRPCDecoder, ClacksRPCEncoder


# ----------------------------------------------------------------------------------------------------------------------
class ClacksRPCProxyObjectEncoder(ClacksRPCEncoder):

    # -- give these the lowest priority as it is the fallback encoder
    PRIORITY = -9999999

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def viable(cls, type_key: str) -> bool:
        return True

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def encode(cls, value: object) -> tuple[str, bytes]:
        type_key = 'proxy'
        guid = uuid4().hex

        store_object(value, guid)

        data = {
            'guid': guid,
            '__str__': value.__str__(),
            '__type__': type(value).__name__,
        }

        return type_key, bytes(json.dumps(data), 'utf-8')


# ----------------------------------------------------------------------------------------------------------------------
class ClacksRPCProxyObjectDecoder(ClacksRPCDecoder):

    # -- give these the lowest priority as it is the fallback encoder
    PRIORITY = -9999999

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def viable(cls, type_key: str) -> bool:
        return True

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def decode(cls, value: bytes) -> object:
        data = value.decode('utf-8')
        data = json.loads(data)
        return ClacksRPCObjectProxy(**data)
